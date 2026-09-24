"""La linea de comandos, de punta a punta, sin red ni API."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

from investigacion_hotel.__main__ import main, slug


class TestSlug(unittest.TestCase):
    def test_saca_acentos_y_espacios(self):
        self.assertEqual(slug("Hotel Ñandú de Palermo"), "hotel-nandu-de-palermo")

    def test_nombre_impronunciable_no_da_ruta_vacia(self):
        self.assertEqual(slug("!!!"), "hotel")


class TestCorridaOffline(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.carpeta = Path(self.tmp.name) / "salida"
        self.salida = io.StringIO()
        with redirect_stdout(self.salida):
            self.codigo = main(["--offline", "--externo", "--salida", str(self.carpeta)])

    def tearDown(self):
        self.tmp.cleanup()

    def test_termina_bien(self):
        self.assertEqual(self.codigo, 0)

    def test_escribe_los_tres_archivos(self):
        for nombre in ("dossier.md", "dossier.json", "estimacion_preliminar.md"):
            self.assertTrue((self.carpeta / nombre).exists(), nombre)

    def test_el_json_se_puede_volver_a_leer(self):
        d = json.loads((self.carpeta / "dossier.json").read_text(encoding="utf-8"))
        self.assertIn("hallazgos", d)
        self.assertEqual(d["hallazgos"]["habitaciones"]["valor"], 38)

    def test_avisa_que_es_material_interno(self):
        self.assertIn("No sale de Veintiuno sin autorización", self.salida.getvalue())

    def test_avisa_cual_es_el_unico_archivo_que_ve_el_hotel(self):
        self.assertIn("ÚNICO", self.salida.getvalue())

    def test_sin_externo_no_escribe_la_pieza_que_va_al_hotel(self):
        otra = Path(self.tmp.name) / "sin-externo"
        with redirect_stdout(io.StringIO()):
            main(["--offline", "--salida", str(otra)])
        self.assertTrue((otra / "dossier.md").exists())
        self.assertFalse((otra / "estimacion_preliminar.md").exists())


class TestRehacer(unittest.TestCase):
    """El circuito con el que se cierran las verificaciones pendientes: editar
    el JSON a mano y rehacer los documentos sin volver a pagar la investigacion."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.carpeta = Path(self.tmp.name)
        with redirect_stdout(io.StringIO()):
            main(["--offline", "--salida", str(self.carpeta)])

    def tearDown(self):
        self.tmp.cleanup()

    def test_un_dato_agregado_a_mano_cambia_el_veredicto(self):
        ruta = self.carpeta / "dossier.json"
        d = json.loads(ruta.read_text(encoding="utf-8"))
        self.assertEqual(d["score"]["lista"], "indeterminado")

        fuente = {
            "url": "https://www.booking.com/hotel/ar/prueba.html",
            "titulo": "Booking",
            "consultada": "2026-09-15",
        }
        d["hallazgos"]["pct_resenas_idioma_extranjero"] = {
            "campo": "pct_resenas_idioma_extranjero",
            "valor": 63.0,
            "estado": "verificado",
            "fuente": fuente,
            "cita": "19 de 30 en inglés",
            "confianza": "alta",
            "nota": "verificado a mano",
        }
        d["hallazgos"]["muestra_resenas"] = {
            "campo": "muestra_resenas",
            "valor": 30,
            "estado": "verificado",
            "fuente": fuente,
            "cita": "ultimas 30",
            "confianza": "alta",
            "nota": "",
        }
        ruta.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")

        with redirect_stdout(io.StringIO()):
            codigo = main(["--rehacer", str(self.carpeta)])
        self.assertEqual(codigo, 0)

        rehecho = json.loads(ruta.read_text(encoding="utf-8"))
        self.assertEqual(rehecho["score"]["lista"], "A")
        self.assertTrue(rehecho["estimacion"]["hay_numero"])

    def test_sin_dossier_json_falla_con_mensaje_claro(self):
        vacia = self.carpeta / "vacia"
        vacia.mkdir()
        err = io.StringIO()
        with redirect_stderr(err), redirect_stdout(io.StringIO()):
            codigo = main(["--rehacer", str(vacia)])
        self.assertEqual(codigo, 2)
        self.assertIn("No hay dossier.json", err.getvalue())

    def test_un_campo_que_ya_no_existe_se_descarta_sin_romper(self):
        ruta = self.carpeta / "dossier.json"
        d = json.loads(ruta.read_text(encoding="utf-8"))
        d["hallazgos"]["campo_de_una_version_vieja"] = {
            "campo": "campo_de_una_version_vieja",
            "valor": "x",
            "estado": "verificado",
            "fuente": None,
            "cita": "",
            "confianza": "alta",
        }
        ruta.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(["--rehacer", str(self.carpeta)]), 0)


class TestGuardas(unittest.TestCase):
    def test_sin_nombre_ni_offline_no_corre(self):
        err = io.StringIO()
        with redirect_stderr(err), redirect_stdout(io.StringIO()):
            codigo = main([])
        self.assertEqual(codigo, 2)
        self.assertIn("Falta --nombre", err.getvalue())

    def test_sin_clave_avisa_y_ofrece_offline(self):
        import os

        previo = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            err = io.StringIO()
            with redirect_stderr(err), redirect_stdout(io.StringIO()):
                codigo = main(["--nombre", "Hotel X"])
            self.assertIn(codigo, (3, 4))
            self.assertIn("--offline", err.getvalue())
        finally:
            if previo is not None:
                os.environ["ANTHROPIC_API_KEY"] = previo


if __name__ == "__main__":
    unittest.main()
