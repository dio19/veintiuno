"""
Veintiuno - investigacion_hotel · Acceso HTTP y HTML a texto
=============================================================
Todo sobre libreria estandar. No hace falta requests: son pocos GET simples, y
mantener el arbol de dependencias corto es lo que permite que el resto del repo
siga siendo stdlib puro.

La cache en disco no es una optimizacion: es lo que hace que se pueda iterar el
prompt y el render sin volver a pagar la investigacion.
"""

import gzip
import hashlib
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from dataclasses import dataclass
from html.parser import HTMLParser

from .. import config


@dataclass
class Respuesta:
    url: str
    status: int
    html: str = ""
    texto: str = ""
    error: str = ""
    desde_cache: bool = False

    @property
    def ok(self) -> bool:
        return self.status == 200 and not self.error


class _ExtractorDeTexto(HTMLParser):
    """HTML a texto plano. No necesitamos un arbol DOM: el LLM lee texto y las
    huellas se buscan por regex sobre el HTML crudo."""

    SALTEAR = {"script", "style", "noscript", "svg", "head"}
    BLOQUE = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "section", "article"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.partes = []
        self._saltando = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SALTEAR:
            self._saltando += 1
        elif tag in self.BLOQUE:
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SALTEAR and self._saltando:
            self._saltando -= 1

    def handle_data(self, data):
        if not self._saltando and data.strip():
            self.partes.append(data.strip())

    def texto(self) -> str:
        crudo = " ".join(self.partes)
        crudo = re.sub(r"[ \t]+", " ", crudo)
        return re.sub(r"\n\s*\n+", "\n\n", crudo).strip()


def html_a_texto(html: str) -> str:
    p = _ExtractorDeTexto()
    try:
        p.feed(html)
    except Exception:
        # HTML roto: devolvemos lo que se haya podido juntar antes de romper.
        pass
    return p.texto()


def _ruta_cache(url: str):
    clave = hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]
    return config.CACHE_DIR / f"{clave}.json"


def _leer_cache(url: str):
    ruta = _ruta_cache(url)
    if not ruta.exists():
        return None
    if (time.time() - ruta.stat().st_mtime) > config.CACHE_TTL_H * 3600:
        return None
    try:
        d = json.loads(ruta.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return Respuesta(**d, desde_cache=True)


def _guardar_cache(r: Respuesta):
    config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    d = {"url": r.url, "status": r.status, "html": r.html, "texto": r.texto, "error": r.error}
    try:
        _ruta_cache(r.url).write_text(json.dumps(d), encoding="utf-8")
    except OSError:
        pass  # sin cache se puede seguir; es una optimizacion, no un requisito


# El Python de python.org en macOS viene sin bundle de certificados propio, y
# entonces cualquier HTTPS falla con CERTIFICATE_VERIFY_FAILED. En vez de pedir
# certifi o -peor- apagar la verificacion, usamos el bundle del sistema.
# La verificacion queda ENCENDIDA: lo unico que cambia es de donde salen las CA.
_CA_DEL_SISTEMA = "/etc/ssl/cert.pem"
_contexto: ssl.SSLContext | None = None


def _contexto_ssl() -> ssl.SSLContext:
    global _contexto
    if _contexto is None:
        _contexto = ssl.create_default_context()
        propio = ssl.get_default_verify_paths().openssl_cafile
        if not (propio and os.path.exists(propio)) and os.path.exists(_CA_DEL_SISTEMA):
            _contexto.load_verify_locations(cafile=_CA_DEL_SISTEMA)
    return _contexto


_robots: dict = {}


def permitido_por_robots(url: str) -> bool:
    """Consulta robots.txt del origen. Ante la duda (robots ilegible o caido),
    permite: el default de la RFC es permisivo y no vamos a inventar un bloqueo."""
    if not config.RESPETAR_ROBOTS:
        return True
    partes = urllib.parse.urlparse(url)
    origen = f"{partes.scheme}://{partes.netloc}"
    if origen not in _robots:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(f"{origen}/robots.txt")
        try:
            pedido = urllib.request.Request(
                f"{origen}/robots.txt", headers={"User-Agent": config.USER_AGENT}
            )
            with urllib.request.urlopen(
                pedido, timeout=config.TIMEOUT_HTTP_S, context=_contexto_ssl()
            ) as resp:
                rp.parse(resp.read().decode("utf-8", errors="replace").splitlines())
        except Exception:
            rp = None
        _robots[origen] = rp
    rp = _robots[origen]
    if rp is None:
        return True
    try:
        return rp.can_fetch(config.USER_AGENT, url)
    except Exception:
        return True


def traer(url: str, usar_cache: bool = True, timeout: int | None = None) -> Respuesta:
    """GET con timeout, user-agent identificable, gzip y cache en disco."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    if usar_cache:
        cacheada = _leer_cache(url)
        if cacheada is not None:
            return cacheada

    if not permitido_por_robots(url):
        return Respuesta(url, 0, error="bloqueado por robots.txt")

    pedido = urllib.request.Request(
        url,
        headers={
            "User-Agent": config.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip",
        },
    )
    try:
        with urllib.request.urlopen(
            pedido, timeout=timeout or config.TIMEOUT_HTTP_S, context=_contexto_ssl()
        ) as resp:
            crudo = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                crudo = gzip.decompress(crudo)
            juego = resp.headers.get_content_charset() or "utf-8"
            html = crudo.decode(juego, errors="replace")
            r = Respuesta(url, resp.status, html=html, texto=html_a_texto(html))
    except urllib.error.HTTPError as e:
        r = Respuesta(url, e.code, error=f"HTTP {e.code}")
    except Exception as e:
        r = Respuesta(url, 0, error=f"{type(e).__name__}: {e}")

    if r.ok:
        _guardar_cache(r)
    return r
