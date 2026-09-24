"""
Veintiuno - investigacion_hotel · Configuracion y topes
=======================================================
Un sólo lugar para lo que se ajusta: modelo, presupuesto de la corrida, rutas
y los avisos fijos que van en todo documento.

Los topes no son una optimizacion de costo: son la garantia de que una corrida
termina. Al agotarse cualquiera, se renderiza lo que haya con las secciones
marcadas como incompletas. Nunca se falla dejando al usuario sin nada.
"""

import os
from pathlib import Path

# --- Modelo ---
MODELO = "claude-opus-5"
ESFUERZO_DEFAULT = "medium"  # low | medium | high
MAX_TOKENS = 16_000

# --- Topes de una corrida ---
MAX_BUSQUEDAS = 8  # busquedas web server-side
MAX_FETCHES = 12  # paginas que traemos nosotros
MAX_TURNOS = 24  # vueltas del loop agentico
MAX_REINICIOS_PAUSE_TURN = 5
TIMEOUT_TOTAL_S = 300  # reloj de pared de la corrida entera
TIMEOUT_HTTP_S = 15

# --- HTTP ---
# User-agent identificable: si un hotel mira sus logs, tiene que poder saber
# quien lo visito y por que. Es lo minimo decente de un scraper propio.
USER_AGENT = (
    "Veintiuno-investigacion/0.1 "
    "(prospeccion comercial; contacto: hernandezdionisiooscar@gmail.com)"
)
RESPETAR_ROBOTS = True

# --- Rutas ---
RAIZ = Path(__file__).resolve().parent.parent
SALIDA_DEFAULT = RAIZ / "salida_investigacion"
CACHE_DIR = Path(os.environ.get("VEINTIUNO_CACHE", RAIZ / ".cache_investigacion"))
CACHE_TTL_H = 24 * 7

# --- Fuentes fijas ---
# Dataset abierto del GCBA "Alojamientos Turisticos" (ver
# research/customer-acquisition.md). Solo cubre CABA: fuera de la Ciudad la
# herramienta corre en modo degradado y el dossier lo avisa en el encabezado.
URL_PADRON_GCBA = (
    "https://data.buenosaires.gob.ar/dataset/alojamientos-turisticos/"
    "resource/juqdkmgo-51-resource/download"
)

UBICACION_BUSQUEDA = {
    "type": "approximate",
    "country": "AR",
    "city": "Buenos Aires",
    "region": "Ciudad Autonoma de Buenos Aires",
}

# --- Avisos fijos ---
# Van en todo dossier interno, sin excepcion y sin flag que los saque.
BANNER_INTERNO = (
    "MATERIAL INTERNO DE VENTA - NO DISTRIBUIR\n"
    "Este documento es sobre un hotel identificable y se arma con fuentes públicas.\n"
    "No es un informe fiscal ni asesoramiento fiscal: prepara una conversación comercial.\n"
    "No compartir fuera de Veintiuno sin autorización escrita de Dionisio."
)

AVISO_BIN = (
    "El país emisor de la tarjeta (BIN) NO se ve desde afuera. Todo lo que figura "
    "abajo como señal de pago del exterior es eso, una señal: nunca una medición. "
    "La medición sale del cruce de reservas contra liquidación, y eso es la Radiografía."
)

AVISO_EXTERNO = (
    "Estimación preliminar hecha con datos públicos. Es gruesa y está sujeta a "
    "verificación. No constituye asesoramiento fiscal ni una promesa sobre el "
    "resultado de una fiscalización."
)
