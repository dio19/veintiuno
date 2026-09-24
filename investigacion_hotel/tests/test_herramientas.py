"""Herramientas deterministicas: padron del GCBA y senales del sitio propio.

Ninguno de estos tests toca la red: el sitio sale de fixtures/hotel_prueba/ y
el padron de una copia chica. El hotel es ficticio, como tiene que ser: un
prospecto real no entra al repo.
"""

import unittest
from pathlib import Path

from investigacion_hotel.herramientas import padron_gcba, sitio_hotel, web

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures" / "hotel_prueba"
PADRON = str(FIXTURES / "padron.csv")


class TestHtmlATexto(unittest.TestCase):
    def test_saca_script_y_style(self):
        texto = web.html_a_texto((FIXTURES / "sitio.html").read_text(encoding="utf-8"))
        self.assertIn("38 habitaciones", texto)
        self.assertNotIn("analytics", texto)
        self.assertNotIn("display:none", texto)


class TestSenalesDelSitio(unittest.TestCase):
    def setUp(self):
        html = (FIXTURES / "sitio.html").read_text(encoding="utf-8")
        self._original = web.traer
        web.traer = lambda url, **kw: web.Respuesta(
            url, 200, html=html, texto=web.html_a_texto(html)
        )
        sitio_hotel.web.traer = web.traer
        self.s = sitio_hotel.analizar("https://hotelpruebaveintiuno.test")

    def tearDown(self):
        web.traer = self._original
        sitio_hotel.web.traer = self._original

    def test_detecta_version_en_ingles(self):
        self.assertTrue(self.s.sitio_en_ingles.valor)
        self.assertIn("en", self.s.idiomas.valor)

    def test_detecta_precios_en_usd_con_cita(self):
        self.assertTrue(self.s.publica_precios_usd.valor)
        self.assertIn("USD 95", self.s.publica_precios_usd.cita)

    def test_detecta_mencion_de_exencion_con_cita(self):
        self.assertTrue(self.s.menciona_exencion.valor)
        self.assertIn("tax free", self.s.menciona_exencion.cita.lower())

    def test_identifica_el_pms_por_la_huella_de_la_url(self):
        self.assertEqual(self.s.pms_detectado.valor, "Cloudbeds")

    def test_motor_de_reserva_propio(self):
        self.assertTrue(self.s.motor_reserva_propio.valor)

    def test_contacto_publico(self):
        self.assertEqual(self.s.instagram.valor, "@hotelpruebaveintiuno")
        self.assertEqual(self.s.whatsapp.valor, "5491133334444")
        self.assertIn("reservas@hotelpruebaveintiuno.test", self.s.mails.valor)

    def test_toda_senal_positiva_trae_cita(self):
        """Una senal sin cita no puede convertirse en Hallazgo verificado."""
        for nombre in (
            "sitio_en_ingles",
            "publica_precios_usd",
            "menciona_exencion",
            "pms_detectado",
            "instagram",
        ):
            senal = getattr(self.s, nombre)
            if senal.valor:
                self.assertTrue(senal.cita.strip(), f"{nombre} sin cita")
                self.assertTrue(senal.url.strip(), f"{nombre} sin url")


class TestSitioCaido(unittest.TestCase):
    def test_no_rompe_y_marca_inaccesible(self):
        original = sitio_hotel.web.traer
        sitio_hotel.web.traer = lambda url, **kw: web.Respuesta(url, 0, error="timeout")
        try:
            s = sitio_hotel.analizar("https://no-responde.test")
            self.assertFalse(s.accesible)
            self.assertEqual(s.error, "timeout")
            self.assertIsNone(s.sitio_en_ingles.valor)
        finally:
            sitio_hotel.web.traer = original


class TestPadron(unittest.TestCase):
    def test_encuentra_por_nombre_exacto(self):
        res, err = padron_gcba.buscar("Hotel Prueba Veintiuno", ruta_local=PADRON)
        self.assertEqual(err, "")
        self.assertEqual(res[0]["nombre"], "Hotel Prueba Veintiuno")
        self.assertEqual(res[0]["tipo"], "3 Estrellas")

    def test_la_categoria_sale_del_padron(self):
        """El campo `tipo` del CSV abierto ya trae la categoria: no hace falta
        parsear el PDF del ENTUR para saber si es 3 estrellas o boutique."""
        res, _ = padron_gcba.buscar("Petit Hotel Palermo", ruta_local=PADRON)
        self.assertIn("Boutique", res[0]["tipo"])

    def test_avisa_cuando_confunde_hotel_con_hostel(self):
        """Un hostel es anti-ICP. Se parecen en una letra y la similitud textual
        no puede distinguirlos: hay que avisar, no rankear en silencio."""
        res, _ = padron_gcba.buscar("Hotel Prueba Veintiuno", ruta_local=PADRON)
        hostel = [m for m in res if m["nombre"].startswith("Hostel")]
        self.assertTrue(hostel, "el hostel deberia aparecer como candidato")
        self.assertIn("hostel", hostel[0]["_advertencia"])

    def test_nombre_inexistente_no_devuelve_nada(self):
        """Compartir la palabra 'hotel' no es parecerse: sin un token distintivo
        en comun no hay coincidencia, aunque el ratio de texto de alto."""
        res, _ = padron_gcba.buscar("Hotel Marambio Quilmes", ruta_local=PADRON)
        self.assertEqual(res, [])

    def test_alcanza_con_un_token_distintivo_en_comun(self):
        res, _ = padron_gcba.buscar("Prueba Veintiuno", ruta_local=PADRON)
        self.assertTrue(any(m["nombre"] == "Hotel Prueba Veintiuno" for m in res))

    def test_no_elige_solo_cuando_hay_ambiguedad(self):
        res, _ = padron_gcba.buscar("Recoleta", ruta_local=PADRON)
        self.assertGreaterEqual(len(res), 1)
        self.assertTrue(all("_similitud" in m for m in res))

    def test_padron_ilegible_devuelve_error_y_no_explota(self):
        res, err = padron_gcba.buscar("X", ruta_local="/no/existe/padron.csv")
        self.assertEqual(res, [])
        self.assertIn("no se pudo leer", err)


if __name__ == "__main__":
    unittest.main()
