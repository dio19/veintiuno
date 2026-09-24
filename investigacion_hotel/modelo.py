"""
Veintiuno - investigacion_hotel · Modelo de datos del dossier
=============================================================
Define QUE se puede saber de un hotel prospecto desde afuera, y con que
respaldo. Es el contrato que hace que el LLM no pueda inventar: un dato entra
al dossier unicamente como Hallazgo, y un Hallazgo sin fuente resoluble queda
marcado SIN VERIFICAR y suma cero al puntaje.

La marca SIN VERIFICAR es la misma convencion que usa research/: cuando no hay
fuente primaria, se escribe el literal en vez de completar por analogia.
"""

from dataclasses import dataclass, field, asdict
from typing import Any
import datetime as dt

SIN_VERIFICAR = "SIN VERIFICAR"

# Estados posibles de un hallazgo.
VERIFICADO = "verificado"

# Procedencia de un insumo de la estimacion.
OBSERVADO = "observado"  # sale de una fuente concreta sobre ESTE hotel
SUPUESTO = "supuesto"  # default nuestro, con su fundamento escrito al lado


@dataclass
class CampoSpec:
    """Un campo que el dossier puede responder.

    `público` es la lista blanca del one-pager externo: si es False, el campo
    NO puede aparecer en material que se le manda al hotel. Es una sola fuente
    de verdad para render/externo.py, no una lista duplicada.
    """

    tipo: str  # texto | entero | porcentaje | booleano | lista
    descripcion: str
    publico: bool = False
    opciones: tuple = ()  # si esta poblado, el valor tiene que ser uno de estos

    # El agente solo puede registrar hallazgos sobre estos campos. Un nombre de
    # campo inventado se rechaza: sin esto, el LLM arma su propio esquema y el
    # render deja de ser auditable.


CAMPOS: dict[str, CampoSpec] = {
    # --- Identificacion ---
    "nombre_oficial": CampoSpec(
        "texto",
        "Razon social o nombre de fantasia tal como figura en fuente oficial",
        publico=True,
    ),
    "domicilio": CampoSpec("texto", "Direccion completa"),
    "barrio": CampoSpec("texto", "Barrio de CABA, o localidad si está fuera"),
    "en_padron_gcba": CampoSpec(
        "booleano", "Figura en el dataset abierto de Alojamientos Turisticos del GCBA"
    ),
    "categoria": CampoSpec("texto", "Categoria declarada: estrellas, boutique, apart"),
    "web": CampoSpec("texto", "URL del sitio propio"),
    # --- Tamano y estructura ---
    "habitaciones": CampoSpec("entero", "Cantidad de habitaciones", publico=True),
    "es_cadena": CampoSpec(
        "texto",
        "Pertenencia a cadena",
        opciones=("independiente", "cadena_local", "cadena_internacional"),
    ),
    # --- Huespedes (proxy del volumen de no residentes) ---
    "pct_resenas_idioma_extranjero": CampoSpec(
        "porcentaje",
        "Porcentaje de reseñas recientes en inglés, portugués, francés o alemán",
        publico=True,
    ),
    "muestra_resenas": CampoSpec(
        "entero",
        "Cuántas reseñas se miraron para calcular el porcentaje anterior",
        publico=True,
    ),
    "nacionalidades_predominantes": CampoSpec(
        "lista", "Países de origen que más aparecen entre los reseñadores", publico=True
    ),
    # --- Señales de pago del exterior (NUNCA una medición: ver aviso del dossier) ---
    "publica_precios_usd": CampoSpec("booleano", "Publica tarifas en dólares", publico=True),
    "moneda_motor_reserva": CampoSpec("texto", "Moneda que ofrece el motor de reserva propio"),
    "menciona_exencion": CampoSpec(
        "booleano",
        "Menciona 'tax free', 'VAT' o exención de IVA en algún canal propio",
        publico=True,
    ),
    # --- Canal de venta ---
    "adr_publicado_ars": CampoSpec(
        "entero", "Tarifa publicada por noche en pesos, con IVA, en fecha alta"
    ),
    "motor_reserva_propio": CampoSpec(
        "booleano", "Tiene motor de reserva directa en su sitio"
    ),
    "pms_detectado": CampoSpec(
        "texto", "PMS o booking engine identificado por la huella de la URL"
    ),
    # --- Presencia online ---
    "sitio_en_ingles": CampoSpec(
        "booleano", "Tiene versión en inglés real, no traductor automático", publico=True
    ),
    "instagram": CampoSpec("texto", "Usuario de Instagram"),
    "responde_resenas": CampoSpec("booleano", "El hotel responde las reseñas públicas"),
    # --- Decisor (solo contacto profesional publicado) ---
    "decisor_nombre": CampoSpec("texto", "Nombre del dueño o gerente general"),
    "decisor_rol": CampoSpec("texto", "Cargo del decisor"),
    "decisor_contacto": CampoSpec("texto", "Vía de contacto profesional publicada"),
    "decisor_es_generico": CampoSpec(
        "booleano", "El único contacto disponible es un mail genérico (info@, reservas@)"
    ),
    # --- Entorno ---
    "competencia": CampoSpec("lista", "Hoteles comparables cercanos y con que señalan"),
}

# Lo que el dossier NO puede responder porque no lo tenemos sin el export del
# hotel. Se imprime en el documento para que nadie confunda una senal publica
# con una medicion. Confundirlas es exactamente como el dossier se vuelve
# mentira frente a un hotelero que si conoce sus numeros.
FUERA_DE_ALCANCE = (
    "ocupación real",
    "ADR real facturado",
    "mezcla real de nacionalidades del PMS",
    "porcentaje real de pago con tarjeta emitida en el exterior",
    "facturación",
    "qué comprobante emite hoy por cada estadía",
)


@dataclass
class Fuente:
    url: str
    titulo: str = ""
    consultada: str = ""

    def __post_init__(self):
        if not self.consultada:
            self.consultada = dt.date.today().isoformat()


@dataclass
class Hallazgo:
    """Un dato sobre el hotel, con su respaldo o con la marca de que no lo tiene."""

    campo: str
    valor: Any
    estado: str = SIN_VERIFICAR
    fuente: Fuente | None = None
    cita: str = ""
    confianza: str = "baja"  # alta | media | baja
    nota: str = ""

    @property
    def verificado(self) -> bool:
        return self.estado == VERIFICADO

    def como_texto(self) -> str:
        """Representacion para el documento. Nunca devuelve un valor pelado si
        el hallazgo no está verificado."""
        if not self.verificado:
            return SIN_VERIFICAR
        if isinstance(self.valor, bool):
            return "sí" if self.valor else "no"
        if isinstance(self.valor, (list, tuple)):
            return ", ".join(str(v) for v in self.valor)
        spec = CAMPOS.get(self.campo)
        if spec and spec.tipo == "porcentaje":
            return f"{self.valor:g}%"
        if spec and spec.tipo == "entero" and self.campo.endswith("_ars"):
            return "ARS " + f"{int(self.valor ):,}".replace(",", ".")
        return str(self.valor)


@dataclass
class VerificacionPendiente:
    """Lo que no se pudo cerrar sólo. Con la URL y la pregunta exacta para que
    se resuelva en dos minutos a mano, en vez de rellenarse a ojo."""

    campo: str
    pregunta: str
    url: str = ""
    porque: str = ""


@dataclass
class Interpretacion:
    """La lectura del agente. Va separada de los datos y rotulada como tal:
    es opinión sobre como entrar, no un hecho sobre el hotel."""

    angulo_de_entrada: str = ""
    objecion_esperada: str = ""
    proximo_paso: str = ""


@dataclass
class Dossier:
    hotel_consultado: str
    ciudad: str
    generado: str = ""
    modo_degradado: bool = False  # corrio sin padron (fuera de CABA)
    hallazgos: dict[str, Hallazgo] = field(default_factory=dict)
    pendientes: list[VerificacionPendiente] = field(default_factory=list)
    interpretacion: Interpretacion | None = None
    score: Any = None  # ResultadoScore, de scoring.py
    estimacion: Any = None  # ResultadoEstimacion, de estimacion.py
    consumo: dict = field(default_factory=dict)
    secciones_incompletas: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.generado:
            self.generado = dt.datetime.now().isoformat(timespec="seconds")

            # -- acceso --

    def valor(self, campo: str, default=None):
        """Valor de un campo SOLO si está verificado. Un hallazgo sin fuente no
        se puede leer como dato: para el resto del sistema, no existe."""
        h = self.hallazgos.get(campo)
        return h.valor if (h and h.verificado) else default

    def hallazgo(self, campo: str) -> Hallazgo | None:
        return self.hallazgos.get(campo)

    def fuentes(self) -> list[Fuente]:
        vistas, salida = set(), []
        for h in self.hallazgos.values():
            if h.fuente and h.fuente.url not in vistas:
                vistas.add(h.fuente.url)
                salida.append(h.fuente)
        return salida

    def a_dict(self) -> dict:
        return asdict(self)


def normalizar_valor(campo: str, valor: Any) -> Any:
    """Convierte el valor crudo que mando el agente al tipo que declara CAMPOS.

    Devuelve el valor convertido, o lanza ValueError con el motivo. El que
    llama decide que hacer con el error; acá no se adivina ni se rellena.
    """
    spec = CAMPOS.get(campo)
    if spec is None:
        raise ValueError(f"campo desconocido: {campo !r}")

    if spec.tipo == "booleano":
        if isinstance(valor, bool):
            return valor
        texto = str(valor).strip().lower()
        if texto in ("si", "sí", "true", "1", "yes"):
            return True
        if texto in ("no", "false", "0"):
            return False
        raise ValueError(f"{campo}: no es booleano: {valor !r}")

    if spec.tipo == "entero":
        try:
            entero = int(float(str(valor).replace(".", "").replace(",", ".")))
        except (TypeError, ValueError):
            raise ValueError(f"{campo}: no es entero: {valor !r}")
        if entero < 0:
            raise ValueError(f"{campo}: negativo: {valor !r}")
        return entero

    if spec.tipo == "porcentaje":
        try:
            numero = float(str(valor).replace("%", "").replace(",", "."))
        except (TypeError, ValueError):
            raise ValueError(f"{campo}: no es porcentaje: {valor !r}")
        if not 0 <= numero <= 100:
            raise ValueError(f"{campo}: fuera de 0-100: {valor !r}")
        return numero

    if spec.tipo == "lista":
        if isinstance(valor, (list, tuple)):
            return [str(v).strip() for v in valor if str(v).strip()]
        return [p.strip() for p in str(valor).split(",") if p.strip()]

    texto = str(valor).strip()
    if spec.opciones and texto not in spec.opciones:
        raise ValueError(f"{campo}: {texto !r} no esta en {spec.opciones}")
    return texto


def dossier_desde_dict(d: dict) -> Dossier:
    """Reconstruye un Dossier guardado en JSON.

    Restaura los hallazgos, las pendientes y la interpretación. NO restaura el
    puntaje ni la estimación: se recalculan. Ese es justamente el punto de
    --rehacer — editas un hallazgo a mano y el veredicto se rehace sólo, sin
    volver a pagar la investigacion.
    """
    dossier = Dossier(
        hotel_consultado=d.get("hotel_consultado", ""),
        ciudad=d.get("ciudad", ""),
        generado=d.get("generado", ""),
        modo_degradado=bool(d.get("modo_degradado")),
        consumo=d.get("consumo") or {},
        secciones_incompletas=list(d.get("secciones_incompletas") or []),
    )

    for campo, h in (d.get("hallazgos") or {}).items():
        if campo not in CAMPOS:
            continue  # el catalogo cambio: se descarta en vez de romper
        fuente = h.get("fuente")
        dossier.hallazgos[campo] = Hallazgo(
            campo=campo,
            valor=h.get("valor"),
            estado=h.get("estado", SIN_VERIFICAR),
            fuente=Fuente(**fuente) if fuente else None,
            cita=h.get("cita", ""),
            confianza=h.get("confianza", "baja"),
            nota=h.get("nota", ""),
        )

    for p in d.get("pendientes") or []:
        dossier.pendientes.append(VerificacionPendiente(**p))

    interp = d.get("interpretacion")
    if interp:
        dossier.interpretacion = Interpretacion(**interp)

    return dossier
