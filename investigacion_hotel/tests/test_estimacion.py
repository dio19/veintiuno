"""La estimacion preliminar: un rango con los supuestos a la vista, o nada."""

import unittest

from investigacion_hotel.estimacion import (
    estimar,
    quitar_iva,
    DESCUENTO_EXENCION,
    IVA,
    SUPUESTO_OCUPACION,
    SUPUESTO_PAGO_EXTERIOR,
)
from investigacion_hotel.modelo import SIN_VERIFICAR, OBSERVADO, SUPUESTO
from investigacion_hotel.tests.ayuda import dossier, sin_fuente


def completo(**pisar):
    base = dict(
        habitaciones=40,
        adr_publicado_ars=100_000,
        pct_resenas_idioma_extranjero=50.0,
        muestra_resenas=30,
    )
    base.update(pisar)
    return dossier(**base)


class TestConversionDeIva(unittest.TestCase):
    def test_quitar_iva_es_menos_17_36_por_ciento(self):
        """Quitar el IVA de un precio final es -17,36%, no -21%."""
        self.assertAlmostEqual(DESCUENTO_EXENCION, 0.173553719, places=8)
        self.assertAlmostEqual(quitar_iva(121_000), 100_000, places=6)
        self.assertAlmostEqual(quitar_iva(100_000) / 100_000, 1 - DESCUENTO_EXENCION, places=8)

    def test_no_es_restar_el_21_por_ciento(self):
        self.assertNotAlmostEqual(quitar_iva(100_000), 79_000, places=0)


class TestSeNiegaAInventar(unittest.TestCase):
    def test_sin_ningun_insumo_no_emite_numero(self):
        r = estimar(dossier())
        self.assertFalse(r.hay_numero)
        self.assertIsNone(r.rango_iva_mensual_estimado_ars)
        self.assertEqual(len(r.faltantes), 3)
        self.assertIn("dos o más sin verificar", r.motivo_sin_numero)

    def test_con_un_solo_faltante_dice_cual_es(self):
        d = completo()
        del d.hallazgos["adr_publicado_ars"]
        r = estimar(d)
        self.assertFalse(r.hay_numero)
        self.assertEqual(r.faltantes, ["ADR publicado con IVA"])
        self.assertIn("ADR publicado con IVA", r.motivo_sin_numero)

    def test_insumo_faltante_queda_SIN_VERIFICAR_y_no_en_cero(self):
        """Un dato que falta no es un cero: un cero se multiplicaria y daria
        un rango de cero, que se leeria como 'este hotel no tiene nada en juego'."""
        d = completo()
        del d.hallazgos["habitaciones"]
        r = estimar(d)
        insumo = next(i for i in r.insumos if i.nombre == "habitaciones")
        self.assertEqual(insumo.procedencia, SIN_VERIFICAR)
        self.assertIsNone(insumo.valor)
        self.assertNotEqual(insumo.valor, 0)

    def test_hallazgo_sin_fuente_no_habilita_la_estimacion(self):
        d = completo()
        del d.hallazgos["habitaciones"]
        sin_fuente(d, "habitaciones", 40)
        self.assertFalse(estimar(d).hay_numero)


class TestRango(unittest.TestCase):
    def test_emite_rango_con_los_cinco_insumos(self):
        r = estimar(completo())
        self.assertTrue(r.hay_numero)
        bajo, alto = r.rango_iva_mensual_estimado_ars
        self.assertLess(bajo, alto)
        self.assertGreater(bajo, 0)

    def test_el_rango_coincide_con_la_formula(self):
        r = estimar(completo())
        neto = quitar_iva(100_000)
        esperado_bajo = (
            40 * 30 * SUPUESTO_OCUPACION[0] * 0.50 * SUPUESTO_PAGO_EXTERIOR[0] * neto * IVA
        )
        esperado_alto = (
            40 * 30 * SUPUESTO_OCUPACION[1] * 0.50 * SUPUESTO_PAGO_EXTERIOR[1] * neto * IVA
        )
        bajo, alto = r.rango_iva_mensual_estimado_ars
        self.assertAlmostEqual(bajo, esperado_bajo, delta=10_000)
        self.assertAlmostEqual(alto, esperado_alto, delta=10_000)

    def test_anualizado_es_doce_meses(self):
        r = estimar(completo())
        mes_bajo, mes_alto = r.rango_iva_mensual_estimado_ars
        ano_bajo, ano_alto = r.rango_iva_anualizado_estimado_ars
        self.assertAlmostEqual(ano_bajo, mes_bajo * 12, delta=100_000)
        self.assertAlmostEqual(ano_alto, mes_alto * 12, delta=100_000)

    def test_los_supuestos_viajan_con_su_fundamento(self):
        """Un supuesto que no se ve es una mentira: cada insumo supuesto tiene
        que poder explicarse solo en el documento."""
        r = estimar(completo())
        supuestos = [i for i in r.insumos if i.procedencia == SUPUESTO]
        self.assertEqual(len(supuestos), 2)
        for i in supuestos:
            self.assertTrue(i.fundamento.strip(), i.nombre)
        pago = next(i for i in supuestos if "exterior" in i.nombre)
        self.assertIn(SIN_VERIFICAR, pago.fundamento)

    def test_observados_marcados_como_tales(self):
        r = estimar(completo())
        observados = [i.nombre for i in r.insumos if i.procedencia == OBSERVADO]
        self.assertEqual(len(observados), 3)


class TestAdvertencias(unittest.TestCase):
    def test_avisa_por_brasil_y_chile_sin_inventar_un_coeficiente(self):
        r = estimar(completo(nacionalidades_predominantes=["Brasil", "Estados Unidos"]))
        self.assertTrue(r.hay_numero)
        aviso = " ".join(r.advertencias)
        self.assertIn("Brasil", aviso)
        self.assertIn(SIN_VERIFICAR, aviso)

    def test_avisa_cuando_la_muestra_de_resenas_es_chica(self):
        r = estimar(completo(muestra_resenas=5))
        self.assertTrue(any("muestra de 5" in a for a in r.advertencias))

    def test_sin_muestra_chica_no_hay_aviso_de_muestra(self):
        r = estimar(completo(muestra_resenas=30))
        self.assertFalse(any("muestra de" in a for a in r.advertencias))


if __name__ == "__main__":
    unittest.main()


class TestNoSeConfundeConLaFuga(unittest.TestCase):
    """El rango es IVA en juego, no plata perdida. Presentarlo como fuga infla
    el numero y se cae en la primera reunion."""

    def test_declara_que_mide(self):
        r = estimar(completo())
        self.assertIn("IVA en juego", r.que_mide)
        self.assertIn("NO es la fuga", r.que_mide)

    def test_calibracion_contra_la_corrida_del_motor(self):
        """El unico contraste disponible: los parametros del hotel de la demo
        puestos en esta formula tienen que contener el IVA en juego que el motor
        midio de verdad sobre ese mismo dataset.

        Valida la aritmetica, no el supuesto de mercado: la demo es sintetica.
        """
        d = completo(
            habitaciones=42, adr_publicado_ars=100_384, pct_resenas_idioma_extranjero=43.4
        )
        bajo, alto = estimar(d).rango_iva_mensual_estimado_ars
        medido_por_el_motor = 2_749_353  # demo/salida/radiografia.json, mensualizado
        self.assertLess(bajo, medido_por_el_motor)
        self.assertGreater(alto, medido_por_el_motor)
