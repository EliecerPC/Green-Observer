
from core.parametros import Parametros
from core.simulacion import simular

p = Parametros()

# Ejecutar una simulación de 24 horas.
datos = simular(p)

print("Cantidad de instantes:", len(datos["tiempo"]))
print("Temperatura inicial:", datos["temperatura"][0])
print("Temperatura final:", datos["temperatura"][-1])
print("Humedad inicial:", datos["humedad"][0])
print("Humedad final:", datos["humedad"][-1])
print("Crecimiento inicial:", datos["crecimiento"][0])
print("Crecimiento final:", datos["crecimiento"][-1])

print("\nEventos registrados:")
for evento in datos["eventos"]:
    print(evento)
