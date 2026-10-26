
import math

from core.parametros import Parametros


def calcular_hora_del_dia(tiempo: float, p: Parametros) -> float:
    """Devuelve la hora del día para un tiempo transcurrido en minutos."""
    return (p.hora_inicio + tiempo / 60.0) % 24.0


def calcular_temperatura_ambiental(
    tiempo: float, p: Parametros
) -> float:
    """Temperatura exterior según la hora y las perturbaciones."""
    hora = calcular_hora_del_dia(tiempo, p)

    temperatura = p.temperatura_media + (
        p.amplitud_temperatura
        * math.sin(2 * math.pi * (hora - 9.0) / 24.0)
    )

    if p.perturbacion_inicio <= tiempo < p.perturbacion_fin:
        temperatura += p.perturbacion_temperatura

    return temperatura


def calcular_luminosidad_natural(
    tiempo: float, p: Parametros
) -> float:
    """Luminosidad natural según la hora y la nubosidad."""
    hora = calcular_hora_del_dia(tiempo, p)

    altura_solar = max(
        0.0,
        math.sin(2 * math.pi * (hora - 6.0) / 24.0)
    )

    return (
        p.luminosidad_maxima
        * (1.0 - p.nubosidad)
        * altura_solar
    )


def calcular_evaporacion(
    temperatura: float, p: Parametros
) -> float:
    """Evaporación del suelo en porcentaje por minuto."""
    if p.acoplamiento_activo:
        factor = 1.0 + p.factor_evaporacion * (
            temperatura - p.temperatura_referencia
        )
        return max(0.0, p.evaporacion_base * factor)

    return p.evaporacion_base


def calcular_tasa_humedad(
    aporte_riego: float, evaporacion: float
) -> float:
    """dH/dt = riego - evaporación."""
    return aporte_riego - evaporacion


def calcular_tasa_temperatura(
    temperatura: float,
    temperatura_ambiental: float,
    luminosidad: float,
    ventilando: bool,
    p: Parametros
) -> float:
    """Tasa de cambio de la temperatura interior."""
    intercambio = p.intercambio_termico

    if ventilando:
        intercambio += p.intercambio_ventilacion

    return (
        intercambio * (temperatura_ambiental - temperatura)
        + p.efecto_solar * luminosidad
    )


def calcular_factores_crecimiento(
    temperatura: float,
    humedad: float,
    luminosidad: float,
    p: Parametros
) -> tuple[float, float, float]:
    """Factores de temperatura, humedad y luz, entre 0 y 1."""
    factor_temperatura = math.exp(
        -((temperatura - p.temperatura_optima)
          / p.tolerancia_temperatura) ** 2
    )

    factor_humedad = math.exp(
        -((humedad - p.humedad_optima)
          / p.tolerancia_humedad) ** 2
    )

    factor_luz = min(1.0, max(0.0, luminosidad / 100.0))

    return factor_temperatura, factor_humedad, factor_luz


def calcular_tasa_crecimiento(
    crecimiento: float,
    temperatura: float,
    humedad: float,
    luminosidad: float,
    p: Parametros
) -> float:
    """Tasa de crecimiento logístico de la planta."""
    factor_t, factor_h, factor_l = calcular_factores_crecimiento(
        temperatura, humedad, luminosidad, p
    )

    return (
        p.crecimiento_maximo
        * factor_t
        * factor_h
        * factor_l
        * crecimiento
        * (1.0 - crecimiento / p.crecimiento_limite)
    )
