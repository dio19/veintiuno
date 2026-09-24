"""
Veintiuno - investigacion_hotel · Estimacion preliminar (material externo)
==========================================================================
La única pieza que sale de Veintiuno y llega al hotel. Una página, hecha con
datos públicos, que se manda ANTES de pedir nada (ver business/outreach.md).

La diferencia con el dossier interno no es de tono, es de contenido: acá no
entra el puntaje, ni el nombre del decisor, ni la competencia, ni la objecion
que esperamos. Nada de eso es información del hotel: es nuestra evaluacion
comercial de el, y mandarsela por error quema el prospecto.

Como se hace cumplir: este modulo sólo puede leer campos marcados público=True
en modelo.CAMPOS. Pedir cualquier otro levanta CampoNoPublico. No hay una
segunda lista que se pueda desincronizar de la primera.
"""

from pathlib import Path

from .. import config, normativa
from ..modelo import Dossier, CAMPOS, SIN_VERIFICAR
from .comun import IndiceDeFuentes, pesos, rango_pesos


class CampoNoPublico(Exception):
    """Se intento poner un campo interno en material que va al hotel."""

    # Lo que se le muestra al hotel sobre si mismo: observaciones publicas que
    # justifican por que le escribimos. Todos tienen que ser publico=True.


CAMPOS_EXTERNOS = [
    "habitaciones",
    "pct_resenas_idioma_extranjero",
    "muestra_resenas",
    "nacionalidades_predominantes",
    "sitio_en_ingles",
    "publica_precios_usd",
    "menciona_exencion",
]

FRASES = {
    "pct_resenas_idioma_extranjero": "reseñas recientes en idioma extranjero",
    "muestra_resenas": "reseñas miradas para ese cálculo",
    "habitaciones": "habitaciones",
    "nacionalidades_predominantes": "origen más frecuente de los reseñadores",
    "sitio_en_ingles": "sitio con versión en inglés",
    "publica_precios_usd": "tarifas publicadas en dólares",
    "menciona_exencion": "menciona tax free / exención de IVA en sus canales",
}


def _verificar_lista_blanca():
    for campo in CAMPOS_EXTERNOS:
        spec = CAMPOS.get(campo)
        if spec is None:
            raise CampoNoPublico(f"campo inexistente en el modelo: {campo}")
        if not spec.publico:
            raise CampoNoPublico(
                f"'{campo}' no esta marcado publico=True en modelo.CAMPOS y no puede "
                f"salir en material que ve el hotel"
            )


def render_externo(d: Dossier) -> str:
    _verificar_lista_blanca()
    idx = IndiceDeFuentes(d, CAMPOS_EXTERNOS)
    L = []
    esc = L.append

    esc(f"# {d.hotel_consultado} — IVA de huéspedes no residentes")
    esc("")
    esc("Estimación preliminar · Veintiuno")
    esc("")

    # -- Lo que vemos desde afuera --
    esc("## Lo que vemos desde afuera")
    esc("")
    observados = [
        c for c in CAMPOS_EXTERNOS if (h := d.hallazgo(c)) is not None and h.verificado
    ]
    if not observados:
        esc(
            f"{SIN_VERIFICAR}: no hay observaciones publicas verificadas. "
            "Este documento no debería mandarse así."
        )
    else:
        for campo in observados:
            h = d.hallazgo(campo)
            esc(f"- {FRASES[campo ]}: **{h.como_texto()}** {idx.marca(h )}")

            # -- El regimen --
    esc("")
    esc("## El régimen")
    esc("")
    esc(normativa.PARRAFO_PUBLICO)
    esc("")
    esc(
        f"Quitar el IVA de un precio final equivale a un "
        f"{str(normativa.DESCUENTO_EQUIVALENTE_PCT).replace('.', ',')}% menos de tarifa "
        f"mostrada, sin tocar el neto que cobra el hotel."
    )

    # -- La estimacion --
    esc("")
    esc("## Qué hay en juego, aproximadamente")
    esc("")
    e = d.estimacion
    if e is None or not e.hay_numero:
        esc(
            "No alcanzan los datos públicos para estimar un monto en este caso. "
            "El número exacto sale del cruce de reservas contra liquidación."
        )
    else:
        esc(f"**{rango_pesos(e.rango_iva_mensual_estimado_ars )} por mes.**")
        esc("")
        esc(e.que_mide)
        esc("")
        esc("Cómo se calcula, para que se pueda discutir:")
        esc("")
        for i in e.insumos:
            if isinstance(i.valor, tuple):
                valor = f"{i.valor[0 ]:.0%} a {i.valor[1 ]:.0%}"
            elif i.valor is None:
                valor = SIN_VERIFICAR
            elif i.unidad == "ARS":
                valor = pesos(i.valor)
            elif i.unidad == "%":
                valor = f"{i.valor:g}%"
            else:
                valor = f"{i.valor:g} {i.unidad}".strip()
            esc(f"- {i.nombre}: {valor} ({i.procedencia})")
        for a in e.advertencias:
            esc("")
            esc(f"> {a}")

            # -- Que sigue --
    esc("")
    esc("## Qué sigue")
    esc("")
    esc(
        "El cálculo exacto es la Radiografía del 21%: se cruza el export de reservas "
        "de los últimos 90 días contra la liquidación de la pasarela y sale, estadía "
        "por estadía, cuáles calificaban y cómo se facturaron. Sin cargo, en 48 horas "
        "desde que llega el export."
    )
    esc("")
    esc(
        "Trabajamos al lado del PMS, nunca contra: leemos sus exports, no pedimos "
        "integración."
    )

    # -- Limites --
    esc("")
    esc("---")
    esc("")
    esc(config.AVISO_EXTERNO)
    esc("")
    listado = idx.listado(d)
    if listado:
        esc("Fuentes de lo observado:")
        esc("")
        L.extend(listado)

    return "\n".join(L) + "\n"


def escribir_externo(d: Dossier, carpeta) -> Path:
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / "estimacion_preliminar.md"
    ruta.write_text(render_externo(d), encoding="utf-8")
    return ruta
