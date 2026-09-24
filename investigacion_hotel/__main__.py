"""
Veintiuno - investigacion_hotel · Linea de comandos
===================================================
Corre sola, sin sesion de Claude Code.

    python3 -m investigacion_hotel --nombre "Hotel X" --ciudad "Buenos Aires"

Necesita ANTHROPIC_API_KEY para una corrida real. `--offline` no la necesita:
corre el pipeline entero contra fixtures, gratis y determinístico.
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

from . import config
from .estimacion import estimar
from .modelo import dossier_desde_dict
from .render import escribir_interno, escribir_externo
from .scoring import calificar


def slug(texto: str) -> str:
    sin_acentos = "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )
    return (
        re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", sin_acentos.lower())).strip("-")
        or "hotel"
    )


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="python3 -m investigacion_hotel",
        description="Investigacion comercial de un hotel prospecto para Veintiuno. "
        "Produce un dossier interno y, opcionalmente, la estimación de "
        "una página que se le manda al hotel.",
        epilog="La salida es material interno sobre un hotel identificable: no sale "
        "de Veintiuno sin autorización.",
    )
    p.add_argument("--nombre", help="Nombre del hotel prospecto")
    p.add_argument("--ciudad", default="Buenos Aires", help="Ciudad (default: Buenos Aires)")
    p.add_argument("--sitio", help="URL del sitio del hotel, si ya la conoces")
    p.add_argument(
        "--salida", help=f"Carpeta de salida (default: {config.SALIDA_DEFAULT}/<hotel>)"
    )
    p.add_argument(
        "--externo",
        action="store_true",
        help="Genera tambien la estimación preliminar de una página para el hotel",
    )
    p.add_argument(
        "--esfuerzo",
        choices=("low", "medium", "high"),
        default=config.ESFUERZO_DEFAULT,
        help="Esfuerzo del modelo",
    )
    p.add_argument(
        "--max-busquedas",
        type=int,
        default=config.MAX_BUSQUEDAS,
        help=f"Tope de busquedas web (default: {config.MAX_BUSQUEDAS})",
    )
    p.add_argument(
        "--max-fetches",
        type=int,
        default=config.MAX_FETCHES,
        help=f"Tope de paginas leidas (default: {config.MAX_FETCHES})",
    )
    p.add_argument("--padron", help="CSV propio del padron, en vez de bajarlo del GCBA")
    p.add_argument(
        "--offline",
        action="store_true",
        help="Corre contra fixtures: sin red, sin API, sin costo",
    )
    p.add_argument(
        "--rehacer",
        metavar="DIR",
        help="Vuelve a armar los documentos desde un dossier.json ya guardado, "
        "sin llamar a la API. Es como se cierran las verificaciones "
        "pendientes: editas el JSON y rehaces.",
    )
    return p.parse_args(argv)


def escribir(d, carpeta: Path, externo: bool) -> list:
    carpeta.mkdir(parents=True, exist_ok=True)
    escritos = [escribir_interno(d, carpeta)]

    ruta_json = carpeta / "dossier.json"
    ruta_json.write_text(
        json.dumps(d.a_dict(), ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    escritos.append(ruta_json)

    if externo:
        escritos.append(escribir_externo(d, carpeta))
    return escritos


def main(argv=None) -> int:
    args = parse_args(argv)

    if args.rehacer:
        carpeta = Path(args.rehacer)
        ruta = carpeta / "dossier.json"
        if not ruta.exists():
            print(f"No hay dossier.json en {carpeta}", file=sys.stderr)
            return 2
        d = dossier_desde_dict(json.loads(ruta.read_text(encoding="utf-8")))
        d.score = calificar(d)
        d.estimacion = estimar(d)
        escritos = escribir(d, carpeta, args.externo)
        print(f"Rehecho desde {ruta} (sin costo de API).")

    elif args.offline:
        from .agente import Presupuesto
        from .offline import correr

        d = correr(Presupuesto(max_busquedas=args.max_busquedas, max_fetches=args.max_fetches))
        carpeta = Path(args.salida) if args.salida else config.SALIDA_DEFAULT / "offline"
        escritos = escribir(d, carpeta, args.externo)
        print("Corrida OFFLINE contra fixtures: hotel ficticio, sin red, sin costo.")

    else:
        if not args.nombre:
            print("Falta --nombre (o usa --offline / --rehacer).", file=sys.stderr)
            return 2
        try:
            from .agente import Presupuesto, investigar
        except ImportError:
            print(
                "Falta el SDK: pip3 install -r investigacion_hotel/requirements.txt",
                file=sys.stderr,
            )
            return 3

        import os

        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("Falta ANTHROPIC_API_KEY. Para probar sin clave: --offline", file=sys.stderr)
            return 4

        presupuesto = Presupuesto(
            max_busquedas=args.max_busquedas, max_fetches=args.max_fetches
        )
        print(
            f"Investigando {args.nombre} ({args.ciudad})... "
            f"tope: {args.max_busquedas} busquedas, {args.max_fetches} lecturas."
        )
        d = investigar(
            args.nombre,
            args.ciudad,
            sitio=args.sitio,
            padron_local=args.padron,
            esfuerzo=args.esfuerzo,
            presupuesto=presupuesto,
        )
        carpeta = (
            Path(args.salida) if args.salida else config.SALIDA_DEFAULT / slug(args.nombre)
        )
        escritos = escribir(d, carpeta, args.externo)

        # -- Resumen por consola --
    print()
    if d.score is not None:
        print(
            f"  Veredicto: {d.score.lista} — {d.score.puntos}/{d.score.maximo_evaluable} "
            f"puntos evaluables"
        )
    verificados = sum(1 for h in d.hallazgos.values() if h.verificado)
    print(f"  Hallazgos: {verificados} verificados de {len(d.hallazgos )}")
    if d.estimacion is not None and d.estimacion.hay_numero:
        bajo, alto = d.estimacion.rango_iva_mensual_estimado_ars
        print(f"  IVA en juego estimado: ARS {bajo:,} a {alto:,}".replace(",", "."))
    elif d.estimacion is not None:
        print(f"  Sin estimación: {d.estimacion.motivo_sin_numero}")
    if d.pendientes:
        print(f"  Verificaciones pendientes: {len(d.pendientes )}")
    if d.consumo:
        print(f"  Consumo: {', '.join (f'{k} {v}'for k ,v in d .consumo .items ())}")
    print()
    for ruta in escritos:
        print(f"  -> {ruta}")

    print()
    print(
        "  Material interno sobre un hotel identificable. No sale de Veintiuno "
        "sin autorización."
    )
    if args.externo:
        print(
            "  El .md de estimación preliminar es lo ÚNICO de esta carpeta que "
            "puede verlo el hotel."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
