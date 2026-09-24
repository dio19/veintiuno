"""
Veintiuno - investigacion_hotel · Calificacion del prospecto
============================================================
Codifica la checklist de 8 preguntas de business/ideal-customer.md: 100 puntos,
umbral 65 para Lista A y 45 para Lista B, más la regla dura que anula el puntaje.

El criterio comercial ya estaba decidido y escrito. Aca no se reinventa: se
traduce. Si cambia el criterio, cambia primero ideal-customer.md y despues está
tabla, nunca al reves.

Una pregunta sin dato verificado suma CERO, pero se cuenta aparte: no es lo
mismo un hotel que puntua 40 porque no califica que uno que puntua 40 porque no
encontramos la mitad de los datos. El segundo no se descarta, se completa.
"""

from dataclasses import dataclass, field

from .modelo import Dossier

UMBRAL_LISTA_A = 65
UMBRAL_LISTA_B = 45

# Pregunta 7 de la checklist. Los prioritarios son los del ICP; el resto de
# CABA puntua 4. "Perifericos" es nuestra definicion operativa para la regla
# dura: dentro de CABA pero fuera del corredor de receptivo.
BARRIOS_PRIORITARIOS = {
    "microcentro",
    "san nicolas",
    "retiro",
    "recoleta",
    "puerto madero",
    "palermo",
    "palermo soho",
    "palermo hollywood",
}
BARRIOS_CENTRICOS_SECUNDARIOS = {
    "congreso",
    "monserrat",
    "san telmo",
    "balvanera",
    "montserrat",
}

LISTA_A = "A"
LISTA_B = "B"
DESCARTAR = "descartar"
INDETERMINADO = "indeterminado"


@dataclass
class Respuesta:
    numero: int
    pregunta: str
    puntos: int
    maximo: int
    detalle: str
    evaluable: bool = True


@dataclass
class ResultadoScore:
    puntos: int = 0
    maximo_evaluable: int = 0  # 100 menos lo que no se pudo evaluar
    respuestas: list[Respuesta] = field(default_factory=list)
    lista: str = INDETERMINADO
    motivo_lista: str = ""
    sin_datos: list[str] = field(default_factory=list)

    @property
    def puntos_no_evaluables(self) -> int:
        return 100 - self.maximo_evaluable


def _normalizar_barrio(barrio: str | None) -> str:
    if not barrio:
        return ""
    limpio = (
        barrio.lower()
        .strip()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
    )
    return limpio


def _p1_resenas(d: Dossier) -> Respuesta:
    pct = d.valor("pct_resenas_idioma_extranjero")
    muestra = d.valor("muestra_resenas")
    if pct is None:
        return Respuesta(
            1,
            "% de reseñas en idioma extranjero",
            0,
            20,
            "sin dato verificado",
            evaluable=False,
        )
        # El tamano de muestra viaja siempre pegado al porcentaje: 3 de 5 resenas
        # no es lo mismo que 15 de 30, y presentarlos igual es inflar el dato.
    sufijo = f" (muestra: {muestra})" if muestra else " (muestra sin precisar)"
    if pct >= 50:
        return Respuesta(
            1, "% de reseñas en idioma extranjero", 20, 20, f"{pct:.0f}%{sufijo}"
        )
    if pct >= 25:
        return Respuesta(
            1, "% de reseñas en idioma extranjero", 10, 20, f"{pct:.0f}%{sufijo}"
        )
    return Respuesta(1, "% de reseñas en idioma extranjero", 0, 20, f"{pct:.0f}%{sufijo}")


def _p2_habitaciones(d: Dossier) -> Respuesta:
    n = d.valor("habitaciones")
    if n is None:
        return Respuesta(
            2, "Cantidad de habitaciones", 0, 10, "sin dato verificado", evaluable=False
        )
    if 25 <= n <= 90:
        return Respuesta(2, "Cantidad de habitaciones", 10, 10, f"{n} habitaciones")
    if 15 <= n <= 24 or 91 <= n <= 150:
        return Respuesta(2, "Cantidad de habitaciones", 5, 10, f"{n} habitaciones")
    return Respuesta(2, "Cantidad de habitaciones", 0, 10, f"{n} habitaciones")


def _p3_cadena(d: Dossier) -> Respuesta:
    v = d.valor("es_cadena")
    if v is None:
        return Respuesta(
            3, "Independiente o de cadena", 0, 15, "sin dato verificado", evaluable=False
        )
    tabla = {"independiente": 15, "cadena_local": 8, "cadena_internacional": 0}
    return Respuesta(3, "Independiente o de cadena", tabla.get(v, 0), 15, v)


def _p4_decisor(d: Dossier) -> Respuesta:
    nombre = d.valor("decisor_nombre")
    contacto = d.valor("decisor_contacto")
    generico = d.valor("decisor_es_generico")
    if nombre and contacto and not generico:
        return Respuesta(
            4,
            "Decisor con nombre y contacto directo",
            15,
            15,
            f"{nombre} - {d.valor('decisor_rol')or 'rol sin precisar'}",
        )
    if contacto or generico:
        return Respuesta(
            4, "Decisor con nombre y contacto directo", 6, 15, "sólo contacto genérico"
        )
    if nombre:
        return Respuesta(
            4,
            "Decisor con nombre y contacto directo",
            6,
            15,
            f"{nombre}, sin via de contacto publicada",
        )
    return Respuesta(
        4,
        "Decisor con nombre y contacto directo",
        0,
        15,
        "sin dato verificado",
        evaluable=False,
    )


def _p5_sitio(d: Dossier) -> Respuesta:
    ingles = d.valor("sitio_en_ingles")
    motor = d.valor("motor_reserva_propio")
    if ingles is None and motor is None:
        return Respuesta(
            5,
            "Sitio en inglés y motor de reserva propio",
            0,
            10,
            "sin dato verificado",
            evaluable=False,
        )
    tiene = sum(1 for x in (ingles, motor) if x is True)
    detalle = f"inglés: {_si_no(ingles)} · motor propio: {_si_no(motor)}"
    return Respuesta(
        5,
        "Sitio en inglés y motor de reserva propio",
        {2: 10, 1: 5}.get(tiene, 0),
        10,
        detalle,
    )


def _p6_adr(d: Dossier) -> Respuesta:
    adr = d.valor("adr_publicado_ars")
    if adr is None:
        return Respuesta(
            6, "ADR publicado en fecha alta", 0, 10, "sin dato verificado", evaluable=False
        )
    if adr >= 70_000:
        return Respuesta(
            6, "ADR publicado en fecha alta", 10, 10, f"ARS {adr:,.0f}".replace(",", ".")
        )
    if adr >= 45_000:
        return Respuesta(
            6, "ADR publicado en fecha alta", 5, 10, f"ARS {adr:,.0f}".replace(",", ".")
        )
    return Respuesta(
        6, "ADR publicado en fecha alta", 0, 10, f"ARS {adr:,.0f}".replace(",", ".")
    )


def _p7_ubicacion(d: Dossier) -> Respuesta:
    barrio = _normalizar_barrio(d.valor("barrio"))
    if not barrio:
        return Respuesta(
            7,
            "Ubicación en el corredor de receptivo",
            0,
            10,
            "sin dato verificado",
            evaluable=False,
        )
    if barrio in BARRIOS_PRIORITARIOS:
        return Respuesta(7, "Ubicación en el corredor de receptivo", 10, 10, barrio)
    return Respuesta(7, "Ubicación en el corredor de receptivo", 4, 10, barrio)


def _p8_senal_exencion(d: Dossier) -> Respuesta:
    exencion = d.valor("menciona_exencion")
    usd = d.valor("publica_precios_usd")
    if exencion is None and usd is None:
        return Respuesta(
            8,
            "Menciona exención o publica en USD",
            0,
            10,
            "sin dato verificado",
            evaluable=False,
        )
    if exencion is True:
        # Doble lectura, y las dos son venta: o ya lo opera y le falta el
        # legajo, o lo promete y no lo cumple.
        return Respuesta(
            8, "Menciona exención o publica en USD", 10, 10, "menciona la exención"
        )
    if usd is True:
        return Respuesta(
            8, "Menciona exención o publica en USD", 5, 10, "publica precios en USD"
        )
    return Respuesta(8, "Menciona exención o publica en USD", 0, 10, "ninguna señal")


def _si_no(v) -> str:
    return "sin dato" if v is None else ("sí" if v else "no")


def calificar(d: Dossier) -> ResultadoScore:
    """Aplica la checklist completa y devuelve el desglose pregunta por pregunta."""
    respuestas = [
        f(d)
        for f in (
            _p1_resenas,
            _p2_habitaciones,
            _p3_cadena,
            _p4_decisor,
            _p5_sitio,
            _p6_adr,
            _p7_ubicacion,
            _p8_senal_exencion,
        )
    ]
    puntos = sum(r.puntos for r in respuestas)
    maximo = sum(r.maximo for r in respuestas if r.evaluable)
    sin_datos = [r.pregunta for r in respuestas if not r.evaluable]

    res = ResultadoScore(
        puntos=puntos, maximo_evaluable=maximo, respuestas=respuestas, sin_datos=sin_datos
    )

    p1 = respuestas[0]
    pct = d.valor("pct_resenas_idioma_extranjero")
    barrio = _normalizar_barrio(d.valor("barrio"))
    periferico = bool(barrio) and (
        barrio not in BARRIOS_PRIORITARIOS and barrio not in BARRIOS_CENTRICOS_SECUNDARIOS
    )

    # Regla dura de ideal-customer.md: sin extranjeros no hay producto, y
    # anula el puntaje aunque sume 60.
    if pct is not None and pct < 25 and periferico:
        res.lista = DESCARTAR
        res.motivo_lista = (
            f"Regla dura: {pct:.0f}% de resenas en idioma extranjero "
            f"(<25%) y barrio fuera del corredor ({barrio}). "
            f"Se descarta aunque sume {puntos}."
        )
        return res

        # Sin la pregunta 1 no hay calificacion posible: es el proxy de todo lo
        # demas. Y si falta demasiado, el numero no es comparable contra otro hotel.
    if not p1.evaluable:
        res.lista = INDETERMINADO
        res.motivo_lista = (
            "Falta el dato de idioma de las reseñas, que es el proxy "
            "central del ICP. Sin eso el puntaje no califica nada."
        )
        return res
    if res.puntos_no_evaluables > 30:
        res.lista = INDETERMINADO
        res.motivo_lista = (
            f"Quedaron {res.puntos_no_evaluables} puntos sin poder evaluar "
            f"({len(sin_datos )} preguntas sin dato): el puntaje no es "
            f"comparable contra otro hotel hasta completarlas."
        )
        return res

    if puntos >= UMBRAL_LISTA_A:
        res.lista = LISTA_A
        res.motivo_lista = (
            f"{puntos}/100: se produce la estimación preliminar y se contacta esta semana."
        )
    elif puntos >= UMBRAL_LISTA_B:
        res.lista = LISTA_B
        res.motivo_lista = f"{puntos}/100: contacto masivo, sin estimacion personalizada."
    else:
        res.lista = DESCARTAR
        res.motivo_lista = f"{puntos}/100: por debajo de {UMBRAL_LISTA_B}, no se toca."
    return res
