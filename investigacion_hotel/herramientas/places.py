"""
Veintiuno - investigacion_hotel · Google Places (opcional)
==========================================================
Fuente legitima y estable para rating, cantidad de reseñas y -lo que de verdad
nos importa- el IDIOMA de las reseñas, que es el proxy central del ICP.

El límite que hay que tener presente y decir siempre: Place Details devuelve
como maximo 5 reseñas, no 30. El porcentaje que sale de acá es sobre una
muestra chica, y por eso `muestra_resenas` viaja siempre pegado al porcentaje.
Presentar "60% de las reseñas en inglés" callando que fueron 3 de 5 es
exactamente el tipo de número inflado que este proyecto no produce.

Requiere clave propia con facturacion (GOOGLE_PLACES_API_KEY). Sin clave, la
herramienta no se ofrece al agente.
"""

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field

from .. import config
from . import web

ENDPOINT = "https://places.googleapis.com/v1/places:searchText"

CAMPOS_PEDIDOS = ",".join(
    [
        "places.id",
        "places.displayName",
        "places.formattedAddress",
        "places.rating",
        "places.userRatingCount",
        "places.websiteUri",
        "places.nationalPhoneNumber",
        "places.googleMapsUri",
        "places.reviews",
    ]
)

# Idiomas que cuentan como huesped no residente. El castellano no: puede ser
# argentino, o puede ser un chileno pagando en pesos. El portugues suma al
# conteo pero se avisa aparte, porque Brasil paga mucho con tarjeta local.
IDIOMAS_EXTRANJEROS = {"en", "pt", "fr", "de", "it", "nl", "ru", "ja", "zh", "he", "ko"}
IDIOMAS_A_DESCONTAR = {"pt"}


@dataclass
class ResultadoPlaces:
    encontrado: bool = False
    error: str = ""
    nombre: str = ""
    direccion: str = ""
    rating: float | None = None
    total_resenas: int | None = None
    web: str = ""
    telefono: str = ""
    url_maps: str = ""
    idiomas: list = field(default_factory=list)
    muestra: int = 0
    pct_extranjero: float | None = None
    aviso: str = ""


def hay_clave() -> bool:
    return bool(os.environ.get("GOOGLE_PLACES_API_KEY"))


def _pedir(nombre: str, ciudad: str, clave: str) -> tuple:
    cuerpo = json.dumps(
        {"textQuery": f"{nombre}, {ciudad}", "maxResultCount": 1, "languageCode": "es"}
    ).encode("utf-8")
    pedido = urllib.request.Request(
        ENDPOINT,
        data=cuerpo,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": clave,
            "X-Goog-FieldMask": CAMPOS_PEDIDOS,
            "User-Agent": config.USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(
            pedido, timeout=config.TIMEOUT_HTTP_S, context=web._contexto_ssl()
        ) as resp:
            return json.loads(resp.read().decode("utf-8")), ""
    except urllib.error.HTTPError as e:
        detalle = e.read().decode("utf-8", errors="replace")[:200]
        return None, f"HTTP {e.code}: {detalle}"
    except Exception as e:
        return None, f"{type(e ).__name__}: {e}"


def interpretar(payload: dict) -> ResultadoPlaces:
    """Separado del pedido HTTP para poder testearlo contra un fixture."""
    lugares = (payload or {}).get("places") or []
    if not lugares:
        return ResultadoPlaces(error="sin resultados para ese nombre y ciudad")

    p = lugares[0]
    r = ResultadoPlaces(
        encontrado=True,
        nombre=(p.get("displayName") or {}).get("text", ""),
        direccion=p.get("formattedAddress", ""),
        rating=p.get("rating"),
        total_resenas=p.get("userRatingCount"),
        web=p.get("websiteUri", ""),
        telefono=p.get("nationalPhoneNumber", ""),
        url_maps=p.get("googleMapsUri", ""),
    )

    resenas = p.get("reviews") or []
    idiomas = []
    for resena in resenas:
        codigo = (
            (resena.get("originalText") or {}).get("languageCode")
            or resena.get("languageCode")
            or ""
        )
        if codigo:
            idiomas.append(codigo.split("-")[0].lower())

    r.idiomas = idiomas
    r.muestra = len(idiomas)
    if not idiomas:
        r.aviso = "Places no devolvio reseñas con idioma: el proxy sigue sin resolverse."
        return r

    extranjeras = [i for i in idiomas if i in IDIOMAS_EXTRANJEROS]
    r.pct_extranjero = round(100 * len(extranjeras) / len(idiomas), 1)

    avisos = [
        f"Muestra de {r.muestra} resenas, no 30: Place Details devuelve hasta 5. "
        f"Tomalo como indicio."
    ]
    if r.total_resenas:
        avisos.append(f"El hotel tiene {r.total_resenas} resenas en total.")
    if any(i in IDIOMAS_A_DESCONTAR for i in extranjeras):
        avisos.append(
            "Hay reseñas en portugués: Brasil paga mucho en pesos o con "
            "tarjeta local, así que ese tramo hay que descontarlo."
        )
    r.aviso = " ".join(avisos)
    return r


def consultar(nombre: str, ciudad: str) -> ResultadoPlaces:
    clave = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not clave:
        return ResultadoPlaces(error="falta GOOGLE_PLACES_API_KEY")
    payload, error = _pedir(nombre, ciudad, clave)
    if error:
        return ResultadoPlaces(error=error)
    return interpretar(payload)
