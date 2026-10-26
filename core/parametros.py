
from dataclasses import dataclass


@dataclass
class Parametros:
    # Condiciones iniciales
    temperatura_inicial: float = 22.0
    humedad_inicial: float = 60.0
    crecimiento_inicial: float = 2.0

    # Duración y tiempo de simulación
    paso_tiempo: float = 1.0
    duracion: float = 1440.0
    hora_inicio: float = 6.0

    # Condiciones ambientales
    temperatura_media: float = 24.0
    amplitud_temperatura: float = 5.0
    luminosidad_maxima: float = 100.0
    nubosidad: float = 0.0

    # Evaporación del agua del suelo
    evaporacion_base: float = 0.03
    factor_evaporacion: float = 0.04
    temperatura_referencia: float = 25.0

    # Modelo de temperatura
    intercambio_termico: float = 0.02
    intercambio_ventilacion: float = 0.06
    efecto_solar: float = 0.0016

    # Modelo de crecimiento de la planta
    crecimiento_maximo: float = 0.002
    crecimiento_limite: float = 50.0
    temperatura_optima: float = 25.0
    tolerancia_temperatura: float = 8.0
    humedad_optima: float = 60.0
    tolerancia_humedad: float = 25.0

    # Control del riego
    humedad_riego_activar: float = 40.0
    humedad_riego_desactivar: float = 70.0

    # Control de la ventilación
    temperatura_ventilacion_activar: float = 30.0
    temperatura_ventilacion_desactivar: float = 27.0

    # Control de la iluminación artificial
    luminosidad_minima: float = 20.0
    luminosidad_artificial: float = 40.0
    hora_luz_inicio: float = 6.0
    hora_luz_fin: float = 20.0
    luz_artificial_activa: bool = False

    # Configuración adicional del modelo
    acoplamiento_activo: bool = True


    # Perturbaciones ambientales
    perturbacion_inicio: float = 0.0
    perturbacion_fin: float = 0.0
    perturbacion_temperatura: float = 0.0

    # Activación del sistema de control
    control_activo: bool = True

    # Aporte de agua cuando el riego está encendido
    aporte_riego: float = 0.20


    def validar(self):
        """Comprueba que los parámetros de la simulación sean coherentes."""

        if self.paso_tiempo <= 0 or self.duracion <= 0:
            raise ValueError(
                "El paso de tiempo y la duración deben ser positivos."
            )

        if self.paso_tiempo > self.duracion:
            raise ValueError(
                "El paso de tiempo no puede superar la duración."
            )

        if self.duracion / self.paso_tiempo > 200_000:
            raise ValueError(
                "La simulación tiene demasiados pasos de tiempo."
            )

        if not 0 <= self.humedad_inicial <= 100:
            raise ValueError(
                "La humedad inicial debe estar entre 0 y 100 %."
            )

        if self.crecimiento_inicial < 0:
            raise ValueError(
                "El crecimiento inicial no puede ser negativo."
            )

        if self.crecimiento_limite <= 0:
            raise ValueError(
                "El límite de crecimiento debe ser positivo."
            )

        if self.crecimiento_inicial > self.crecimiento_limite:
            raise ValueError(
                "El crecimiento inicial supera el límite establecido."
            )

        if not 0 <= self.nubosidad <= 1:
            raise ValueError(
                "La nubosidad debe estar entre 0 y 1."
            )

        if self.humedad_riego_activar >= self.humedad_riego_desactivar:
            raise ValueError(
                "El umbral de activación del riego debe ser menor "
                "que el de desactivación."
            )

        if (
            self.temperatura_ventilacion_desactivar
            >= self.temperatura_ventilacion_activar
        ):
            raise ValueError(
                "El umbral de desactivación de la ventilación "
                "debe ser menor que el de activación."
            )

        if self.tolerancia_temperatura <= 0:
            raise ValueError(
                "La tolerancia de temperatura debe ser positiva."
            )

        if self.tolerancia_humedad <= 0:
            raise ValueError(
                "La tolerancia de humedad debe ser positiva."
            )

        if self.luminosidad_maxima < 0:
            raise ValueError(
                "La luminosidad máxima no puede ser negativa."
            )

        if not 0 <= self.luminosidad_minima <= 100:
            raise ValueError(
                "La luminosidad mínima debe estar entre 0 y 100."
            )

        if not 0 <= self.luminosidad_artificial <= 100:
            raise ValueError(
                "La luminosidad artificial debe estar entre 0 y 100."
            )

        if not 0 <= self.hora_luz_inicio < 24:
            raise ValueError(
                "La hora inicial de iluminación debe estar entre 0 y 24."
            )

        if not 0 <= self.hora_luz_fin <= 24:
            raise ValueError(
                "La hora final de iluminación debe estar entre 0 y 24."
            )

        if self.aporte_riego < 0 or self.evaporacion_base < 0:
            raise ValueError(
                "El aporte de riego y la evaporación no pueden ser negativos."
            )


