
import unittest

from core.parametros import Parametros
from core.modelo import (
    calcular_temperatura_ambiental,
    calcular_evaporacion,
    calcular_tasa_humedad,
    calcular_tasa_temperatura,
)


class TestVerificacionModelo(unittest.TestCase):

    def setUp(self):
        self.p = Parametros()

    def test_temperatura_ambiental_a_las_15(self):
        # Inicio: 06:00. Tiempo transcurrido: 9 horas.
        resultado = calcular_temperatura_ambiental(540, self.p)

        # 24 + 5 * sin(pi / 2) = 29 °C.
        self.assertAlmostEqual(resultado, 29.0, places=6)

    def test_evaporacion_a_30_grados(self):
        # 0.03 * [1 + 0.04 * (30 - 25)] = 0.036.
        resultado = calcular_evaporacion(30.0, self.p)

        self.assertAlmostEqual(resultado, 0.036, places=6)

    def test_tasa_humedad_con_riego(self):
        # Aporte de 0.20 menos evaporación de 0.03.
        resultado = calcular_tasa_humedad(0.20, 0.03)

        self.assertAlmostEqual(resultado, 0.17, places=6)

    def test_tasa_temperatura_sin_ventilacion(self):
        # 0.02 * (25 - 22) = 0.06 °C por minuto.
        resultado = calcular_tasa_temperatura(
            temperatura=22.0,
            temperatura_ambiental=25.0,
            luminosidad=0.0,
            ventilando=False,
            p=self.p,
        )

        self.assertAlmostEqual(resultado, 0.06, places=6)


if __name__ == "__main__":
    unittest.main()
