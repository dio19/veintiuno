"""
Veintiuno - investigacion_hotel · Motor de la corrida
=====================================================
Orquesta el loop agentico y, sobre todo, HACE CUMPLIR el contrato: un hallazgo
sin fuente resoluble y sin cita comprobable no entra al dossier como dato.

El prompt le pide al agente que no invente. Este archivo se asegura de que no
pueda, aunque quiera o aunque se distraiga.

Dos detalles tecnicos que no son opcionales:

- El tool_runner de Python NO reanuda sólo un `pause_turn`, y con busqueda
  server-side eso pasa. La corrida terminaria sin error y con la respuesta
  truncada: se ve como un dossier pobre, no como una falla. Por eso espejamos
  el historial y reiniciamos el runner con el turno pausado adjunto.
- Los errores de las herramientas server-side NO levantan excepcion: vuelven
  con HTTP 200 y un objeto de error adentro del bloque. Hay que mirarlo.
"""

import re
import time
import unicodedata
from dataclasses import dataclass, field

from . import config, prompts
from .estimacion import estimar
from .modelo import (
    CAMPOS,
    Dossier,
    Fuente,
    Hallazgo,
    Interpretacion,
    VerificacionPendiente,
    VERIFICADO,
    SIN_VERIFICAR,
    normalizar_valor,
)
from .scoring import calificar
from .herramientas import padron_gcba, places, sitio_hotel, web

MAX_CHARS_PAGINA = 6000  # lo que le pasamos al modelo de una pagina

# Que campos responden cada una de las 8 preguntas del ICP. Sirve para no
# duplicar pendientes: si el agente ya marco el campo, la pregunta esta cubierta.
CAMPOS_POR_PREGUNTA = {
    1: ("pct_resenas_idioma_extranjero", "muestra_resenas"),
    2: ("habitaciones",),
    3: ("es_cadena",),
    4: ("decisor_nombre", "decisor_rol", "decisor_contacto", "decisor_es_generico"),
    5: ("sitio_en_ingles", "motor_reserva_propio"),
    6: ("adr_publicado_ars",),
    7: ("barrio",),
    8: ("menciona_exencion", "publica_precios_usd"),
}


@dataclass
class Presupuesto:
    max_busquedas: int = config.MAX_BUSQUEDAS
    max_fetches: int = config.MAX_FETCHES
    max_turnos: int = config.MAX_TURNOS
    timeout_total_s: int = config.TIMEOUT_TOTAL_S

    busquedas: int = 0
    fetches: int = 0
    turnos: int = 0
    verificaciones: int = 0
    tokens_entrada: int = 0
    tokens_salida: int = 0
    arranque: float = field(default_factory=time.monotonic)

    @property
    def transcurrido(self) -> float:
        return time.monotonic() - self.arranque

    def hay_tiempo(self) -> bool:
        return self.transcurrido < self.timeout_total_s

    def puede_fetch(self) -> bool:
        return self.fetches < self.max_fetches and self.hay_tiempo()

    def agotado(self) -> bool:
        return self.turnos >= self.max_turnos or not self.hay_tiempo()

    def resumen(self) -> dict:
        return {
            "turnos": f"{self.turnos}/{self.max_turnos}",
            "búsquedas web": f"{self.busquedas}/{self.max_busquedas}",
            "páginas leídas": f"{self.fetches}/{self.max_fetches}",
            "verificaciones de cita": self.verificaciones,
            "tokens entrada": self.tokens_entrada,
            "tokens salida": self.tokens_salida,
            "duración": f"{self.transcurrido:.0f}s",
        }


def _aplanar(texto: str) -> str:
    """Normaliza para comparar citas: sin acentos, sin puntuacion, sin espacios.

    Tolera que el modelo cite con comillas distintas o espaciado raro, sin
    tolerar que cite algo que no está.
    """
    sin_acentos = "".join(
        c for c in unicodedata.normalize("NFD", texto or "") if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"[^a-z0-9]", "", sin_acentos.lower())


class Investigacion:
    """Estado de una corrida. Las herramientas del agente son metodos de acá."""

    def __init__(
        self,
        hotel: str,
        ciudad: str,
        sitio: str | None = None,
        padron_local: str | None = None,
        presupuesto: Presupuesto | None = None,
    ):
        self.dossier = Dossier(hotel_consultado=hotel, ciudad=ciudad)
        self.presupuesto = presupuesto or Presupuesto()
        self.sitio_conocido = sitio
        self.padron_local = padron_local
        self.contenidos: dict[str, str] = {}  # url -> texto ya visto
        self.registro: list[str] = []  # bitacora legible de la corrida

        # ------------------------------------------------------------------
        # Verificacion de citas: el nucleo del contrato
        # ------------------------------------------------------------------

    def _verificar_cita(self, url: str, cita: str) -> tuple:
        """(ok, motivo). Busca la cita en el contenido de esa URL.

        Si no leimos esa página todavia, la traemos. Si no se puede traer
        (403, muro de JavaScript, sitio caido), NO damos por buena la cita:
        el hallazgo queda sin verificar y se abre una verificación pendiente.
        Es el caso tipico de Booking, y está bien que sea así.
        """
        if not cita or len(cita.strip()) < 8:
            return False, "cita vacia o demasiado corta para comprobar"

        texto = self.contenidos.get(url)
        if texto is None:
            if not self.presupuesto.puede_fetch():
                return False, "no quedaba presupuesto para verificar la fuente"
            r = web.traer(url)
            self.presupuesto.fetches += 1
            self.presupuesto.verificaciones += 1
            if not r.ok:
                return (
                    False,
                    f"no se pudo leer la fuente para comprobar la cita ({r.error or r.status})",
                )
            texto = r.texto
            self.contenidos[url] = texto

        aguja, pajar = _aplanar(cita), _aplanar(texto)
        if not aguja:
            return False, "la cita no tiene texto comparable"
        if aguja in pajar:
            return True, ""
            # Citas largas se cortan o se recomponen: alcanza con un nucleo presente.
        if len(aguja) > 60 and aguja[:60] in pajar:
            return True, ""
        return False, "la cita no aparece en la fuente citada"

        # ------------------------------------------------------------------
        # Herramientas
        # ------------------------------------------------------------------

    def registrar_hallazgo(
        self, campo: str, valor: str, fuente_url: str, cita: str, confianza: str = "media"
    ) -> str:
        if campo not in CAMPOS:
            return (
                f"ERROR: '{campo}' no es un campo valido. Usa exactamente uno de: "
                f"{', '.join(CAMPOS )}."
            )
        try:
            valor_normalizado = normalizar_valor(campo, valor)
        except ValueError as e:
            return f"ERROR: {e}. No lo registres de otra forma: corregi el valor."

        url = (fuente_url or "").strip()
        if not url.startswith(("http://", "https://")):
            self._guardar_sin_verificar(campo, valor_normalizado, cita, "sin URL de fuente")
            return (
                f"Registrado '{campo}' como {SIN_VERIFICAR}: no diste una URL de "
                f"fuente valida, asi que no suma al puntaje. Si tenes la fuente, "
                f"volve a registrarlo con la URL."
            )

        ok, motivo = self._verificar_cita(url, cita)
        if not ok:
            self._guardar_sin_verificar(campo, valor_normalizado, cita, motivo, url)
            self.pendiente(
                campo,
                f"Confirmar '{campo}' = {valor_normalizado}",
                url,
                f"el agente lo encontró pero no se pudo comprobar: {motivo}",
            )
            return (
                f"Registrado '{campo}' como {SIN_VERIFICAR}: {motivo}. "
                f"Queda como verificacion pendiente. Si tenes otra fuente donde la "
                f"cita aparezca textual, registralo de nuevo con esa."
            )

        self.dossier.hallazgos[campo] = Hallazgo(
            campo=campo,
            valor=valor_normalizado,
            estado=VERIFICADO,
            fuente=Fuente(url),
            cita=cita.strip()[:300],
            confianza=confianza if confianza in ("alta", "media", "baja") else "media",
        )
        self.registro.append(f"hallazgo {campo}={valor_normalizado} <- {url}")
        return f"OK: '{campo}' = {valor_normalizado}, verificado contra la fuente."

    def observar(self, campo: str, valor, fuente_url: str, cita: str, nota: str = "") -> bool:
        """Registra algo que observo el CODIGO, no el modelo.

        La verificación por cita existe porque una afirmacion del LLM puede no
        estar en ninguna fuente. Cuando el dato sale de una herramienta nuestra
        que parseo la respuesta ella misma -el padron, Places, las huellas del
        sitio- ese riesgo no existe: Python ya lo vio. Pedirle una cita textual
        a una respuesta JSON no agregaria garantia, sólo perderia el dato.

        Devuelve False si el valor no pasa la validacion de tipo.
        """
        try:
            valor_normalizado = normalizar_valor(campo, valor)
        except ValueError as e:
            self.registro.append(f"observacion descartada: {e}")
            return False
        self.dossier.hallazgos[campo] = Hallazgo(
            campo=campo,
            valor=valor_normalizado,
            estado=VERIFICADO,
            fuente=Fuente(fuente_url),
            cita=cita[:300],
            confianza="alta",
            # La marca de procedencia va siempre: es lo que distingue este dato
            # de una afirmacion del modelo, y no tiene que poder perderse al
            # pasar una nota propia.
            nota=(
                "observado por la herramienta, no afirmado por el modelo"
                + (f" ({nota})" if nota else "")
            ),
        )
        self.registro.append(f"observado {campo}={valor_normalizado} <- {fuente_url}")
        return True

    def consultar_places(self, nombre: str = "", ciudad: str = "") -> str:
        """Consulta Google Places y registrá lo que devuelve, sin pasar por el modelo."""
        if not places.hay_clave():
            return (
                "Google Places no está configurado (falta GOOGLE_PLACES_API_KEY). "
                "Resolvé el idioma de las reseñas por otra vía, o marcalo pendiente."
            )
        r = places.consultar(
            nombre or self.dossier.hotel_consultado, ciudad or self.dossier.ciudad
        )
        if r.error:
            return f"Places no pudo responder: {r.error}"
        if not r.encontrado:
            return "Places no encontró ese alojamiento."

        fuente = r.url_maps or "https://maps.google.com/"
        registrados = []
        if r.pct_extranjero is not None:
            cita = f"idiomas de las resenas: {', '.join(r.idiomas )}"
            if self.observar(
                "pct_resenas_idioma_extranjero",
                r.pct_extranjero,
                fuente,
                cita,
                f"Google Places, muestra de {r.muestra} resenas",
            ):
                registrados.append("pct_resenas_idioma_extranjero")
            if self.observar("muestra_resenas", r.muestra, fuente, cita, "Google Places"):
                registrados.append("muestra_resenas")
        if r.web:
            self.observar("web", r.web, fuente, f"sitio web: {r.web}", "Google Places")
            registrados.append("web")

            # La muestra chica no se puede tapar: queda anotado como pendiente para
            # que alguien mire las 30 resenas de verdad antes de cerrar el numero.
        self.pendiente(
            "pct_resenas_idioma_extranjero",
            "Confirmar el porcentaje sobre las últimas 30 reseñas, no sobre "
            f"las {r.muestra} que devuelve Places",
            fuente,
            "Places entrega hasta 5 reseñas; el ICP pide 30",
        )

        return (
            f"Places: {r.nombre} | {r.direccion} | rating {r.rating} "
            f"({r.total_resenas} resenas en total)\n"
            f"Idiomas de la muestra: {', '.join(r.idiomas )or 'ninguno'}\n"
            f"Registrado automaticamente: {', '.join(registrados )or 'nada'}\n"
            f"{r.aviso}"
        )

    def _guardar_sin_verificar(self, campo, valor, cita, motivo, url=""):
        self.dossier.hallazgos[campo] = Hallazgo(
            campo=campo,
            valor=valor,
            estado=SIN_VERIFICAR,
            fuente=Fuente(url) if url else None,
            cita=cita.strip()[:300],
            confianza="baja",
            nota=motivo,
        )
        self.registro.append(f"SIN VERIFICAR {campo}: {motivo}")

    def pendiente(self, campo: str, pregunta: str, url: str = "", porque: str = "") -> str:
        if any(p.campo == campo for p in self.dossier.pendientes):
            return "Ya estaba anotado como pendiente."
        self.dossier.pendientes.append(
            VerificacionPendiente(campo=campo, pregunta=pregunta, url=url, porque=porque)
        )
        return "Anotado como verificación pendiente."

    def leer_sitio(self, url: str) -> str:
        if not self.presupuesto.puede_fetch():
            return (
                "ERROR: se agoto el presupuesto de lecturas. Registra lo que tengas y termina."
            )
        s = sitio_hotel.analizar(url)
        self.presupuesto.fetches += 1
        if not s.accesible:
            return f"No se pudo leer {url}: {s.error}"

        r = web.traer(url)
        self.contenidos[s.url] = r.texto
        senales = [f"idiomas declarados: {', '.join(s.idiomas.valor )or 'ninguno'}"]
        for nombre in (
            "sitio_en_ingles",
            "publica_precios_usd",
            "menciona_exencion",
            "pms_detectado",
            "motor_reserva_propio",
            "instagram",
            "whatsapp",
        ):
            senal = getattr(s, nombre)
            if senal.valor:
                senales.append(f'{nombre} = {senal.valor} | cita: "{senal.cita}"')
        if s.mails.valor:
            senales.append(f"mails publicados: {', '.join(s.mails.valor )}")

        return (
            "SENALES DETECTADAS (podes registrarlas citando textual lo que figura "
            "entre comillas):\n- "
            + "\n- ".join(senales)
            + f"\n\nTEXTO DE LA PAGINA ({s.url}):\n"
            + r.texto[:MAX_CHARS_PAGINA]
        )

    def buscar_en_padron_gcba(self, nombre: str) -> str:
        res, err = padron_gcba.buscar(nombre, ruta_local=self.padron_local)
        if err:
            self.dossier.modo_degradado = True
            return f"No se pudo consultar el padron: {err}"
        if not res:
            return (
                f"'{nombre}' no aparece en el padron abierto del GCBA. Puede ser que "
                f"este fuera de CABA, que use otro nombre de fantasia, o que no este "
                f"registrado. No lo des por inexistente."
            )

            # El contenido del padron cuenta como fuente leida: asi las citas sobre
            # estos campos se pueden comprobar sin volver a bajar el CSV.
        self.contenidos[config.URL_PADRON_GCBA] = "\n".join(
            " | ".join(f"{k}: {v}" for k, v in f.items() if not k.startswith("_"))
            for f in res
        )

        lineas = [f"Fuente para citar: {config.URL_PADRON_GCBA}", ""]
        for f in res:
            aviso = f"  <-- {f['_advertencia']}" if f.get("_advertencia") else ""
            lineas.append(
                f"[similitud {f['_similitud']}] nombre: {f['nombre']} | tipo: {f['tipo']} "
                f"| direccion: {f['direccion']} | tel: {f.get('telefono', '')} "
                f"| email: {f.get('email', '')} | web: {f.get('web', '')}{aviso}"
            )
        lineas.append("")
        lineas.append(
            "Elegi vos cual corresponde, o ninguna. Fijate en la direccion y el "
            "sitio web, no sólo en el parecido del nombre."
        )
        return "\n".join(lineas)

    def registrar_interpretacion(
        self, angulo_de_entrada: str, objecion_esperada: str, proximo_paso: str
    ) -> str:
        self.dossier.interpretacion = Interpretacion(
            angulo_de_entrada=angulo_de_entrada.strip(),
            objecion_esperada=objecion_esperada.strip(),
            proximo_paso=proximo_paso.strip(),
        )
        return "Interpretación registrada. Si ya juntaste lo importante, termina acá."

        # ------------------------------------------------------------------

    def cerrar(self) -> Dossier:
        """Calcula puntaje y estimación y devuelve el dossier listo para render."""
        d = self.dossier
        d.score = calificar(d)
        d.estimacion = estimar(d)
        d.consumo = self.presupuesto.resumen()

        if self.presupuesto.agotado():
            faltan = [r.pregunta for r in d.score.respuestas if not r.evaluable]
            d.secciones_incompletas = faltan or ["la investigacion"]
            # Cada pregunta sin dato abre una pendiente, salvo que el agente ya
            # haya anotado una sobre alguno de los campos que la responden: dos
            # entradas para lo mismo hacen que la lista deje de leerse.
        ya_anotados = {p.campo for p in d.pendientes}
        for r in d.score.respuestas:
            if r.evaluable:
                continue
            if ya_anotados & set(CAMPOS_POR_PREGUNTA.get(r.numero, ())):
                continue
            d.pendientes.append(
                VerificacionPendiente(
                    campo=f"pregunta {r.numero}",
                    pregunta=r.pregunta,
                    porque=f"vale {r.maximo} puntos del puntaje ICP y quedo sin dato",
                )
            )
        return d

        # ======================================================================
        # Loop agentico contra la API
        # ======================================================================


DESCRIPCIONES = {
    "registrar_hallazgo": (
        "Registra un dato verificado sobre el hotel. El sistema comprueba que la cita "
        "aparezca textual en la URL: si no aparece, el dato queda SIN VERIFICAR y no "
        "suma al puntaje."
    ),
}


def construir_tools(inv: "Investigacion", max_busquedas: int | None = None) -> list:
    """Arma las herramientas del agente cerrando sobre el estado de la corrida.

    Importa anthropic acá adentro a proposito: el modo offline tiene que poder
    correr sin el SDK instalado.
    """
    from anthropic import beta_tool

    @beta_tool
    def registrar_hallazgo(
        campo: str, valor: str, fuente_url: str, cita: str, confianza: str = "media"
    ) -> str:
        """Registra un dato verificado sobre el hotel.

        El sistema comprueba que la cita aparezca textual en la página de fuente_url.
        Si no aparece, el dato queda marcado SIN VERIFICAR y no suma al puntaje.

        Args:
            campo: Nombre exacto del campo del catalogo (por ejemplo habitaciones).
            valor: El valor observado. Numeros sin unidad, booleanos como si/no.
            fuente_url: URL donde figura el dato. Tiene que empezar con http.
            cita: Fragmento textual de esa página donde se ve el dato.
            confianza: alta, media o baja.
        """
        return inv.registrar_hallazgo(campo, valor, fuente_url, cita, confianza)

    @beta_tool
    def marcar_verificacion_pendiente(
        campo: str, pregunta: str, url: str = "", porque: str = ""
    ) -> str:
        """Anota algo que no se pudo confirmar, para resolverlo a mano despues.

        Usala en vez de estimar o completar por analogia.

        Args:
            campo: Campo del catalogo que quedó sin cerrar.
            pregunta: La pregunta concreta que hay que responder, en una linea.
            url: La URL exacta donde se responde, si la sabes.
            porque: Por qué importa ese dato.
        """
        return inv.pendiente(campo, pregunta, url, porque)

    @beta_tool
    def leer_sitio(url: str) -> str:
        """Lee una página web y devuelve su texto más las señales detectadas.

        Sirve para el sitio propio del hotel y para cualquier página que quieras
        citar. Lo que devuelve es lo único que se puede citar de esa URL.

        Args:
            url: URL completa de la página.
        """
        return inv.leer_sitio(url)

    @beta_tool
    def buscar_en_padron_gcba(nombre: str) -> str:
        """Busca el alojamiento en el padron abierto de la Ciudad de Buenos Aires.

        Es la única fuente oficial de que el alojamiento existe y está registrado,
        y ademas da la categoría (estrellas, boutique, apart). Solo cubre CABA.

        Args:
            nombre: Nombre del hotel tal como lo conoces.
        """
        return inv.buscar_en_padron_gcba(nombre)

    @beta_tool
    def registrar_interpretacion(
        angulo_de_entrada: str, objecion_esperada: str, proximo_paso: str
    ) -> str:
        """Registra tu lectura comercial del caso y termina la investigacion.

        Args:
            angulo_de_entrada: Con que abrir la conversación con este hotel.
            objecion_esperada: La objecion más probable y como responderla.
            proximo_paso: Que hacer concretamente y cuando.
        """
        return inv.registrar_interpretacion(angulo_de_entrada, objecion_esperada, proximo_paso)

    @beta_tool
    def consultar_google_places(nombre: str = "", ciudad: str = "") -> str:
        """Consulta Google Places: rating, cantidad de reseñas y el idioma de una
        muestra de reseñas. Lo que devuelve queda registrado automaticamente, no
        hace falta que lo registres vos.

        Ojo: Places entrega hasta 5 reseñas, no 30. El porcentaje es un indicio.

        Args:
            nombre: Nombre del hotel. Vacio usa el que se está investigando.
            ciudad: Ciudad. Vacio usa la de la corrida.
        """
        return inv.consultar_places(nombre, ciudad)

    herramientas = [
        registrar_hallazgo,
        marcar_verificacion_pendiente,
        leer_sitio,
        buscar_en_padron_gcba,
        registrar_interpretacion,
    ]
    if places.hay_clave():
        herramientas.append(consultar_google_places)

        # Busqueda server-side: corre en la infraestructura de Anthropic y vuelve con
        # las URL de origen, que es justo lo que necesita la disciplina de citar.
    herramientas.append(
        {
            "type": "web_search_20260209",
            "name": "web_search",
            "max_uses": (
                max_busquedas if max_busquedas is not None else inv.presupuesto.max_busquedas
            ),
            "user_location": config.UBICACION_BUSQUEDA,
        }
    )
    return herramientas


def _contar_uso(inv: "Investigacion", mensaje) -> None:
    uso = getattr(mensaje, "usage", None)
    if uso is None:
        return
    inv.presupuesto.tokens_entrada += getattr(uso, "input_tokens", 0) or 0
    inv.presupuesto.tokens_salida += getattr(uso, "output_tokens", 0) or 0


def _revisar_server_tools(inv: "Investigacion", mensaje) -> None:
    """Cuenta busquedas y detecta sus errores.

    Las herramientas server-side no levantan excepcion: vuelven con HTTP 200 y
    un objeto de error adentro del bloque. En exito el `content` es una LISTA;
    en error es un objeto. Hay que ramificar por eso antes de indexar.
    """
    for bloque in getattr(mensaje, "content", []) or []:
        if getattr(bloque, "type", "") != "web_search_tool_result":
            continue
        contenido = getattr(bloque, "content", None)
        if isinstance(contenido, list):
            inv.presupuesto.busquedas += 1
            for r in contenido:
                url = getattr(r, "url", "")
                if url:
                    inv.registro.append(f"busqueda -> {url}")
        else:
            codigo = getattr(contenido, "error_code", "desconocido")
            inv.registro.append(f"ERROR de busqueda web: {codigo}")
            if codigo == "max_uses_exceeded":
                inv.presupuesto.busquedas = inv.presupuesto.max_busquedas


def investigar(
    hotel: str,
    ciudad: str,
    sitio: str | None = None,
    padron_local: str | None = None,
    esfuerzo: str = config.ESFUERZO_DEFAULT,
    presupuesto: Presupuesto | None = None,
    cliente=None,
) -> Dossier:
    """Corre la investigacion completa y devuelve el dossier cerrado.

    Nunca lanza por agotamiento de presupuesto: si se acaba, devuelve el dossier
    con lo que haya y las secciones marcadas como incompletas. Un dossier corto
    y honesto sirve; una excepcion despues de gastar en busquedas, no.
    """
    import anthropic

    inv = Investigacion(hotel, ciudad, sitio, padron_local, presupuesto)
    cliente = cliente or anthropic.Anthropic()
    tools = construir_tools(inv)
    mensajes = [{"role": "user", "content": prompts.tarea(hotel, ciudad, sitio)}]

    reinicios = 0
    while True:
        runner = cliente.beta.messages.tool_runner(
            model=config.MODELO,
            max_tokens=config.MAX_TOKENS,
            system=prompts.SISTEMA,
            thinking={"type": "adaptive"},
            output_config={"effort": esfuerzo},
            tools=tools,
            messages=mensajes,
        )

        ultimo = None
        for mensaje in runner:
            ultimo = mensaje
            inv.presupuesto.turnos += 1
            _contar_uso(inv, mensaje)
            _revisar_server_tools(inv, mensaje)

            # Espejamos el historial: el runner guarda el suyo y no lo expone,
            # y sin esta copia no se puede reanudar un turno pausado.
            mensajes.append({"role": "assistant", "content": mensaje.content})
            respuesta = runner.generate_tool_call_response()
            if respuesta is not None:
                mensajes.append(respuesta)

            if inv.presupuesto.agotado():
                inv.registro.append("presupuesto agotado: se corta la corrida")
                break

        if inv.presupuesto.agotado():
            break
        if ultimo is None or getattr(ultimo, "stop_reason", None) != "pause_turn":
            break

        reinicios += 1
        if reinicios > config.MAX_REINICIOS_PAUSE_TURN:
            inv.registro.append("el turno sigue pausado despues de varios reinicios")
            break
        inv.registro.append(f"turno pausado: reinicio {reinicios}")

    return inv.cerrar()
