
import unittest

from core.parametros import Parametros
from core.modelo import calcular_tasa_humedad
from core.control import Controlador
from core.simulacion import simular, Simulador
from core.modelo import calcular_tasa_temperatura
from core.modelo import calcular_factores_crecimiento
from core.modelo import calcular_tasa_crecimiento


class TestGreenObserver(unittest.TestCase):

    def test_tasa_humedad(self):
        resultado = calcular_tasa_humedad(0.20, 0.03)
        self.assertAlmostEqual(resultado, 0.17)

    def test_rechaza_humedad_invalida(self):
        p = Parametros()
        p.humedad_inicial = 120.0

        with self.assertRaises(ValueError):
            p.validar()

    def test_activa_riego_y_ventilacion(self):
        p = Parametros()
        controlador = Controlador(p)

        eventos = controlador.evaluar(
            tiempo=0,
            temperatura=31.0,
            humedad=35.0,
            luz_natural=10.0,
            hora=10.0,
        )

        tipos = [evento[1] for evento in eventos]

        self.assertIn("riego_on", tipos)
        self.assertIn("vent_on", tipos)
        self.assertTrue(controlador.riego)
        self.assertTrue(controlador.ventilacion)

    def test_simulacion_guarda_todos_los_instantes(self):
        p = Parametros()
        p.duracion = 10.0
        p.paso_tiempo = 1.0

        datos = simular(p)

        self.assertEqual(len(datos["tiempo"]), 11)
        self.assertEqual(datos["tiempo"][0], 0.0)
        self.assertEqual(datos["tiempo"][-1], 10.0)

    def test_humedad_dentro_de_limites(self):
        p = Parametros()
        datos = simular(p)

        self.assertTrue(
            all(0 <= h <= 100 for h in datos["humedad"])
        )

    def test_todos_los_escenarios_son_validos(self):
        from core.escenarios import obtener_escenarios

        escenarios = obtener_escenarios()

        self.assertEqual(len(escenarios), 6)

        for parametros in escenarios.values():
            with self.subTest(escenario=parametros):
                parametros.validar()

    def test_escenario_alta_temperatura(self):
        from core.escenarios import obtener_escenarios

        escenarios = obtener_escenarios()
        p = escenarios["Alta temperatura"]

        self.assertEqual(p.temperatura_media, 29.0)
        self.assertEqual(p.temperatura_inicial, 27.0)

    def test_escenario_sin_control(self):
        from core.escenarios import obtener_escenarios

        p = obtener_escenarios()["Sin control"]

        self.assertFalse(p.control_activo)

    def test_temperaturas_iguales_sin_luz(self):
        p = Parametros()
        tasa = calcular_tasa_temperatura(25.0, 25.0, 0.0, False, p)
        self.assertEqual(tasa, 0.0)

    def test_interior_mas_caliente_que_ambiente(self):
        p = Parametros()
        tasa = calcular_tasa_temperatura(30.0, 25.0, 0.0, False, p)
        self.assertLess(tasa, 0.0)

    def test_interior_mas_frio_que_ambiente(self):
        p = Parametros()
        tasa = calcular_tasa_temperatura(20.0, 25.0, 0.0, False, p)
        self.assertGreater(tasa, 0.0)

    def test_ventilacion_aumenta_intercambio_termico(self):
        p = Parametros()

        tasa_sin_ventilacion = calcular_tasa_temperatura(
            30.0, 25.0, 0.0, False, p
        )

        tasa_con_ventilacion = calcular_tasa_temperatura(
            30.0, 25.0, 0.0, True, p
        )

        self.assertLess(tasa_con_ventilacion, tasa_sin_ventilacion)

    def test_crecimiento_no_supera_limite(self):
        p = Parametros()
        datos = simular(p)

        self.assertTrue(
            all(0 <= valor <= p.crecimiento_limite
                for valor in datos["crecimiento"])
        )

    def test_crecimiento_inicial_se_conserva(self):
        p = Parametros()
        datos = simular(p)

        self.assertAlmostEqual(
            datos["crecimiento"][0],
            p.crecimiento_inicial
        )

    def test_factores_maximos_en_condiciones_optimas(self):
        p = Parametros()

        factor_t, factor_h, factor_l = calcular_factores_crecimiento(
            p.temperatura_optima,
            p.humedad_optima,
            100.0,
            p
        )

        self.assertAlmostEqual(factor_t, 1.0)
        self.assertAlmostEqual(factor_h, 1.0)
        self.assertAlmostEqual(factor_l, 1.0)

    def test_sin_luz_no_hay_crecimiento(self):
        p = Parametros()

        tasa = calcular_tasa_crecimiento(
            p.crecimiento_inicial,
            p.temperatura_optima,
            p.humedad_optima,
            0.0,
            p
        )

        self.assertEqual(tasa, 0.0)

    def test_simulacion_incremental_completa(self):
        p = Parametros()
        p.duracion = 10.0
        p.paso_tiempo = 1.0

        # Ejecución habitual.
        datos_completos = simular(p)

        # Ejecución paso a paso.
        simulador = Simulador(p)

        while not simulador.terminado:
            simulador.paso()

        # Todas las variables deben coincidir.
        self.assertEqual(simulador.datos, datos_completos)

if __name__ == "__main__":
    unittest.main()
