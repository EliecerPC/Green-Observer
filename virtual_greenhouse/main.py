
import tkinter as tk
from tkinter import ttk
import math

from core.escenarios import obtener_escenarios
from core.simulacion import Simulador

def mezclar_colores(color1, color2, proporcion):
    """Mezcla dos colores hexadecimales."""
    proporcion = max(0.0, min(1.0, proporcion))

    r1 = int(color1[1:3], 16)
    g1 = int(color1[3:5], 16)
    b1 = int(color1[5:7], 16)

    r2 = int(color2[1:3], 16)
    g2 = int(color2[3:5], 16)
    b2 = int(color2[5:7], 16)

    r = int(r1 + (r2 - r1) * proporcion)
    g = int(g1 + (g2 - g1) * proporcion)
    b = int(b1 + (b2 - b1) * proporcion)

    return f"#{r:02x}{g:02x}{b:02x}"


def abrir_invernadero():
    ventana = tk.Toplevel()
    ventana.title("Green Observer - Invernadero Virtual")

    # Abrir maximizada y bloquear cambios de tamaño.
    ventana.state("zoomed")
    ventana.resizable(False, False)

    # Obtener el escenario y ejecutar el modelo matemático.
    escenarios = obtener_escenarios()
    parametros = escenarios["Día normal"]

    simulador = Simulador(parametros)

    # Calcular y guardar el estado inicial (t = 0).
    simulador.paso()
    resultados = simulador.datos

    # Panel de indicadores.
    panel_datos = ttk.Frame(ventana)
    panel_datos.pack(pady=5)

    etiqueta_temperatura = ttk.Label(
        panel_datos,
        text=f"Temperatura: {resultados['temperatura'][0]:.1f} °C"
    )
    etiqueta_temperatura.pack(side="left", padx=15)

    etiqueta_humedad = ttk.Label(
        panel_datos,
        text=f"Humedad: {resultados['humedad'][0]:.1f} %"
    )
    etiqueta_humedad.pack(side="left", padx=15)

    etiqueta_luminosidad = ttk.Label(
        panel_datos,
        text=f"Luminosidad: {resultados['luminosidad_total'][0]:.1f}"
    )
    etiqueta_luminosidad.pack(side="left", padx=15)

    # Título.
    ttk.Label(
        ventana,
        text="Invernadero Virtual",
        font=("Arial", 20, "bold")
    ).pack(pady=10)

    # Escena visual de tamaño fijo.
    escena = tk.Canvas(
        ventana,
        width=1000,
        height=600,
        bg="#DCEFD5",
        highlightthickness=0
    )
    escena.pack(padx=15, pady=5)

    # Cielo y astros.
    cielo = escena.create_rectangle(
        0, 0, 1000, 420,
        fill="#87CEEB",
        outline=""
    )

    sol = escena.create_oval(
        780, 50, 840, 110,
        fill="#FFD54F",
        outline=""
    )

    luna = escena.create_oval(
        150, 50, 205, 105,
        fill="#F5F5F5",
        outline=""
    )
    escena.itemconfigure(luna, state="hidden")

    # Suelo.
    suelo = escena.create_rectangle(
        80, 420, 920, 520,
        fill="#795548",
        outline=""
    )

    # Estructura del invernadero.
    techo = escena.create_polygon(
        80, 200,
        500, 60,
        920, 200,
        outline="#557C55",
        fill="#EFF8E9",
        width=5
    )

    pared_izquierda = escena.create_line(
        80, 200, 80, 420,
        fill="#557C55",
        width=5
    )

    pared_derecha = escena.create_line(
        920, 200, 920, 420,
        fill="#557C55",
        width=5
    )

    columna_central = escena.create_line(
        500, 60, 500, 420,
        fill="#557C55",
        width=3
    )

    # Plantas vinculadas al crecimiento del modelo.
    plantas = []

    for x in (220, 380, 620, 780):
        tallo = escena.create_line(
            x, 420, x, 380,
            fill="#38783B",
            width=5
        )

        hoja_izquierda = escena.create_oval(
            x - 30, 365,
            x, 390,
            fill="#4DAD55",
            outline=""
        )

        hoja_derecha = escena.create_oval(
            x, 355,
            x + 30, 380,
            fill="#388E3C",
            outline=""
        )

        plantas.append(
            (x, tallo, hoja_izquierda, hoja_derecha)
        )

    # Variables de control de la simulación.
    indice_actual = 0
    tarea_actualizacion = None
    pausado = False
    velocidad_var = tk.StringVar(value="1x")

    def actualizar_datos():
        nonlocal indice_actual, tarea_actualizacion

        if indice_actual >= len(resultados["tiempo"]):
            if simulador.terminado:
                tarea_actualizacion = None
                return

            # Calcular el siguiente instante cuando sea necesario.
            simulador.paso()

        # Actualizar los indicadores.
        etiqueta_temperatura.config(
            text=(
                f"Temperatura: "
                f"{resultados['temperatura'][indice_actual]:.1f} °C"
            )
        )

        etiqueta_humedad.config(
            text=(
                f"Humedad: "
                f"{resultados['humedad'][indice_actual]:.1f} %"
            )
        )

        etiqueta_luminosidad.config(
            text=(
                f"Luminosidad: "
                f"{resultados['luminosidad_total'][indice_actual]:.1f}"
            )
        )

        # Obtener valores calculados por el modelo.
        crecimiento = resultados["crecimiento"][indice_actual]
        hora = resultados["hora"][indice_actual]
        luminosidad = resultados["luminosidad_natural"][indice_actual]

        # Actualizar el cielo, el sol y la luna.
        if 6 <= hora < 18:
            escena.itemconfigure(sol, state="normal")
            escena.itemconfigure(luna, state="hidden")

            progreso = (hora - 6) / 12

            posicion_x = 100 + progreso * 800
            posicion_y = 350 - 250 * math.sin(math.pi * progreso)

            escena.coords(
                sol,
                posicion_x - 30, posicion_y - 30,
                posicion_x + 30, posicion_y + 30
            )

            # Color del cielo según la luminosidad natural.
            if luminosidad >= 70:
                color_cielo = "#87CEEB"

            elif luminosidad >= 30:
                proporcion = (luminosidad - 30) / 40

                color_cielo = mezclar_colores(
                    "#5B9BD5",
                    "#87CEEB",
                    proporcion
                )

            else:
                proporcion = luminosidad / 30

                color_cielo = mezclar_colores(
                    "#F0A35E",
                    "#5B9BD5",
                    proporcion
                )

            escena.itemconfigure(cielo, fill=color_cielo)

        else:
            escena.itemconfigure(sol, state="hidden")
            escena.itemconfigure(luna, state="normal")

            hora_nocturna = (
                hora - 18 if hora >= 18 else hora + 6
            )

            progreso = hora_nocturna / 12

            posicion_x = 100 + progreso * 800
            posicion_y = 350 - 250 * math.sin(math.pi * progreso)

            escena.coords(
                luna,
                posicion_x - 27, posicion_y - 27,
                posicion_x + 27, posicion_y + 27
            )

            escena.itemconfigure(cielo, fill="#172554")

        # Actualizar el tamaño de las plantas.
        altura = (
            25
            + (crecimiento / parametros.crecimiento_limite) * 100
        )

        for x, tallo, hoja_izquierda, hoja_derecha in plantas:
            punta_tallo = 420 - altura

            escena.coords(
                tallo,
                x, 420,
                x, punta_tallo
            )

            escena.coords(
                hoja_izquierda,
                x - 30, punta_tallo - 15,
                x, punta_tallo + 5
            )

            escena.coords(
                hoja_derecha,
                x, punta_tallo - 25,
                x + 30, punta_tallo - 5
            )

        # Avanzar al siguiente instante simulado.
        indice_actual += 1

        if not simulador.terminado:
            velocidad = float(
                velocidad_var.get().replace("x", "")
            )

            intervalo = int(1000 / velocidad)

            tarea_actualizacion = ventana.after(
                intervalo,
                actualizar_datos
            )
        else:
            tarea_actualizacion = None

    def pausar_simulacion():
        nonlocal tarea_actualizacion, pausado

        pausado = True

        if tarea_actualizacion is not None:
            ventana.after_cancel(tarea_actualizacion)
            tarea_actualizacion = None

    def iniciar_simulacion():
        nonlocal tarea_actualizacion, pausado

        if tarea_actualizacion is None and not simulador.terminado:
            pausado = False

            velocidad = float(
                velocidad_var.get().replace("x", "")
            )

            intervalo = int(1000 / velocidad)

            tarea_actualizacion = ventana.after(
                intervalo,
                actualizar_datos
            )

    def reiniciar_simulacion():
        nonlocal indice_actual, tarea_actualizacion, pausado, resultados

        if tarea_actualizacion is not None:
            ventana.after_cancel(tarea_actualizacion)

        simulador.reiniciar()
        simulador.paso()
        resultados = simulador.datos

        indice_actual = 0
        pausado = False
        tarea_actualizacion = None

        actualizar_datos()

    # Panel de controles.
    panel_controles = ttk.Frame(ventana)
    panel_controles.pack(pady=5)

    ttk.Label(
        panel_controles,
        text="Velocidad:"
    ).pack(side="left", padx=5)

    selector_velocidad = ttk.Combobox(
        panel_controles,
        textvariable=velocidad_var,
        values=("1x", "2x", "5x", "10x"),
        state="readonly",
        width=5
    )
    selector_velocidad.pack(side="left", padx=5)

    ttk.Button(
        panel_controles,
        text="Iniciar",
        command=iniciar_simulacion
    ).pack(side="left", padx=5)

    ttk.Button(
        panel_controles,
        text="Pausar",
        command=pausar_simulacion
    ).pack(side="left", padx=5)

    ttk.Button(
        panel_controles,
        text="Reiniciar",
        command=reiniciar_simulacion
    ).pack(side="left", padx=5)

    # Texto de apoyo.
    escena.create_text(
        500, 565,
        text="Simulación visual basada en el modelo matemático",
        font=("Arial", 11)
    )

    # Mostrar el estado inicial.
    actualizar_datos()


if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.withdraw()
    abrir_invernadero()
    raiz.mainloop()
