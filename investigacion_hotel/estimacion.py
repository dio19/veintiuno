"""
Veintiuno - investigacion_hotel · Estimacion preliminar del IVA en juego
========================================================================
Aritmetica gruesa sobre señales públicas. NO es la Radiografia.

La diferencia no es de precision, es de naturaleza: la Radiografia mide estadia
por estadia sobre el export del hotel y resuelve el pais emisor de la tarjeta
por BIN. Esto estima un rango a partir de lo que se ve desde afuera, donde el
BIN es invisible. Por eso los campos de salida se llaman distinto a proposito
(rango_iva_mensual_estimado_ars, nunca iva_en_juego) y este modulo no importa
nada del motor: que nadie pueda confundir un supuesto con una medición.

Regla de la casa: si falta alguno de los insumos observables, NO se emite
número. Se dice cual falta. Un rango inventado sobre tres supuestos encadenados
no resiste la primera pregunta del hotelero, que si conoce sus números.
"""

from dataclasses import dataclass, field

from .modelo import Dossier, SIN_VERIFICAR, OBSERVADO, SUPUESTO

IVA = 0.21

# QUE MIDE ESTE NUMERO, y por que la distincion no es un detalle de redaccion.
# El rango es el IVA EN JUEGO: el impuesto sobre las estadias que PODRIAN
# encuadrar en el regimen. No es plata perdida. Parte de eso el hotel quiza ya
# lo factura bien. Que porcion se esta fugando de verdad es justamente lo que
# mide la Radiografia sobre el export, y para hoteles reales es la hipotesis 1
# del README, todavia sin validar. Presentar esto como "lo que perdes por mes"
# es inflar el numero y perder la reunion apenas el hotelero abra su propio PMS.
QUE_MIDE = (
    "IVA en juego: el impuesto sobre las estadías que podrían encuadrar en "
    "el régimen de exención. NO es la fuga: qué porción se está facturando "
    "mal sólo lo dice la Radiografía sobre el export del hotel."
)

# Quitar el IVA de un precio final es -17,36%, no -21%. Regla de bolsillo:
# dividir la tarifa por 1,21.
DESCUENTO_EXENCION = 1 - 1 / (1 + IVA)

DIAS_MES = 30

# Supuestos por default, cada uno con su fundamento escrito. Se imprimen en el
# documento al lado del numero: un supuesto que no se ve es una mentira.
SUPUESTO_OCUPACION = (0.50, 0.65)
FUENTE_OCUPACION = (
    "Ocupación general de CABA ~65% en julio 2026; los 2-3 estrellas "
    "entre 45-50%. Ver README.md y research/customer-acquisition.md."
)

SUPUESTO_PAGO_EXTERIOR = (0.35, 0.55)
FUENTE_PAGO_EXTERIOR = (
    "Proporción de huéspedes no residentes que paga con tarjeta "
    "emitida en el exterior o transferencia del exterior. "
    f"{SIN_VERIFICAR}: la corrida de la demo dio ~50%, pero es un "
    "supuesto del generador sintético, no un dato de campo. Es "
    "exactamente la hipótesis 1 del README, todavía sin validar."
)

# Paises cuyos huespedes pagan mucho en pesos o con tarjeta local. No lo
# cuantificamos (no tenemos con que): se avisa y listo.
PAISES_A_DESCONTAR = {"brasil", "br", "chile", "cl"}


@dataclass
class Insumo:
    nombre: str
    valor: float | tuple | None
    procedencia: str  # observado | supuesto | SIN VERIFICAR
    fundamento: str = ""
    unidad: str = ""
    campo: str = ""  # campo del dossier del que salio, si es observado

    @property
    def falta(self) -> bool:
        return self.procedencia == SIN_VERIFICAR


@dataclass
class ResultadoEstimacion:
    que_mide: str = QUE_MIDE
    hay_numero: bool = False
    motivo_sin_numero: str = ""
    rango_iva_mensual_estimado_ars: tuple | None = None
    rango_iva_anualizado_estimado_ars: tuple | None = None
    insumos: list[Insumo] = field(default_factory=list)
    advertencias: list[str] = field(default_factory=list)

    @property
    def faltantes(self) -> list[str]:
        return [i.nombre for i in self.insumos if i.falta]


def quitar_iva(precio_final: float) -> float:
    """Precio exento a partir de un precio final con IVA. Es dividir por 1,21."""
    return precio_final / (1 + IVA)


def _redondear(valor: float, paso: int = 10_000) -> int:
    """Redondea al paso indicado. Un rango terminado en 1.234.567 finge una
    precisión que esta cuenta no tiene."""
    return int(round(valor / paso) * paso)


def estimar(d: Dossier) -> ResultadoEstimacion:
    """Rango de IVA mensual en juego, o la explicacion de por que no se puede.

    IVA mensual = habitaciones x 30 x ocupacion x %extranjero x %pago exterior
                  x (ADR / 1,21) x 0,21
    """
    habitaciones = d.valor("habitaciones")
    adr = d.valor("adr_publicado_ars")
    pct_extranjero = d.valor("pct_resenas_idioma_extranjero")
    muestra = d.valor("muestra_resenas")

    insumos = [
        Insumo(
            "habitaciones",
            habitaciones,
            OBSERVADO if habitaciones is not None else SIN_VERIFICAR,
            "Cantidad de habitaciones publicada",
            "hab",
            "habitaciones",
        ),
        Insumo(
            "ADR publicado con IVA",
            adr,
            OBSERVADO if adr is not None else SIN_VERIFICAR,
            "Tarifa por noche publicada en fecha alta",
            "ARS",
            "adr_publicado_ars",
        ),
        Insumo(
            "proporción de huéspedes no residentes",
            pct_extranjero,
            OBSERVADO if pct_extranjero is not None else SIN_VERIFICAR,
            (
                "Proxy: idioma de las reseñas públicas"
                + (
                    f", sobre una muestra de {muestra}"
                    if muestra
                    else ", muestra sin precisar"
                )
                + ". No es la mezcla real de nacionalidades del PMS."
            ),
            "%",
            "pct_resenas_idioma_extranjero",
        ),
        Insumo("ocupación", SUPUESTO_OCUPACION, SUPUESTO, FUENTE_OCUPACION, "%"),
        Insumo(
            "pago desde el exterior",
            SUPUESTO_PAGO_EXTERIOR,
            SUPUESTO,
            FUENTE_PAGO_EXTERIOR,
            "%",
        ),
    ]

    res = ResultadoEstimacion(insumos=insumos)
    faltan = [i.nombre for i in insumos if i.falta]
    if faltan:
        if len(faltan) >= 2:
            res.motivo_sin_numero = (
                f"Faltan {len(faltan )} insumos observables ({', '.join(faltan )}). "
                "Con dos o más sin verificar, cualquier rango sería una invención "
                "encadenada: no se emite número."
            )
        else:
            res.motivo_sin_numero = (
                f"Falta un insumo observable: {faltan[0 ]}. Se resuelve mirando el "
                "sitio del hotel o su ficha en una OTA; hasta entonces no se emite número."
            )
        return res

        # Advertencia sin cuantificar: no tenemos con que ponerle un numero al
        # descuento, asi que se avisa en vez de inventar un coeficiente.
    nacionalidades = d.valor("nacionalidades_predominantes") or []
    if any(str(n).strip().lower() in PAISES_A_DESCONTAR for n in nacionalidades):
        res.advertencias.append(
            "Entre las nacionalidades predominantes hay Brasil o Chile, que pagan mucho "
            "en pesos o con tarjeta local. El rango de esta estimación está sobreestimado y no "
            f"sabemos cuánto: la magnitud del descuento es {SIN_VERIFICAR}."
        )

    if muestra and muestra < 10:
        res.advertencias.append(
            f"La proporcion de no residentes sale de una muestra de {muestra} resenas. "
            "Es poco: tomalo como indicio, no como medición."
        )

    neto = quitar_iva(adr)
    noches = habitaciones * DIAS_MES
    bajo = (
        noches
        * SUPUESTO_OCUPACION[0]
        * (pct_extranjero / 100)
        * SUPUESTO_PAGO_EXTERIOR[0]
        * neto
        * IVA
    )
    alto = (
        noches
        * SUPUESTO_OCUPACION[1]
        * (pct_extranjero / 100)
        * SUPUESTO_PAGO_EXTERIOR[1]
        * neto
        * IVA
    )

    res.hay_numero = True
    res.rango_iva_mensual_estimado_ars = (_redondear(bajo), _redondear(alto))
    res.rango_iva_anualizado_estimado_ars = (
        _redondear(bajo * 12, 100_000),
        _redondear(alto * 12, 100_000),
    )
    return res
