"""
Veintiuno - investigacion_hotel · Dossier interno
=================================================
El documento que lee Dionisio antes de decidir si toca la puerta de este hotel.
Lleva TODO: el puntaje, el decisor, la competencia, las objeciones. Por eso
mismo no sale de Veintiuno sin autorización, y el banner lo dice arriba de todo.

Regla del render: cada dato del hotel sale con su nota al pie o con la marca
SIN VERIFICAR. No hay tercera opcion, y no existe un camino en este archivo que
imprima un valor pelado.
"""

from pathlib import Path

from .. import config
from ..modelo import Dossier, CAMPOS, FUERA_DE_ALCANCE, SIN_VERIFICAR, OBSERVADO
from ..scoring import INDETERMINADO
from .comun import IndiceDeFuentes, pesos, rango_pesos

# Orden de presentacion. Agrupa como se lee, no como esta en CAMPOS.
BLOQUES = [
    (
        "Identificación",
        ["nombre_oficial", "domicilio", "barrio", "categoria", "en_padron_gcba", "web"],
    ),
    ("Tamaño y estructura", ["habitaciones", "es_cadena"]),
    (
        "Huéspedes (proxy de no residentes)",
        ["pct_resenas_idioma_extranjero", "muestra_resenas", "nacionalidades_predominantes"],
    ),
    (
        "Señales de pago del exterior",
        ["publica_precios_usd", "moneda_motor_reserva", "menciona_exencion"],
    ),
    ("Canal de venta", ["adr_publicado_ars", "motor_reserva_propio", "pms_detectado"]),
    ("Presencia online", ["sitio_en_ingles", "instagram", "responde_resenas"]),
    ("Decisor", ["decisor_nombre", "decisor_rol", "decisor_contacto", "decisor_es_generico"]),
    ("Entorno", ["competencia"]),
]


def render_interno(d: Dossier) -> str:
    idx = IndiceDeFuentes(d)
    L = []
    esc = L.append

    # -- Encabezado --
    esc(f"# Dossier · {d.hotel_consultado}")
    esc("")
    esc("> " + config.BANNER_INTERNO.replace("\n", "\n> "))
    esc("")
    esc(f"Generado: {d.generado} · Ciudad: {d.ciudad}")
    if d.modo_degradado:
        esc("")
        esc(
            "**MODO DEGRADADO**: el padron abierto del GCBA sólo cubre CABA. Fuera de la "
            "Ciudad no hubo fuente oficial que confirme que el alojamiento existe y está "
            "registrado, así que todo lo de abajo sale de fuentes secundarias."
        )
    if d.secciones_incompletas:
        esc("")
        esc(
            f"**CORRIDA INCOMPLETA**: se agoto el presupuesto antes de cerrar "
            f"{', '.join(d.secciones_incompletas )}. Lo que falta esta listado en "
            f"'Verificacion pendiente'."
        )

        # -- Veredicto --
    esc("")
    esc("## Veredicto")
    esc("")
    if d.score is None:
        esc(f"{SIN_VERIFICAR}: no se pudo calificar.")
    else:
        s = d.score
        etiqueta = {
            "A": "Lista A",
            "B": "Lista B",
            "descartar": "Descartar",
            INDETERMINADO: "Indeterminado",
        }.get(s.lista, s.lista)
        if s.puntos_no_evaluables:
            esc(
                f"**{etiqueta}** — {s.puntos} puntos sobre los {s.maximo_evaluable} "
                f"que se pudieron evaluar (de 100 posibles)"
            )
        else:
            esc(f"**{etiqueta}** — {s.puntos}/100")
        esc("")
        esc(s.motivo_lista)
        if s.sin_datos:
            esc("")
            esc(
                f"Sin dato para {len(s.sin_datos )} de 8 preguntas: "
                + "; ".join(s.sin_datos)
                + "."
            )

            # -- Calificacion --
    if d.score is not None:
        esc("")
        esc("## Calificación — las 8 preguntas de `business/ideal-customer.md`")
        esc("")
        esc("| # | Pregunta | Puntos | Detalle |")
        esc("|---|---|---|---|")
        for r in d.score.respuestas:
            puntos = f"{r.puntos}/{r.maximo}" if r.evaluable else f"— /{r.maximo}"
            esc(f"| {r.numero} | {r.pregunta} | {puntos} | {r.detalle} |")

            # -- Lo que sabemos --
    esc("")
    esc("## Qué sabemos del hotel")
    esc("")
    for titulo, campos in BLOQUES:
        presentes = [c for c in campos if c in d.hallazgos]
        if not presentes:
            continue
        esc(f"### {titulo}")
        esc("")
        esc("| Campo | Valor | Fuente | Cita |")
        esc("|---|---|---|---|")
        for campo in presentes:
            h = d.hallazgo(campo)
            cita = (h.cita or "").replace("|", "/")[:110]
            esc(
                f"| {CAMPOS[campo ].descripcion} | {h.como_texto()} "
                f"| {idx.marca(h )} | {cita if h.verificado else ''} |"
            )
        esc("")

        # -- Estimacion --
    esc("## IVA en juego — estimación preliminar")
    esc("")
    if d.estimacion is None:
        esc(f"{SIN_VERIFICAR}: no se calculó.")
    else:
        e = d.estimacion
        esc(f"*{e.que_mide}*")
        esc("")
        if e.hay_numero:
            esc(f"**Por mes: {rango_pesos(e.rango_iva_mensual_estimado_ars )}**")
            esc("")
            esc(f"Anualizado: {rango_pesos(e.rango_iva_anualizado_estimado_ars )}")
        else:
            esc(f"**Sin numero.** {e.motivo_sin_numero}")
        esc("")
        esc("| Insumo | Valor | Procedencia | Fundamento |")
        esc("|---|---|---|---|")
        for i in e.insumos:
            if i.valor is None:
                valor = SIN_VERIFICAR
            elif isinstance(i.valor, tuple):
                valor = f"{i.valor[0 ]:.0%} a {i.valor[1 ]:.0%}"
            elif i.unidad == "ARS":
                valor = pesos(i.valor)
            elif i.unidad == "%":
                valor = f"{i.valor:g}%"
            else:
                valor = f"{i.valor:g} {i.unidad}".strip()
                # Un insumo observado se respalda con la misma nota al pie que el
                # hallazgo del que salio: sin eso, la tabla de la estimacion muestra
                # un numero cuyo origen hay que ir a buscar a otra seccion.
            marca = idx.marca(d.hallazgo(i.campo)) if i.campo else ""
            respaldo = f"{i.procedencia} {marca}".strip() if marca else i.procedencia
            esc(f"| {i.nombre} | {valor} | {respaldo} | {i.fundamento} |")
        for a in e.advertencias:
            esc("")
            esc(f"> {a}")

            # -- Limites --
    esc("")
    esc("## Lo que este dossier NO puede responder")
    esc("")
    esc(config.AVISO_BIN)
    esc("")
    for item in FUERA_DE_ALCANCE:
        esc(f"- {item}")
    esc("")
    esc(
        "Todo eso sale del cruce de reservas contra liquidación de la pasarela, "
        "es decir, de la Radiografía del 21%. Este documento prepara esa conversación; "
        "no la reemplaza ni la anticipa."
    )

    # -- Pendientes --
    esc("")
    esc("## Verificación pendiente")
    esc("")
    if not d.pendientes:
        esc("Nada pendiente.")
    else:
        esc(
            "Dos minutos a mano cierran cada uno de estos. Se responden editando "
            "`dossier.json` y volviendo a correr con `--rehacer`, sin costo de API."
        )
        esc("")
        for p in d.pendientes:
            esc(f"- **{p.campo}** — {p.pregunta}")
            if p.url:
                esc(f"  - {p.url}")
            if p.porque:
                esc(f"  - por qué importa: {p.porque}")

                # -- Interpretacion --
    esc("")
    esc("## Interpretación")
    esc("")
    esc(
        "*Esto es lectura del agente sobre cómo entrar, no un dato sobre el hotel. "
        "Se discute; no se cita.*"
    )
    esc("")
    if d.interpretacion is None:
        esc(SIN_VERIFICAR)
    else:
        i = d.interpretacion
        esc(f"- **Angulo de entrada:** {i.angulo_de_entrada or SIN_VERIFICAR}")
        esc(f"- **Objecion esperada:** {i.objecion_esperada or SIN_VERIFICAR}")
        esc(f"- **Proximo paso:** {i.proximo_paso or SIN_VERIFICAR}")

        # -- Fuentes --
    esc("")
    esc("## Fuentes")
    esc("")
    listado = idx.listado(d)
    if listado:
        L.extend(listado)
    else:
        esc("Ninguna fuente resoluble. Todo el dossier está SIN VERIFICAR.")

    if d.consumo:
        esc("")
        esc("## Consumo de la corrida")
        esc("")
        for k, v in d.consumo.items():
            esc(f"- {k}: {v}")

    return "\n".join(L) + "\n"


def escribir_interno(d: Dossier, carpeta) -> Path:
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / "dossier.md"
    ruta.write_text(render_interno(d), encoding="utf-8")
    return ruta
