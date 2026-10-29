
import math
import unittest


class TestErrorEuler(unittest.TestCase):

    def setUp(self):
        # Parámetros del modelo térmico simplificado
        self.temperatura_inicial = 22.0
        self.temperatura_ambiental = 25.0
        self.k = 0.02
        self.duracion = 60.0  # minutos

    def calcular_euler(self, dt):
        """Calcula la temperatura mediante el método de Euler."""
        temperatura = self.temperatura_inicial
        tiempo = 0.0

        while tiempo < self.duracion:
            paso = min(dt, self.duracion - tiempo)

            # dT/dt = k * (Tamb - T)
            tasa = self.k * (
                self.temperatura_ambiental - temperatura
            )

            temperatura += tasa * paso
            tiempo += paso

        return temperatura

    def calcular_solucion_exacta(self):
        """Calcula la solución analítica de la ecuación térmica."""
        diferencia = (
            self.temperatura_inicial
            - self.temperatura_ambiental
        )

        return self.temperatura_ambiental + diferencia * math.exp(
            -self.k * self.duracion
        )

    def test_solucion_exacta(self):
        resultado = self.calcular_solucion_exacta()

        self.assertAlmostEqual(
            resultado,
            24.0964,
            places=3
        )

    def test_euler_con_paso_de_un_minuto(self):
        resultado = self.calcular_euler(dt=1.0)
        exacto = self.calcular_solucion_exacta()
        error = abs(resultado - exacto)

        print("\n--- Euler con paso de 1 minuto ---")
        print(f"Temperatura de Euler: {resultado:.6f} °C")
        print(f"Solución exacta:      {exacto:.6f} °C")
        print(f"Error absoluto:       {error:.6f} °C")

        self.assertLess(error, 0.02)

    def test_reducir_paso_disminuye_error(self):
        exacto = self.calcular_solucion_exacta()

        resultado_1 = self.calcular_euler(dt=1.0)
        resultado_05 = self.calcular_euler(dt=0.5)
        resultado_01 = self.calcular_euler(dt=0.1)

        error_1 = abs(resultado_1 - exacto)
        error_05 = abs(resultado_05 - exacto)
        error_01 = abs(resultado_01 - exacto)

        print("\n--- Comparación del error de Euler ---")
        print(f"Paso 1.0 min: error = {error_1:.8f} °C")
        print(f"Paso 0.5 min: error = {error_05:.8f} °C")
        print(f"Paso 0.1 min: error = {error_01:.8f} °C")

        self.assertLess(error_05, error_1)
        self.assertLess(error_01, error_05)


if __name__ == "__main__":
    unittest.main(verbosity=2)
