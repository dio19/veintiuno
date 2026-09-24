"""
Veintiuno - investigacion_hotel · Padron abierto del GCBA
=========================================================
Dataset "Alojamientos Turisticos" del portal de datos abiertos de la Ciudad
(ver research/customer-acquisition.md). Campos: nombre, domicilio, telefono,
email, web, tipo, calle, altura, direccion, Long, Lat.

Es la única fuente OFICIAL que tenemos de que un alojamiento existe y está
registrado. Por eso el hallazgo `en_padron_gcba` vale: no es una inferencia.

Solo cubre CABA. Fuera de la Ciudad esta herramienta no responde y la corrida
queda en modo degradado, que el dossier avisa en el encabezado.
"""

import csv
import difflib
import io
import re
import unicodedata

from .. import config
from . import web

_cache_filas: list | None = None

# Solo lo que de verdad no distingue nada. Ojo con sacar "hotel" y "hostel"
# de aca: dejarlos afuera hace que "Hotel Recoleta" y "Hostel Recoleta" queden
# identicos, y un hostel es anti-ICP, no el mismo prospecto escrito distinto.
PALABRAS_VACIAS = {"de", "del", "la", "el", "los", "las", "y", "sa", "srl", "s", "a"}

# Palabras que dicen el TIPO de alojamiento, no cual es. Sirven para comparar,
# pero un nombre que solo comparte estas no es una coincidencia.
PALABRAS_DE_TIPO = {
    "hotel",
    "hostel",
    "apart",
    "aparthotel",
    "hospedaje",
    "suites",
    "suite",
    "boutique",
    "residencia",
    "hosteria",
}


def normalizar(texto: str) -> str:
    """Minusculas, sin acentos, sin puntuacion. Para comparar nombres."""
    if not texto:
        return ""
    sin_acentos = "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"[^a-z0-9 ]", " ", sin_acentos.lower()).strip()


def _tokens(texto: str) -> set:
    return {t for t in normalizar(texto).split() if t and t not in PALABRAS_VACIAS}


def _distintivos(texto: str) -> set:
    """Tokens que identifican a ESTE alojamiento, sin las palabras de tipo."""
    return _tokens(texto) - PALABRAS_DE_TIPO


def cargar(ruta_local: str | None = None, forzar: bool = False) -> tuple:
    """Devuelve (filas, error). Cachea en memoria y en disco.

    `ruta_local` permite pasar una copia propia del CSV con --padron, sin tocar
    codigo, igual que --bin-map en el motor.
    """
    global _cache_filas
    if _cache_filas is not None and not forzar and not ruta_local:
        return _cache_filas, ""

    if ruta_local:
        try:
            with open(ruta_local, encoding="utf-8-sig", newline="") as f:
                filas = list(csv.DictReader(f))
        except OSError as e:
            return [], f"no se pudo leer {ruta_local}: {e}"
    else:
        r = web.traer(config.URL_PADRON_GCBA, usar_cache=not forzar, timeout=30)
        if not r.ok:
            return [], f"no se pudo bajar el padron del GCBA: {r.error or r.status}"
        try:
            filas = list(csv.DictReader(io.StringIO(r.html)))
        except csv.Error as e:
            return [], f"padron ilegible: {e}"

            # Normalizamos los nombres de columna: el portal cambia mayusculas entre
            # versiones (Long/long, Lat/lat) y no queremos que eso rompa una corrida.
    filas = [
        {(k or "").lstrip("\ufeff").strip().lower(): (v or "").strip() for k, v in f.items()}
        for f in filas
    ]
    if not ruta_local:
        _cache_filas = filas
    return filas, ""


def buscar(nombre: str, limite: int = 5, ruta_local: str | None = None) -> tuple:
    """Busca un alojamiento por nombre. Devuelve (coincidencias, error).

    Cada coincidencia trae `_similitud` (0 a 1). No decide sola cual es: si hay
    ambiguedad, se la pasa al agente para que la resuelva con otra señal
    (direccion, sitio web). Elegir en silencio el primer resultado es como se
    arma un dossier sobre el hotel equivocado.
    """
    filas, error = cargar(ruta_local)
    if error:
        return [], error

    buscado = _tokens(nombre)
    buscado_distintivo = _distintivos(nombre)
    if not buscado:
        return [], "nombre vacio"
    normalizado = normalizar(nombre)
    tipo_buscado = _tokens(nombre) & PALABRAS_DE_TIPO

    puntuadas = []
    for fila in filas:
        candidato = fila.get("nombre", "")
        tokens = _tokens(candidato)
        if not tokens:
            continue

            # Sin al menos una palabra distintiva en comun no hay coincidencia.
            # Compartir "hotel" no es parecerse: sin este filtro, un nombre que no
            # esta en el padron devuelve igual media docena de candidatos plausibles.
        if buscado_distintivo and not (buscado_distintivo & _distintivos(candidato)):
            continue

        jaccard = len(buscado & tokens) / len(buscado | tokens)
        ratio = difflib.SequenceMatcher(None, normalizado, normalizar(candidato)).ratio()
        similitud = max(jaccard, ratio)
        if similitud < 0.45:
            continue

            # "Hotel X" y "Hostel X" se parecen en una letra y son prospectos
            # opuestos: el hostel es anti-ICP. La similitud textual no puede
            # resolverlo, asi que se avisa en vez de rankear en silencio.
        tipo_candidato = tokens & PALABRAS_DE_TIPO
        advertencia = ""
        if tipo_buscado and tipo_candidato and tipo_buscado != tipo_candidato:
            advertencia = (
                f"ojo: buscaste '{'/'.join(sorted(tipo_buscado ))}' y esto es "
                f"'{'/'.join(sorted(tipo_candidato ))}'"
            )
        puntuadas.append(
            {**fila, "_similitud": round(similitud, 3), "_advertencia": advertencia}
        )

    puntuadas.sort(key=lambda f: f["_similitud"], reverse=True)
    return puntuadas[:limite], ""
