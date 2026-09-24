"""
Veintiuno - investigacion_hotel · Senales del sitio propio del hotel
====================================================================
Determinístico: no interviene el LLM. Se trae el HTML y se buscan huellas
concretas. Cada señal viaja con la CITA que la justifica, porque despues se
convierte en un Hallazgo y un Hallazgo sin cita no vale.

Que se mirá y por que (ver business/ideal-customer.md):
  - versión en inglés real -> alguien decidio invertir en el mercado externo
  - precios en USD         -> ya piensa en la moneda del huésped
  - mencion de tax free    -> o ya lo opera y le falta el legajo, o lo promete
                              y no lo cumple; las dos son venta
  - motor de reserva propio -> hay canal directo donde enchufar el modulo 4
  - PMS detectado          -> el criterio operativo real es que exporte a CSV
"""

import re
from dataclasses import dataclass, field

from . import web


@dataclass
class Senal:
    valor: object
    cita: str = ""
    url: str = ""

    def __bool__(self):
        return bool(self.valor)


@dataclass
class SenalesSitio:
    url: str = ""
    accesible: bool = False
    error: str = ""
    idiomas: Senal = field(default_factory=lambda: Senal([]))
    sitio_en_ingles: Senal = field(default_factory=lambda: Senal(None))
    publica_precios_usd: Senal = field(default_factory=lambda: Senal(None))
    menciona_exencion: Senal = field(default_factory=lambda: Senal(None))
    motor_reserva_propio: Senal = field(default_factory=lambda: Senal(None))
    pms_detectado: Senal = field(default_factory=lambda: Senal(None))
    instagram: Senal = field(default_factory=lambda: Senal(None))
    mails: Senal = field(default_factory=lambda: Senal([]))
    whatsapp: Senal = field(default_factory=lambda: Senal(None))

    # Huellas de motores de reserva y PMS. La lista sale de los nombres que
    # aparecen en research/: Pxsol, Cloudbeds, SiteMinder/Little Hotelier, Zeus,
    # MiniHotel, AlojaSys, CQR. El resto son los que mas se ven en CABA.


HUELLAS_PMS = {
    "Cloudbeds": r"cloudbeds|hotels\.cloudbeds\.com",
    "SiteMinder / Little Hotelier": r"siteminder|littlehotelier|直|book-directonline",
    "Pxsol": r"pxsol",
    "Zeus": r"zeus\w*booking|zeustecnologia",
    "MiniHotel": r"minihotel",
    "AlojaSys": r"alojasys",
    "CQR": r"cqrsistemas|cqr\.com\.ar",
    "Simple Booking": r"simplebooking",
    "Synxis": r"synxis",
    "Mews": r"mews\.com|mewssystems",
    "Booking Engine genérico (motor propio)": r"motor(?:de)?reserv|/reservar|/booking|book-now",
}

PATRON_EXENCION = re.compile(
    r"tax[\s\-]?free|vat[\s\-]?(?:free|refund|exempt)|"
    r"exenci[oó]n\s+de\s+iva|iva\s+exent|sin\s+iva\s+para|"
    r"exempt\s+from\s+vat",
    re.I,
)

PATRON_USD = re.compile(
    r"(?:US\s?\$|USD|U\$S|d[oó]lares)\s?\d{2,6}|" r"\d{2,6}\s?(?:US\s?\$|USD|U\$S)", re.I
)

PATRON_MAIL = re.compile(r"[\w\.\-\+]+@[\w\-]+\.[\w\.\-]+")
PATRON_IG = re.compile(r"instagram\.com/([A-Za-z0-9_.]{2,30})")
PATRON_WA = re.compile(r"(?:wa\.me/|api\.whatsapp\.com/send\?phone=)(\+?\d{6,15})")

MAILS_A_IGNORAR = re.compile(r"@(?:sentry|example|wixpress|godaddy|squarespace)\.", re.I)


def _cita(texto: str, patron: re.Pattern, ancho: int = 90) -> tuple:
    """Devuelve (coincidencia, fragmento de contexto) o (None, '')."""
    m = patron.search(texto)
    if not m:
        return None, ""
    ini = max(0, m.start() - ancho // 2)
    fin = min(len(texto), m.end() + ancho // 2)
    return m.group(0), " ".join(texto[ini:fin].split())


def _idiomas(html: str) -> list:
    encontrados = set()
    for m in re.finditer(r'<html[^>]*\blang=["\']([a-zA-Z\-]{2,5})', html):
        encontrados.add(m.group(1).split("-")[0].lower())
    for m in re.finditer(r'hreflang=["\']([a-zA-Z\-]{2,5})', html):
        codigo = m.group(1).split("-")[0].lower()
        if codigo != "x":
            encontrados.add(codigo)
            # Enlaces a una version en ingles: /en, /en/, /english, ?lang=en
    if re.search(r'href=["\'][^"\']*(?:/en/|/en["\']|/english|[?&]lang=en)', html, re.I):
        encontrados.add("en")
    return sorted(encontrados)


def analizar(url: str) -> SenalesSitio:
    """Trae el sitio del hotel y extrae las señales. No sigue enlaces: una sola
    página, la de inicio. Si hace falta más, lo decide el agente pidiendo otra URL."""
    r = web.traer(url)
    s = SenalesSitio(url=r.url)
    if not r.ok:
        s.error = r.error or f"HTTP {r.status}"
        return s

    s.accesible = True
    html, texto = r.html, r.texto

    idiomas = _idiomas(html)
    s.idiomas = Senal(
        idiomas, f"lang/hreflang detectados: {', '.join(idiomas )or 'ninguno'}", r.url
    )
    # "Ingles real, no traductor": exigimos una declaracion explicita de idioma
    # o un enlace a la version en ingles. Un widget de Google Translate no cuenta.
    s.sitio_en_ingles = Senal("en" in idiomas, s.idiomas.cita, r.url)

    hit, cita = _cita(texto, PATRON_USD)
    s.publica_precios_usd = Senal(
        bool(hit), cita or "sin precios en USD en la página de inicio", r.url
    )

    hit, cita = _cita(texto, PATRON_EXENCION)
    s.menciona_exencion = Senal(
        bool(hit), cita or "sin mencion de exención en la página de inicio", r.url
    )

    for nombre, patron in HUELLAS_PMS.items():
        hit, cita = _cita(html, re.compile(patron, re.I))
        if hit:
            s.pms_detectado = Senal(nombre, f"huella '{hit}' en el HTML", r.url)
            break

    motor = bool(
        re.search(
            r"/reservar|/booking|book[\s\-]?now|reserv[ae]\s+ahora|"
            r"check[\s\-]?in.*check[\s\-]?out",
            html,
            re.I,
        )
    )
    s.motor_reserva_propio = Senal(
        motor or bool(s.pms_detectado.valor),
        s.pms_detectado.cita or "enlace de reserva en el sitio",
        r.url,
    )

    m = PATRON_IG.search(html)
    if m:
        s.instagram = Senal("@" + m.group(1), f"instagram.com/{m.group(1 )}", r.url)

    mails = sorted(
        {
            m.group(0)
            for m in PATRON_MAIL.finditer(html)
            if not MAILS_A_IGNORAR.search(m.group(0))
        }
    )
    s.mails = Senal(
        mails[:5], f"mails en el sitio: {', '.join(mails[:5 ])}" if mails else "", r.url
    )

    m = PATRON_WA.search(html)
    if m:
        s.whatsapp = Senal(m.group(1), f"enlace de WhatsApp a {m.group(1 )}", r.url)

    return s
