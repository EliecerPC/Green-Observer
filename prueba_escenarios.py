
from core.escenarios import obtener_escenarios
from core.simulacion import simular

escenarios = obtener_escenarios()

for nombre, parametros in escenarios.items():
    parametros.validar()
    datos = simular(parametros)

    temperatura_maxima = max(datos["temperatura"])
    temperatura_minima = min(datos["temperatura"])
    humedad_minima = min(datos["humedad"])

    print(f"\n--- {nombre} ---")
    print("Temperatura inicial:", datos["temperatura"][0], "°C")
    print("Temperatura final:", round(datos["temperatura"][-1], 2), "°C")
    print("Humedad inicial:", datos["humedad"][0], "%")
    print("Humedad final:", round(datos["humedad"][-1], 2), "%")
    print("Eventos registrados:", len(datos["eventos"]))
    for evento in datos["eventos"]:
        print(evento)
    print(f"Temperatura máxima: {temperatura_maxima:.2f} °C")
    print(f"Temperatura mínima: {temperatura_minima:.2f} °C")
    print(f"Humedad mínima: {humedad_minima:.2f} %")
