
import tkinter as tk
from tkinter import ttk
from core.escenarios import obtener_escenarios
from core.simulacion import simular


def main():
    ventana = tk.Tk()
    escenarios = obtener_escenarios()
    ventana.title("Green Observer - Control Center")
    ventana.geometry("900x600")
    ventana.minsize(700, 450)

    titulo = ttk.Label(
        ventana,
        text="Green Observer",
        font=("Arial", 22, "bold")
    )
    titulo.pack(pady=(25, 5))

    subtitulo = ttk.Label(
        ventana,
        text="Centro de control del invernadero virtual",
        font=("Arial", 11)
    )
    subtitulo.pack(pady=(0, 20))

    contenido = ttk.Frame(ventana, padding=20)
    contenido.pack(fill="both", expand=True)

    indicadores = ttk.Frame(contenido)
    indicadores.pack(fill="x", pady=15)

    indicador_temperatura = ttk.Label(
        indicadores,
        text="Temperatura\n-- °C",
        font=("Arial", 14, "bold"),
        anchor="center"
    )
    indicador_temperatura.pack(side="left", expand=True, fill="x", padx=5)

    indicador_humedad = ttk.Label(
        indicadores,
        text="Humedad del suelo\n-- %",
        font=("Arial", 14, "bold"),
        anchor="center"
    )
    indicador_humedad.pack(side="left", expand=True, fill="x", padx=5)

    indicador_crecimiento = ttk.Label(
        indicadores,
        text="Crecimiento\n--",
        font=("Arial", 14, "bold"),
        anchor="center"
    )
    indicador_crecimiento.pack(side="left", expand=True, fill="x", padx=5)

    selector = ttk.Combobox(
        contenido,
        values=list(escenarios.keys()),
        state="readonly",
        width=30
    )
    selector.pack(pady=10)
    selector.set("Día normal")

    def ejecutar_simulacion():
        nombre = selector.get()
        parametros = escenarios[nombre]
        resultados = simular(parametros)

        indicador_temperatura.config(
            text=f"Temperatura\n{resultados['temperatura'][-1]:.2f} °C"
        )

        indicador_humedad.config(
            text=f"Humedad del suelo\n{resultados['humedad'][-1]:.2f} %"
        )

        indicador_crecimiento.config(
            text=f"Crecimiento\n{resultados['crecimiento'][-1]:.4f}"
        )

        mensaje.config(text=f"Simulación completada: {nombre}")

    boton = ttk.Button(
        contenido,
        text="Ejecutar simulación",
        command=ejecutar_simulacion
    )
    boton.pack(pady=10)

    mensaje = ttk.Label(
        contenido,
        text="Sistema preparado para iniciar.",
        font=("Arial", 12)
    )
    mensaje.pack(pady=20)

    ventana.mainloop()


if __name__ == "__main__":
    main()
