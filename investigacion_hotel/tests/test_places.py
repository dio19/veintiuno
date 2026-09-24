"""Google Places: la interpretacion de la respuesta, contra un fixture.

No toca la API. Lo que importa verificar es que el limite de la muestra se
diga siempre, porque es la diferencia entre un indicio y un numero inflado.
"""

import json
import unittest
from pathlib import Path

from investigacion_hotel.agente import Investigacion
from investigacion_hotel.herramientas import places
from investigacion_hotel.modelo import VERIFICADO

FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "hotel_prueba" / "places.json"


class TestInterpretacion(unittest.TestCase):
    def setUp(self):
        self.r = places.interpretar(json.loads(FIXTURE.read_text(encoding="utf-8")))

    def test_datos_basicos(self):
        self.assertTrue(self.r.encontrado)
        self.assertEqual(self.r.rating, 4.3)
        self.assertEqual(self.r.total_resenas, 412)
        self.assertEqual(self.r.web, "https://hotelpruebaveintiuno.test")

    def test_calcula_el_porcentaje_sobre_la_muestra_real(self):
        """4 de 5 resenas en idioma extranjero (en, pt, en, fr) = 80%."""
        self.assertEqual(self.r.muestra, 5)
        self.assertEqual(self.r.pct_extranjero, 80.0)

    def test_el_castellano_no_cuenta_como_extranjero(self):
        self.assertIn("es", self.r.idiomas)
        self.assertLess(self.r.pct_extranjero, 100)

    def test_siempre_avisa_que_la_muestra_es_chica(self):
        self.assertIn("no 30", self.r.aviso)
        self.assertIn("412 resenas en total", self.r.aviso)

    def test_avisa_por_portugues(self):
        self.assertIn("Brasil", self.r.aviso)

    def test_sin_resultados_no_explota(self):
        r = places.interpretar({"places": []})
        self.assertFalse(r.encontrado)
        self.assertIn("sin resultados", r.error)

    def test_sin_resenas_lo_dice_en_vez_de_dar_cero(self):
        """Cero resenas con idioma no es 0% de extranjeros: es que no se sabe."""
        r = places.interpretar({"places": [{"displayName": {"text": "X"}, "reviews": []}]})
        self.assertIsNone(r.pct_extranjero)
        self.assertIn("sigue sin resolverse", r.aviso)


class TestRegistroAutomatico(unittest.TestCase):
    """Lo que devuelve Places lo registra el codigo, no el modelo: no hay cita
    textual que comprobar en una respuesta JSON."""

    def setUp(self):
        self.inv = Investigacion("Hotel Prueba Veintiuno", "Buenos Aires")
        self._consultar = places.consultar
        self._hay_clave = places.hay_clave
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        places.consultar = lambda n, c: places.interpretar(payload)
        places.hay_clave = lambda: True

    def tearDown(self):
        places.consultar = self._consultar
        places.hay_clave = self._hay_clave

    def test_registra_el_proxy_como_verificado(self):
        self.inv.consultar_places()
        h = self.inv.dossier.hallazgos["pct_resenas_idioma_extranjero"]
        self.assertEqual(h.estado, VERIFICADO)
        self.assertEqual(h.valor, 80.0)
        self.assertIn("no afirmado por el modelo", h.nota)

    def test_la_muestra_viaja_pegada_al_porcentaje(self):
        self.inv.consultar_places()
        self.assertEqual(self.inv.dossier.valor("muestra_resenas"), 5)

    def test_deja_pendiente_la_verificacion_sobre_30_resenas(self):
        self.inv.consultar_places()
        p = next(
            p
            for p in self.inv.dossier.pendientes
            if p.campo == "pct_resenas_idioma_extranjero"
        )
        self.assertIn("30 reseñas", p.pregunta)

    def test_sin_clave_no_inventa_nada(self):
        places.hay_clave = lambda: False
        r = self.inv.consultar_places()
        self.assertIn("no está configurado", r)
        self.assertEqual(self.inv.dossier.hallazgos, {})


if __name__ == "__main__":
    unittest.main()
