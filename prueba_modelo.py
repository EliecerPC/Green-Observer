
from core.parametros import Parametros
from core.modelo import (
    calcular_temperatura_ambiental,
    calcular_luminosidad_natural,
    calcular_evaporacion,
    calcular_tasa_humedad,
    calcular_tasa_temperatura,
    calcular_tasa_crecimiento,
)

p = Parametros()

# A las 15:00 han transcurrido 9 horas desde las 06:00.
tiempo = 9 * 60

temperatura_exterior = calcular_temperatura_ambiental(tiempo, p)
luz = calcular_luminosidad_natural(tiempo, p)
evaporacion = calcular_evaporacion(30.0, p)

print("Temperatura exterior:", temperatura_exterior)
print("Luminosidad natural:", luz)
print("Evaporación a 30 °C:", evaporacion)

print("Tasa de humedad:", calcular_tasa_humedad(0.8, evaporacion))

print(
    "Tasa de temperatura:",
    calcular_tasa_temperatura(22, temperatura_exterior, luz, False, p)
)

print(
    "Tasa de crecimiento:",
    calcular_tasa_crecimiento(2, 22, 60, luz, p)
)
