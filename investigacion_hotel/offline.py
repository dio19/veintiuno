"""
Veintiuno - investigacion_hotel · Modo offline
==============================================
Corre el pipeline entero contra fixtures, sin tocar la red ni la API. Costo
cero, resultado determinístico.

Para que existe: iterar el prompt, el render y las validaciones sin gastar una
investigacion real en cada vuelta. Es el loop de todos los dias; la corrida
paga se reserva para cuando el documento ya tiene la forma que queremos.

El guion de abajo NO simula al modelo: llama a las mismas herramientas con las
mismas validaciones. Incluye a proposito un hallazgo con cita falsa, para que
el camino de rechazo se ejercite en cada corrida y no sólo en los tests.
"""

from contextlib import contextmanager
from pathlib import Path

from . import config
from .agente import Investigacion, Presupuesto
from .herramientas import sitio_hotel, web
from .modelo import Dossier

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "hotel_prueba"
URL_SITIO = "https://hotelpruebaveintiuno.test"
HOTEL = "Hotel Prueba Veintiuno"


@contextmanager
def fixtures_en_lugar_de_la_red():
    """Sirve el sitio del hotel ficticio en vez de salir a internet."""
    html = (FIXTURES / "sitio.html").read_text(encoding="utf-8")
    original = web.traer

    def traer_falso(url, **kw):
        if url.rstrip("/").startswith(URL_SITIO):
            return web.Respuesta(URL_SITIO, 200, html=html, texto=web.html_a_texto(html))
        return web.Respuesta(url, 0, error="modo offline: esa URL no está en los fixtures")

    web.traer = traer_falso
    sitio_hotel.web.traer = traer_falso
    try:
        yield
    finally:
        web.traer = original
        sitio_hotel.web.traer = original


def correr(presupuesto: Presupuesto | None = None) -> Dossier:
    """Ejecuta el guion completo y devuelve el dossier cerrado."""
    with fixtures_en_lugar_de_la_red():
        inv = Investigacion(
            HOTEL,
            "Buenos Aires",
            padron_local=str(FIXTURES / "padron.csv"),
            presupuesto=presupuesto or Presupuesto(),
        )

        inv.buscar_en_padron_gcba(HOTEL)
        padron = config.URL_PADRON_GCBA

        inv.registrar_hallazgo(
            "en_padron_gcba", "si", padron, "nombre: Hotel Prueba Veintiuno", "alta"
        )
        inv.registrar_hallazgo("categoria", "3 Estrellas", padron, "tipo: 3 Estrellas", "alta")
        inv.registrar_hallazgo(
            "domicilio", "AV. CALLAO 1234", padron, "direccion: AV. CALLAO 1234", "alta"
        )
        inv.registrar_hallazgo(
            "web", URL_SITIO, padron, "web: https://hotelpruebaveintiuno.test", "alta"
        )

        inv.leer_sitio(URL_SITIO)
        inv.registrar_hallazgo(
            "habitaciones",
            "38",
            URL_SITIO,
            "38 habitaciones en el corazón de Recoleta",
            "alta",
        )
        inv.registrar_hallazgo(
            "barrio",
            "Recoleta",
            URL_SITIO,
            "38 habitaciones en el corazón de Recoleta",
            "alta",
        )
        inv.registrar_hallazgo(
            "adr_publicado_ars",
            "115000",
            URL_SITIO,
            "Tarifas en pesos: ARS 115.000 la noche, IVA incluido",
            "media",
        )
        inv.registrar_hallazgo(
            "publica_precios_usd",
            "si",
            URL_SITIO,
            "Habitacion Standard desde USD 95 por noche",
            "alta",
        )
        inv.registrar_hallazgo(
            "menciona_exencion", "si", URL_SITIO, "may be eligible for a tax free rate", "alta"
        )
        inv.registrar_hallazgo(
            "sitio_en_ingles", "si", URL_SITIO, "International guests", "alta"
        )
        inv.registrar_hallazgo(
            "motor_reserva_propio", "si", URL_SITIO, "Reservar ahora", "alta"
        )
        inv.registrar_hallazgo(
            "pms_detectado", "Cloudbeds", URL_SITIO, "Reservar ahora", "media"
        )
        inv.registrar_hallazgo(
            "instagram", "@hotelpruebaveintiuno", URL_SITIO, "Instagram", "alta"
        )
        inv.registrar_hallazgo(
            "decisor_contacto",
            "reservas@hotelpruebaveintiuno.test",
            URL_SITIO,
            "reservas@hotelpruebaveintiuno.test",
            "media",
        )
        inv.registrar_hallazgo(
            "decisor_es_generico",
            "si",
            URL_SITIO,
            "reservas@hotelpruebaveintiuno.test",
            "alta",
        )
        inv.registrar_hallazgo(
            "es_cadena", "independiente", URL_SITIO, "Hotel Prueba Veintiuno", "baja"
        )

        # A proposito: una cita que NO esta en la pagina. Tiene que rebotar.
        inv.registrar_hallazgo(
            "responde_resenas",
            "si",
            URL_SITIO,
            "el hotel responde todas las reseñas en menos de 24 horas",
            "alta",
        )

        inv.pendiente(
            "pct_resenas_idioma_extranjero",
            "Que porcentaje de las últimas 30 reseñas está en inglés, portugués, "
            "francés o alemán?",
            "https://www.booking.com/",
            "vale 20 puntos del ICP y es el proxy central de no residentes",
        )

        inv.registrar_interpretacion(
            angulo_de_entrada=(
                "Ya menciona 'tax free' en la sección en inglés pero no dice "
                "factura T: o lo opera sin legajo, o lo promete y no lo cumple. "
                "Las dos son venta."
            ),
            objecion_esperada=(
                "'Eso lo maneja mi contador'. Respuesta: el legajo lo protege a el, "
                "por eso el contador es aliado y no obstaculo."
            ),
            proximo_paso="Mail al contacto publicado pidiendo el nombre del gerente.",
        )

        return inv.cerrar()
