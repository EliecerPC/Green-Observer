
from core.parametros import Parametros
from core.modelo import (
    calcular_hora_del_dia,
    calcular_temperatura_ambiental,
    calcular_luminosidad_natural,
    calcular_evaporacion,
    calcular_tasa_humedad,
    calcular_tasa_temperatura,
    calcular_tasa_crecimiento,
)
from core.control import Controlador


def _crear_datos() -> dict:
    """Crea la estructura donde se guardarán los resultados."""
    return {
        "tiempo": [],
        "hora": [],
        "temperatura": [],
        "temperatura_ambiental": [],
        "humedad": [],
        "crecimiento": [],
        "luminosidad_natural": [],
        "luminosidad_total": [],
        "evaporacion": [],
        "riego": [],
        "ventilacion": [],
        "luz_artificial": [],
        "eventos": [],
        "aporte_riego": [],
        "tasa_humedad": [],
        "tasa_temperatura": [],
        "tasa_crecimiento": [],
        "paso_aplicado": [],
    }


class Simulador:
    """Permite ejecutar la simulación un instante a la vez."""

    def __init__(self, p: Parametros):
        self.p = p
        self.p.validar()
        self.reiniciar()

    def reiniciar(self):
        """Restablece las condiciones iniciales del invernadero."""
        self.controlador = Controlador(self.p)
        self.tiempo = 0.0
        self.temperatura = self.p.temperatura_inicial
        self.humedad = self.p.humedad_inicial
        self.crecimiento = self.p.crecimiento_inicial
        self.datos = _crear_datos()
        self.terminado = False

    def paso(self) -> dict | None:
        """
        Registra el instante actual y calcula el siguiente estado
        usando el método de Euler.

        Devuelve los datos del instante registrado.
        Devuelve None cuando la simulación ya terminó.
        """
        if self.terminado:
            return None

        p = self.p
        tiempo = self.tiempo
        temperatura = self.temperatura
        humedad = self.humedad
        crecimiento = self.crecimiento

        hora = calcular_hora_del_dia(tiempo, p)
        temperatura_ambiental = calcular_temperatura_ambiental(
            tiempo, p
        )
        luz_natural = calcular_luminosidad_natural(tiempo, p)

        eventos = self.controlador.evaluar(
            tiempo,
            temperatura,
            humedad,
            luz_natural,
            hora,
        )
        self.datos["eventos"].extend(eventos)

        luz_artificial = (
            p.luminosidad_artificial
            if self.controlador.luz
            else 0.0
        )
        luminosidad_total = min(
            100.0, luz_natural + luz_artificial
        )

        evaporacion = calcular_evaporacion(temperatura, p)

        aporte_riego = (
            p.aporte_riego if self.controlador.riego else 0.0
        )
        tasa_humedad = calcular_tasa_humedad(
            aporte_riego, evaporacion
        )

        tasa_temperatura = calcular_tasa_temperatura(
            temperatura,
            temperatura_ambiental,
            luminosidad_total,
            self.controlador.ventilacion,
            p,
        )

        tasa_crecimiento = calcular_tasa_crecimiento(
            crecimiento,
            temperatura,
            humedad,
            luminosidad_total,
            p,
        )

        if tiempo >= p.duracion - 1e-9:
            dt = 0.0
        else:
            dt = min(p.paso_tiempo, p.duracion - tiempo)

        # Guardar todos los resultados del instante actual.
        valores = {
            "tiempo": tiempo,
            "hora": hora,
            "temperatura": temperatura,
            "temperatura_ambiental": temperatura_ambiental,
            "humedad": humedad,
            "crecimiento": crecimiento,
            "luminosidad_natural": luz_natural,
            "luminosidad_total": luminosidad_total,
            "evaporacion": evaporacion,
            "riego": self.controlador.riego,
            "ventilacion": self.controlador.ventilacion,
            "luz_artificial": self.controlador.luz,
            "aporte_riego": aporte_riego,
            "tasa_humedad": tasa_humedad,
            "tasa_temperatura": tasa_temperatura,
            "tasa_crecimiento": tasa_crecimiento,
            "paso_aplicado": dt,
        }

        for clave, valor in valores.items():
            self.datos[clave].append(valor)

        if dt == 0.0:
            self.terminado = True
        else:
            # Método de Euler: nuevo estado = estado + tasa * dt.
            self.humedad = min(
                100.0,
                max(0.0, humedad + tasa_humedad * dt),
            )
            self.temperatura = (
                temperatura + tasa_temperatura * dt
            )
            self.crecimiento = min(
                p.crecimiento_limite,
                max(0.0, crecimiento + tasa_crecimiento * dt),
            )
            self.tiempo += dt

        return valores


def simular(p: Parametros) -> dict:
    """Ejecuta todos los pasos y devuelve los resultados completos."""
    simulador = Simulador(p)

    while not simulador.terminado:
        simulador.paso()

    return simulador.datos
