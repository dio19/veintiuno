"""
El motor de la corrida, sin red y sin API.

Lo que se verifica aca es el contrato: que un hallazgo sin respaldo no pueda
entrar como dato, que los topes se respeten, y que agotar el presupuesto
devuelva un dossier corto en vez de una excepcion.
"""

import types
import unittest

from investigacion_hotel import offline
from investigacion_hotel.agente import (
    Investigacion,
    Presupuesto,
    _aplanar,
    _contar_uso,
    _revisar_server_tools,
)
from investigacion_hotel.modelo import SIN_VERIFICAR
from investigacion_hotel.scoring import INDETERMINADO

SITIO = offline.URL_SITIO


def investigacion():
    return Investigacion(
        offline.HOTEL, "Buenos Aires", padron_local=str(offline.FIXTURES / "padron.csv")
    )


class TestValidacionDeHallazgos(unittest.TestCase):
    def setUp(self):
        self.ctx = offline.fixtures_en_lugar_de_la_red()
        self.ctx.__enter__()
        self.inv = investigacion()

    def tearDown(self):
        self.ctx.__exit__(None, None, None)

    def test_campo_inexistente_se_rechaza_y_no_guarda_nada(self):
        r = self.inv.registrar_hallazgo("cantidad_de_piletas", "2", SITIO, "una cita larga")
        self.assertTrue(r.startswith("ERROR"))
        self.assertEqual(self.inv.dossier.hallazgos, {})

    def test_valor_de_tipo_equivocado_se_rechaza(self):
        r = self.inv.registrar_hallazgo(
            "habitaciones", "unas cuantas", SITIO, "38 habitaciones"
        )
        self.assertTrue(r.startswith("ERROR"))
        self.assertNotIn("habitaciones", self.inv.dossier.hallazgos)

    def test_cita_real_queda_verificada(self):
        self.inv.registrar_hallazgo(
            "habitaciones", "38", SITIO, "38 habitaciones en el corazon de Recoleta"
        )
        h = self.inv.dossier.hallazgos["habitaciones"]
        self.assertTrue(h.verificado)
        self.assertEqual(h.valor, 38)

    def test_cita_inventada_no_entra_como_dato(self):
        """El caso que este diseno existe para atajar."""
        self.inv.registrar_hallazgo(
            "habitaciones", "120", SITIO, "el hotel cuenta con 120 habitaciones y dos piscinas"
        )
        h = self.inv.dossier.hallazgos["habitaciones"]
        self.assertEqual(h.estado, SIN_VERIFICAR)
        self.assertIn("no aparece en la fuente", h.nota)
        self.assertIsNone(self.inv.dossier.valor("habitaciones"))

    def test_cita_inventada_abre_verificacion_pendiente(self):
        self.inv.registrar_hallazgo(
            "habitaciones", "120", SITIO, "120 habitaciones y dos piscinas"
        )
        self.assertTrue(any(p.campo == "habitaciones" for p in self.inv.dossier.pendientes))

    def test_sin_url_queda_sin_verificar(self):
        self.inv.registrar_hallazgo("habitaciones", "38", "", "38 habitaciones")
        self.assertEqual(self.inv.dossier.hallazgos["habitaciones"].estado, SIN_VERIFICAR)

    def test_fuente_ilegible_no_se_da_por_buena(self):
        """Booking y TripAdvisor bloquean: la cita no se puede comprobar y eso
        se dice, no se asume cierta."""
        self.inv.registrar_hallazgo(
            "pct_resenas_idioma_extranjero",
            "60",
            "https://www.booking.com/hotel/ar/prueba.html",
            "60% de las resenas en inglés",
        )
        h = self.inv.dossier.hallazgos["pct_resenas_idioma_extranjero"]
        self.assertEqual(h.estado, SIN_VERIFICAR)
        self.assertIn("no se pudo leer la fuente", h.nota)

    def test_la_cita_tolera_puntuacion_y_espacios_pero_no_contenido_distinto(self):
        self.assertEqual(_aplanar("USD 95, por noche"), _aplanar("usd  95 por-noche"))
        self.assertNotEqual(_aplanar("USD 95"), _aplanar("USD 195"))


class TestTopes(unittest.TestCase):
    def test_sin_presupuesto_de_lectura_no_lee_ni_explota(self):
        with offline.fixtures_en_lugar_de_la_red():
            inv = Investigacion(
                offline.HOTEL, "Buenos Aires", presupuesto=Presupuesto(max_fetches=0)
            )
            r = inv.leer_sitio(SITIO)
            self.assertIn("se agoto el presupuesto", r)
            self.assertEqual(inv.presupuesto.fetches, 0)

    def test_la_lectura_consume_presupuesto(self):
        with offline.fixtures_en_lugar_de_la_red():
            inv = investigacion()
            inv.leer_sitio(SITIO)
            self.assertEqual(inv.presupuesto.fetches, 1)

    def test_presupuesto_agotado_marca_el_dossier_incompleto(self):
        inv = investigacion()
        inv.presupuesto.turnos = inv.presupuesto.max_turnos
        d = inv.cerrar()
        self.assertTrue(d.secciones_incompletas)
        self.assertEqual(d.score.lista, INDETERMINADO)

    def test_agotar_el_presupuesto_devuelve_dossier_no_excepcion(self):
        d = offline.correr(Presupuesto(max_fetches=0, max_turnos=0))
        self.assertIsNotNone(d.score)
        self.assertIsNotNone(d.estimacion)


class TestServerTools(unittest.TestCase):
    """Los errores de las herramientas server-side vuelven con HTTP 200 y un
    objeto de error adentro. En exito el content es una lista; en error, no."""

    def _mensaje(self, contenido):
        bloque = types.SimpleNamespace(type="web_search_tool_result", content=contenido)
        return types.SimpleNamespace(content=[bloque], usage=None)

    def test_busqueda_exitosa_se_cuenta(self):
        inv = investigacion()
        resultado = types.SimpleNamespace(url="https://ejemplo.test/a", title="A")
        _revisar_server_tools(inv, self._mensaje([resultado]))
        self.assertEqual(inv.presupuesto.busquedas, 1)

    def test_error_de_busqueda_no_explota_y_queda_registrado(self):
        inv = investigacion()
        _revisar_server_tools(
            inv, self._mensaje(types.SimpleNamespace(error_code="max_uses_exceeded"))
        )
        self.assertEqual(inv.presupuesto.busquedas, 0 + inv.presupuesto.max_busquedas)
        self.assertTrue(any("ERROR de busqueda" in l for l in inv.registro))

    def test_mensaje_sin_uso_no_explota(self):
        inv = investigacion()
        _contar_uso(inv, types.SimpleNamespace(usage=None))
        self.assertEqual(inv.presupuesto.tokens_entrada, 0)


class TestCorridaOffline(unittest.TestCase):
    """El pipeline entero contra fixtures: costo cero, resultado siempre igual."""

    @classmethod
    def setUpClass(cls):
        cls.d = offline.correr()

    def test_es_determinista(self):
        otra = offline.correr()
        self.assertEqual(sorted(self.d.hallazgos), sorted(otra.hallazgos))
        self.assertEqual(self.d.score.puntos, otra.score.puntos)

    def test_junta_datos_del_padron_y_del_sitio(self):
        self.assertEqual(self.d.valor("categoria"), "3 Estrellas")
        self.assertEqual(self.d.valor("habitaciones"), 38)
        self.assertTrue(self.d.valor("menciona_exencion"))
        self.assertEqual(self.d.valor("pms_detectado"), "Cloudbeds")

    def test_el_guion_ejercita_el_camino_de_rechazo(self):
        self.assertEqual(self.d.hallazgos["responde_resenas"].estado, SIN_VERIFICAR)

    def test_sin_el_dato_de_resenas_no_califica_ni_estima(self):
        """Los dos frenos, juntos: sin el proxy central no hay veredicto ni numero."""
        self.assertEqual(self.d.score.lista, INDETERMINADO)
        self.assertFalse(self.d.estimacion.hay_numero)

    def test_deja_dicho_como_cerrar_lo_que_falta(self):
        p = next(p for p in self.d.pendientes if p.campo == "pct_resenas_idioma_extranjero")
        self.assertIn("booking.com", p.url)
        self.assertTrue(p.pregunta.strip().endswith("?"))

    def test_registra_el_consumo(self):
        self.assertIn("páginas leídas", self.d.consumo)


if __name__ == "__main__":
    unittest.main()
