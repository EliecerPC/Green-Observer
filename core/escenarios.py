
from dataclasses import replace

from core.parametros import Parametros


def obtener_escenarios() -> dict[str, Parametros]:
    """Devuelve las configuraciones disponibles para la simulación."""

    base = Parametros()

    return {
        "Día normal": base,

        "Baja humedad": replace(
            base,
            humedad_inicial=45.0,
            evaporacion_base=0.06,
            aporte_riego=0.30,
        ),

        "Alta temperatura": replace(
            base,
            temperatura_media=29.0,
            temperatura_inicial=27.0,
        ),

        "Poca luz / nublado": replace(
            base,
            nubosidad=0.75,
            luz_artificial_activa=True,
        ),

        "Ola de calor": replace(
            base,
            perturbacion_inicio=360.0,
            perturbacion_fin=720.0,
            perturbacion_temperatura=6.0,
        ),

        "Sin control": replace(
            base,
            control_activo=False,
        ),
    }
