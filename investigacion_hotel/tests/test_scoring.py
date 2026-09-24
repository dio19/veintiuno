"""La checklist de 8 preguntas de business/ideal-customer.md."""

import unittest

from investigacion_hotel.scoring import calificar, LISTA_A, LISTA_B, DESCARTAR, INDETERMINADO
from investigacion_hotel.tests.ayuda import dossier, sin_fuente


def hotel_ideal(**pisar):
    """Un prospecto que puntua 100: sirve de base para variar de a un campo."""
    base = dict(
        pct_resenas_idioma_extranjero=63.0,
        muestra_resenas=30,
        habitaciones=42,
        es_cadena="independiente",
        decisor_nombre="Ana Gomez",
        decisor_rol="Gerenta General",
        decisor_contacto="ana@ejemplo.test",
        decisor_es_generico=False,
        sitio_en_ingles=True,
        motor_reserva_propio=True,
        adr_publicado_ars=95_000,
        barrio="Recoleta",
        menciona_exencion=True,
        publica_precios_usd=True,
    )
    base.update(pisar)
    return dossier(**base)


class TestPuntajes(unittest.TestCase):
    def test_hotel_ideal_suma_100_y_es_lista_a(self):
        r = calificar(hotel_ideal())
        self.assertEqual(r.puntos, 100)
        self.assertEqual(r.lista, LISTA_A)
        self.assertEqual(r.sin_datos, [])

    def test_tramos_de_la_pregunta_1(self):
        for pct, esperado in ((63.0, 20), (50.0, 20), (49.9, 10), (25.0, 10), (24.9, 0)):
            with self.subTest(pct=pct):
                r = calificar(hotel_ideal(pct_resenas_idioma_extranjero=pct))
                self.assertEqual(r.respuestas[0].puntos, esperado)

    def test_tramos_de_habitaciones(self):
        for n, esperado in ((25, 10), (90, 10), (24, 5), (91, 5), (150, 5), (151, 0), (8, 0)):
            with self.subTest(n=n):
                r = calificar(hotel_ideal(habitaciones=n))
                self.assertEqual(r.respuestas[1].puntos, esperado)

    def test_cadena_internacional_no_suma(self):
        r = calificar(hotel_ideal(es_cadena="cadena_internacional"))
        self.assertEqual(r.respuestas[2].puntos, 0)
        self.assertEqual(
            calificar(hotel_ideal(es_cadena="cadena_local")).respuestas[2].puntos, 8
        )

    def test_decisor_generico_puntua_parcial(self):
        r = calificar(
            hotel_ideal(decisor_es_generico=True, decisor_contacto="info@ejemplo.test")
        )
        self.assertEqual(r.respuestas[3].puntos, 6)

    def test_adr_bajo_no_suma(self):
        self.assertEqual(
            calificar(hotel_ideal(adr_publicado_ars=44_000)).respuestas[5].puntos, 0
        )
        self.assertEqual(
            calificar(hotel_ideal(adr_publicado_ars=45_000)).respuestas[5].puntos, 5
        )

    def test_barrio_fuera_del_corredor_puntua_4(self):
        r = calificar(hotel_ideal(barrio="Villa Devoto"))
        self.assertEqual(r.respuestas[6].puntos, 4)

    def test_usd_sin_mencion_de_exencion_puntua_5(self):
        r = calificar(hotel_ideal(menciona_exencion=False, publica_precios_usd=True))
        self.assertEqual(r.respuestas[7].puntos, 5)


class TestReglaDura(unittest.TestCase):
    """'Si la pregunta 1 da menos de 25% y el hotel es de barrio periferico,
    descartar aunque sume 60.' Sin extranjeros no hay producto."""

    def test_descarta_aunque_supere_el_umbral(self):
        d = hotel_ideal(pct_resenas_idioma_extranjero=10.0, barrio="Villa Devoto")
        r = calificar(d)
        self.assertGreaterEqual(r.puntos, 60)
        self.assertEqual(r.lista, DESCARTAR)
        self.assertIn("Regla dura", r.motivo_lista)

    def test_no_aplica_en_barrio_prioritario(self):
        r = calificar(hotel_ideal(pct_resenas_idioma_extranjero=10.0, barrio="Recoleta"))
        self.assertNotEqual(r.lista, DESCARTAR)

    def test_no_aplica_en_barrio_centrico_secundario(self):
        r = calificar(hotel_ideal(pct_resenas_idioma_extranjero=10.0, barrio="San Telmo"))
        self.assertNotEqual(r.lista, DESCARTAR)


class TestUmbrales(unittest.TestCase):
    def test_lista_b_entre_45_y_64(self):
        # 20+10+15+0+0+0+4+0 = 49
        d = dossier(
            pct_resenas_idioma_extranjero=60.0,
            muestra_resenas=30,
            habitaciones=40,
            es_cadena="independiente",
            barrio="Almagro",
            sitio_en_ingles=False,
            motor_reserva_propio=False,
            adr_publicado_ars=30_000,
            menciona_exencion=False,
            publica_precios_usd=False,
            decisor_nombre="Juan Perez",
        )
        r = calificar(d)
        self.assertEqual(r.lista, LISTA_B, r.puntos)


class TestDatosFaltantes(unittest.TestCase):
    """Un 40 por no calificar y un 40 por no encontrar datos no son lo mismo.
    El segundo no se descarta: se completa."""

    def test_sin_pregunta_1_queda_indeterminado(self):
        d = hotel_ideal()
        del d.hallazgos["pct_resenas_idioma_extranjero"]
        r = calificar(d)
        self.assertEqual(r.lista, INDETERMINADO)
        self.assertIn("idioma de las reseñas", r.motivo_lista)

    def test_demasiados_puntos_sin_evaluar_queda_indeterminado(self):
        d = hotel_ideal()
        for campo in ("habitaciones", "es_cadena", "adr_publicado_ars", "barrio"):
            del d.hallazgos[campo]
        r = calificar(d)
        self.assertEqual(r.lista, INDETERMINADO)
        self.assertGreater(r.puntos_no_evaluables, 30)
        self.assertEqual(len(r.sin_datos), 4)

    def test_hallazgo_sin_fuente_no_suma_puntos(self):
        """El corazon del diseno: un dato que el agente no pudo respaldar vale
        exactamente lo mismo que un dato que no encontro."""
        d = hotel_ideal()
        del d.hallazgos["habitaciones"]
        sin_datos_previo = calificar(d)

        sin_fuente(d, "habitaciones", 42)
        con_hallazgo_flojo = calificar(d)

        self.assertEqual(con_hallazgo_flojo.puntos, sin_datos_previo.puntos)
        self.assertEqual(con_hallazgo_flojo.respuestas[1].puntos, 0)
        self.assertFalse(con_hallazgo_flojo.respuestas[1].evaluable)


if __name__ == "__main__":
    unittest.main()
