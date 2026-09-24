"""
Invariantes de los dos documentos.

Estos tests son el diseno hecho cumplir: que ningun dato se imprima sin
respaldo, y que nada interno se filtre al material que ve el hotel.
"""

import re
import unittest

from investigacion_hotel import config
from investigacion_hotel.estimacion import estimar
from investigacion_hotel.modelo import (
    CAMPOS,
    Interpretacion,
    SIN_VERIFICAR,
    VerificacionPendiente,
)
from investigacion_hotel.render import render_interno, render_externo, CampoNoPublico
from investigacion_hotel.render import externo as mod_externo
from investigacion_hotel.scoring import calificar
from investigacion_hotel.tests.ayuda import dossier, sin_fuente

# Centinelas: strings imposibles de confundir, para buscarlos en la salida.
CENTINELA_DECISOR = "ZZDECISORSECRETOZZ"
CENTINELA_COMPETENCIA = "ZZCOMPETENCIAZZ"
CENTINELA_ANGULO = "ZZANGULODEVENTAZZ"
CENTINELA_OBJECION = "ZZOBJECIONZZ"


def completo():
    d = dossier(
        habitaciones=38,
        adr_publicado_ars=115_000,
        pct_resenas_idioma_extranjero=64.0,
        muestra_resenas=30,
        barrio="Recoleta",
        es_cadena="independiente",
        menciona_exencion=True,
        publica_precios_usd=True,
        sitio_en_ingles=True,
        motor_reserva_propio=True,
        nacionalidades_predominantes=["Estados Unidos", "Francia"],
        decisor_nombre=CENTINELA_DECISOR,
        decisor_rol="Gerente General",
        decisor_contacto="secreto@ejemplo.test",
        decisor_es_generico=False,
        competencia=[CENTINELA_COMPETENCIA],
    )
    d.score = calificar(d)
    d.estimacion = estimar(d)
    d.interpretacion = Interpretacion(CENTINELA_ANGULO, CENTINELA_OBJECION, "llamar el martes")
    d.pendientes = [
        VerificacionPendiente(
            "responde_resenas",
            "Responde las resenas?",
            "https://ejemplo.test/resenas",
            "senal de dolor",
        )
    ]
    return d


def tablas(texto: str) -> dict:
    """Parte el markdown en tablas, indexadas por su fila de encabezado."""
    salida, encabezado = {}, None
    for linea in texto.splitlines():
        if not linea.startswith("|"):
            encabezado = None
            continue
        if encabezado is None:
            encabezado = linea
            salida.setdefault(encabezado, [])
        elif not linea.startswith("|---"):
            salida[encabezado].append(linea)
    return salida


class TestNadaSinRespaldo(unittest.TestCase):
    """Cada dato del hotel sale con nota al pie o con la marca SIN VERIFICAR.
    Un supuesto nuestro sale rotulado como supuesto y con su fundamento.
    No hay tercera opcion."""

    def test_toda_fila_de_dato_del_hotel_tiene_fuente_o_marca(self):
        d = completo()
        sin_fuente(d, "responde_resenas", True)
        texto = render_interno(d)

        filas = [f for enc, fs in tablas(texto).items() if "Cita" in enc for f in fs]
        self.assertGreater(len(filas), 8, "no se encontraron tablas de hallazgos")
        for fila in filas:
            with self.subTest(fila=fila[:60]):
                self.assertTrue(
                    re.search(r"\[\d+\]", fila) or SIN_VERIFICAR in fila,
                    f"fila sin respaldo ni marca: {fila}",
                )

    def test_todo_insumo_de_la_estimacion_declara_de_donde_sale(self):
        """Un numero observado cita su fuente; uno supuesto dice que es supuesto
        y por que. El que falta dice SIN VERIFICAR."""
        texto = render_interno(completo())
        filas = [f for enc, fs in tablas(texto).items() if "Insumo" in enc for f in fs]
        self.assertEqual(len(filas), 5)
        for fila in filas:
            with self.subTest(fila=fila[:50]):
                observado = "observado" in fila and re.search(r"\[\d+\]", fila)
                supuesto = "supuesto" in fila and len(fila.split("|")[4].strip()) > 30
                self.assertTrue(
                    observado or supuesto or SIN_VERIFICAR in fila,
                    f"insumo sin procedencia clara: {fila}",
                )

    def test_el_hallazgo_sin_fuente_se_imprime_como_sin_verificar(self):
        d = completo()
        sin_fuente(d, "responde_resenas", True)
        texto = render_interno(d)
        fila = next(l for l in texto.splitlines()
            if l.startswith("|") and "responde las rese" in l.lower())
        self.assertIn(SIN_VERIFICAR, fila)
        self.assertNotIn("| si |", fila)

    def test_toda_fuente_citada_esta_en_el_listado(self):
        texto = render_interno(completo())
        usadas = {int(n) for n in re.findall(r"\[(\d+)\]", texto)}
        listadas = {int(n) for n in re.findall(r"^\[(\d+)\] http", texto, re.M)}
        self.assertTrue(usadas <= listadas, f"citas sin entrada: {usadas - listadas}")

    def test_sin_ninguna_fuente_lo_dice(self):
        d = dossier()
        sin_fuente(d, "habitaciones", 38)
        self.assertIn("Todo el dossier está SIN VERIFICAR", render_interno(d))


class TestListaBlancaDelExterno(unittest.TestCase):
    """Lo interno no sale. No es cuestion de tono: mandarle al hotel nuestra
    evaluacion comercial de el quema el prospecto."""

    def test_no_se_filtra_ningun_centinela(self):
        texto = render_externo(completo())
        for centinela in (
            CENTINELA_DECISOR,
            CENTINELA_COMPETENCIA,
            CENTINELA_ANGULO,
            CENTINELA_OBJECION,
        ):
            self.assertNotIn(centinela, texto)

    def test_no_lleva_el_puntaje(self):
        texto = render_externo(completo())
        self.assertNotIn("Lista A", texto)
        self.assertNotIn("/100", texto)
        self.assertNotIn("ideal-customer", texto)

    def test_no_lleva_el_banner_interno(self):
        texto = render_externo(completo())
        self.assertNotIn("NO DISTRIBUIR", texto)
        self.assertIn(config.AVISO_EXTERNO.split(".")[0], texto)

    def test_el_interno_si_lleva_todo(self):
        texto = render_interno(completo())
        self.assertIn("NO DISTRIBUIR", texto)
        for centinela in (CENTINELA_DECISOR, CENTINELA_ANGULO):
            self.assertIn(centinela, texto)

    def test_todos_los_campos_externos_estan_marcados_publicos(self):
        for campo in mod_externo.CAMPOS_EXTERNOS:
            self.assertTrue(CAMPOS[campo].publico, f"{campo} no es publico")

    def test_agregar_un_campo_interno_a_la_lista_explota(self):
        """La proteccion tiene que fallar ruidosamente, no filtrar en silencio."""
        original = list(mod_externo.CAMPOS_EXTERNOS)
        mod_externo.CAMPOS_EXTERNOS.append("decisor_nombre")
        try:
            with self.assertRaises(CampoNoPublico):
                render_externo(completo())
        finally:
            mod_externo.CAMPOS_EXTERNOS[:] = original


class TestLimitesDeDominio(unittest.TestCase):
    def test_el_interno_avisa_que_el_bin_no_se_ve(self):
        texto = render_interno(completo())
        self.assertIn("BIN", texto)
        self.assertIn("nunca una medición", texto)

    def test_no_presenta_la_estimacion_como_fuga(self):
        """Es IVA en juego, no plata perdida."""
        for texto in (render_interno(completo()), render_externo(completo())):
            self.assertIn("IVA en juego", texto)
            self.assertNotIn("fuga detectada", texto.lower())
            self.assertNotIn("pierde por mes", texto.lower())

    def test_el_externo_no_promete_resultados_de_fiscalizacion(self):
        texto = render_externo(completo()).lower()
        for prohibido in ("arca no va a observar", "garantiza", "asegura el resultado"):
            self.assertNotIn(prohibido, texto)
        self.assertIn("no constituye asesoramiento fiscal", texto)

    def test_el_externo_usa_el_parrafo_normativo_congelado(self):
        from investigacion_hotel import normativa

        self.assertIn(normativa.MARCO, render_externo(completo()))


class TestCasosBorde(unittest.TestCase):
    def test_dossier_vacio_no_explota(self):
        d = dossier()
        d.score = calificar(d)
        d.estimacion = estimar(d)
        self.assertIn("Indeterminado", render_interno(d))
        self.assertIn("Sin numero", render_interno(d))

    def test_externo_sin_observaciones_avisa_que_no_se_manda(self):
        d = dossier()
        d.estimacion = estimar(d)
        self.assertIn("no debería mandarse así", render_externo(d))

    def test_modo_degradado_se_avisa_arriba(self):
        d = completo()
        d.modo_degradado = True
        self.assertIn("MODO DEGRADADO", render_interno(d).split("## Veredicto")[0])

    def test_corrida_incompleta_se_avisa_arriba(self):
        d = completo()
        d.secciones_incompletas = ["decisor"]
        self.assertIn("CORRIDA INCOMPLETA", render_interno(d).split("## Veredicto")[0])

    def test_pendientes_explican_como_cerrarlas(self):
        texto = render_interno(completo())
        self.assertIn("--rehacer", texto)
        self.assertIn("https://ejemplo.test/resenas", texto)


if __name__ == "__main__":
    unittest.main()
