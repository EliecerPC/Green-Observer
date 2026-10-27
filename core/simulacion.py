
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


def simular(p: Parametros) -> dict:
    """Ejecuta la simulación y devuelve los datos de cada instante."""

    def simular(p: Parametros) -> dict:
        """Ejecuta la simulación y devuelve los datos de cada instante."""

        p.validar()
        controlador = Controlador(p)

    controlador = Controlador(p)

    tiempo = 0.0
    temperatura = p.temperatura_inicial
    humedad = p.humedad_inicial
    crecimiento = p.crecimiento_inicial

    datos = {
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

    while tiempo <= p.duracion + 1e-9:
        hora = calcular_hora_del_dia(tiempo, p)

        # 1. Calcular las condiciones ambientales.
        temperatura_ambiental = calcular_temperatura_ambiental(
            tiempo, p
        )
        luz_natural = calcular_luminosidad_natural(tiempo, p)

        # 2. Evaluar los mecanismos de control.
        eventos = controlador.evaluar(
            tiempo,
            temperatura,
            humedad,
            luz_natural,
            hora,
        )
        datos["eventos"].extend(eventos)

        # La luz artificial se suma a la natural, sin superar el 100 %.
        luz_artificial = (
            p.luminosidad_artificial if controlador.luz else 0.0
        )
        luminosidad_total = min(
            100.0, luz_natural + luz_artificial
        )

        # 3. Calcular las tasas de cambio.
        evaporacion = calcular_evaporacion(temperatura, p)

        aporte_riego = (
            p.aporte_riego if controlador.riego else 0.0
        )
        tasa_humedad = calcular_tasa_humedad(
            aporte_riego, evaporacion
        )

        tasa_temperatura = calcular_tasa_temperatura(
            temperatura,
            temperatura_ambiental,
            luminosidad_total,
            controlador.ventilacion,
            p,
        )

        tasa_crecimiento = calcular_tasa_crecimiento(
            crecimiento,
            temperatura,
            humedad,
            luminosidad_total,
            p,
        )

        # Guardar los valores intermedios de este instante.
        datos["aporte_riego"].append(aporte_riego)
        datos["tasa_humedad"].append(tasa_humedad)
        datos["tasa_temperatura"].append(tasa_temperatura)
        datos["tasa_crecimiento"].append(tasa_crecimiento)

        # 4. Guardar el estado actual para las gráficas y los informes.
        datos["tiempo"].append(tiempo)
        datos["hora"].append(hora)
        datos["temperatura"].append(temperatura)
        datos["temperatura_ambiental"].append(
            temperatura_ambiental
        )
        datos["humedad"].append(humedad)
        datos["crecimiento"].append(crecimiento)
        datos["luminosidad_natural"].append(luz_natural)
        datos["luminosidad_total"].append(luminosidad_total)
        datos["evaporacion"].append(evaporacion)
        datos["riego"].append(controlador.riego)
        datos["ventilacion"].append(controlador.ventilacion)
        datos["luz_artificial"].append(controlador.luz)

        # Determinar cuánto tiempo abarca el siguiente paso.
        # En el último instante no se aplica un nuevo paso.
        if tiempo >= p.duracion - 1e-9:
            dt = 0.0
        else:
            dt = min(p.paso_tiempo, p.duracion - tiempo)

        datos["paso_aplicado"].append(dt)

        # Si llegamos al final, no hay otro estado que calcular.
        if dt == 0.0:
            break

        humedad += tasa_humedad * dt
        temperatura += tasa_temperatura * dt
        crecimiento += tasa_crecimiento * dt

        # Mantener las variables dentro de sus límites físicos.
        humedad = min(100.0, max(0.0, humedad))
        crecimiento = min(
            p.crecimiento_limite,
            max(0.0, crecimiento),
        )

        tiempo += dt

    return datos
