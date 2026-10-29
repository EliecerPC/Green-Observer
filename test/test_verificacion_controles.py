
import unittest

from core.parametros import Parametros
from core.control import Controlador
from core.modelo import (
    calcular_evaporacion,
    calcular_tasa_humedad,
    calcular_tasa_temperatura,
)


class TestVerificacionControles(unittest.TestCase):

    def setUp(self):
        self.p = Parametros()
        self.controlador = Controlador(self.p)

    def test_riego_se_activa_al_llegar_al_umbral(self):
        eventos = self.controlador.evaluar(
            tiempo=0,
            temperatura=22.0,
            humedad=40.0,
            luz_natural=50.0,
            hora=10.0,
        )

        self.assertTrue(self.controlador.riego)
        self.assertIn("riego_on", [evento[1] for evento in eventos])

    def test_riego_se_mantiene_entre_umbrales(self):
        self.controlador.evaluar(0, 22.0, 35.0, 50.0, 10.0)

        eventos = self.controlador.evaluar(
            1, 22.0, 55.0, 50.0, 10.0
        )

        self.assertTrue(self.controlador.riego)
        self.assertNotIn("riego_off", [evento[1] for evento in eventos])

    def test_riego_se_desactiva_al_llegar_al_umbral(self):
        self.controlador.evaluar(0, 22.0, 35.0, 50.0, 10.0)

        eventos = self.controlador.evaluar(
            1, 22.0, 70.0, 50.0, 10.0
        )

        self.assertFalse(self.controlador.riego)
        self.assertIn("riego_off", [evento[1] for evento in eventos])

    def test_ventilacion_se_activa_al_llegar_al_umbral(self):
        eventos = self.controlador.evaluar(
            0, 30.0, 60.0, 50.0, 10.0
        )

        self.assertTrue(self.controlador.ventilacion)
        self.assertIn("vent_on", [evento[1] for evento in eventos])

    def test_ventilacion_se_mantiene_entre_umbrales(self):
        self.controlador.evaluar(0, 31.0, 60.0, 50.0, 10.0)

        eventos = self.controlador.evaluar(
            1, 28.0, 60.0, 50.0, 10.0
        )

        self.assertTrue(self.controlador.ventilacion)
        self.assertNotIn("vent_off", [evento[1] for evento in eventos])

    def test_ventilacion_se_desactiva_al_llegar_al_umbral(self):
        self.controlador.evaluar(0, 31.0, 60.0, 50.0, 10.0)

        eventos = self.controlador.evaluar(
            1, 27.0, 60.0, 50.0, 10.0
        )

        self.assertFalse(self.controlador.ventilacion)
        self.assertIn("vent_off", [evento[1] for evento in eventos])

    def test_control_desactivado_no_activa_mecanismos(self):
        self.p.control_activo = False
        controlador = Controlador(self.p)

        eventos = controlador.evaluar(
            0, 35.0, 20.0, 0.0, 10.0
        )

        self.assertEqual(eventos, [])
        self.assertFalse(controlador.riego)
        self.assertFalse(controlador.ventilacion)
        self.assertFalse(controlador.luz)

    def test_riego_aumenta_la_tasa_de_humedad(self):
        evaporacion = 0.03

        tasa_sin_riego = calcular_tasa_humedad(0.0, evaporacion)
        tasa_con_riego = calcular_tasa_humedad(
            self.p.aporte_riego, evaporacion
        )

        self.assertAlmostEqual(tasa_sin_riego, -0.03)
        self.assertAlmostEqual(tasa_con_riego, 0.17)
        self.assertGreater(tasa_con_riego, tasa_sin_riego)

    def test_ventilacion_aumenta_el_intercambio_termico(self):
        tasa_sin_ventilacion = calcular_tasa_temperatura(
            30.0, 25.0, 0.0, False, self.p
        )

        tasa_con_ventilacion = calcular_tasa_temperatura(
            30.0, 25.0, 0.0, True, self.p
        )

        self.assertAlmostEqual(tasa_sin_ventilacion, -0.10)
        self.assertAlmostEqual(tasa_con_ventilacion, -0.40)
        self.assertLess(
            tasa_con_ventilacion,
            tasa_sin_ventilacion,
        )

    def test_evaporacion_se_acopla_a_la_temperatura(self):
        evaporacion_25 = calcular_evaporacion(25.0, self.p)
        evaporacion_30 = calcular_evaporacion(30.0, self.p)

        self.assertAlmostEqual(evaporacion_25, 0.03)
        self.assertAlmostEqual(evaporacion_30, 0.036)
        self.assertGreater(evaporacion_30, evaporacion_25)


if __name__ == "__main__":
    unittest.main(verbosity=2)
