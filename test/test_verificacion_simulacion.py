
import unittest

from core.parametros import Parametros
from core.simulacion import Simulador, simular


class TestVerificacionSimulacion(unittest.TestCase):

    def setUp(self):
        # Configuramos un caso sencillo y controlado.
        self.p = Parametros()
        self.p.temperatura_inicial = 22.0
        self.p.temperatura_media = 25.0
        self.p.amplitud_temperatura = 0.0
        self.p.intercambio_termico = 0.02
        self.p.efecto_solar = 0.0

        self.p.humedad_inicial = 60.0
        self.p.evaporacion_base = 0.0

        self.p.control_activo = False
        self.p.paso_tiempo = 1.0
        self.p.duracion = 2.0

    def test_temperatura_se_actualiza_con_euler(self):
        simulador = Simulador(self.p)

        simulador.paso()

        # Primer paso:
        # T nueva = 22 + 0.02 * (25 - 22) * 1
        self.assertAlmostEqual(
            simulador.temperatura,
            22.06,
            places=6,
        )

        simulador.paso()

        # Segundo paso:
        # T nueva = 22.06 + 0.02 * (25 - 22.06) * 1
        self.assertAlmostEqual(
            simulador.temperatura,
            22.1188,
            places=6,
        )

    def test_humedad_permanece_constante_sin_aporte_ni_evaporacion(self):
        simulador = Simulador(self.p)

        simulador.paso()
        simulador.paso()

        self.assertAlmostEqual(simulador.humedad, 60.0)

    def test_datos_registrados_corresponden_a_cada_instante(self):
        datos = simular(self.p)

        self.assertEqual(
            datos["tiempo"],
            [0.0, 1.0, 2.0],
        )

        self.assertAlmostEqual(datos["temperatura"][0], 22.0)
        self.assertAlmostEqual(datos["temperatura"][1], 22.06)
        self.assertAlmostEqual(datos["temperatura"][2], 22.1188)

        self.assertEqual(
            datos["humedad"],
            [60.0, 60.0, 60.0],
        )

    def test_paso_final_no_modifica_el_estado(self):
        simulador = Simulador(self.p)

        while not simulador.terminado:
            simulador.paso()

        temperatura_final = simulador.temperatura
        humedad_final = simulador.humedad
        tiempo_final = simulador.tiempo

        resultado = simulador.paso()

        self.assertIsNone(resultado)
        self.assertEqual(simulador.temperatura, temperatura_final)
        self.assertEqual(simulador.humedad, humedad_final)
        self.assertEqual(simulador.tiempo, tiempo_final)


if __name__ == "__main__":
    unittest.main(verbosity=2)
