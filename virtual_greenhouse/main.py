
import tkinter as tk
from tkinter import ttk, messagebox
import math

from core.sesion_simulacion import SesionSimulacion
from core.escenarios import obtener_escenarios

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


def abrir_invernadero(
    sesion=None,
    al_ejecutar=None,
    abrir_control_center=None
):
    ventana = tk.Toplevel()
    ventana.title("Green Observer - Invernadero Virtual")


    # Obtener los parámetros y resultados de la sesión compartida.
    parametros = sesion.simulador.p if sesion is not None else None
    resultados = sesion.resultados if sesion is not None else None

    # Panel de indicadores.
    panel_datos = ttk.Frame(ventana)
    panel_datos.pack(pady=5)

    etiqueta_temperatura = ttk.Label(
        panel_datos,
        text=(
            f"Temperatura: {resultados['temperatura'][0]:.2f} °C"
            if resultados is not None else "Temperatura: -- °C"
        )
    )
    etiqueta_temperatura.pack(side="left", padx=15)

    etiqueta_humedad = ttk.Label(
        panel_datos,
        text=(
            f"Humedad: {resultados['humedad'][0]:.2f} %"
            if resultados is not None else "Humedad: -- %"
        )
    )
    etiqueta_humedad.pack(side="left", padx=15)

    etiqueta_luminosidad = ttk.Label(
        panel_datos,
        text=(
            f"Luminosidad: {resultados['luminosidad_total'][0]:.2f}"
            if resultados is not None else "Luminosidad: --"
        )
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

    escena.pack(
        padx=10,
        pady=5,
        fill="both",
        expand=True
    )

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

    ancho_anterior = [1000]
    alto_anterior = [600]

    def escalar_x(x):
        return x * escena.winfo_width() / 1000

    def escalar_y(y):
        return y * escena.winfo_height() / 600

    def adaptar_escena(evento):
        if evento.width <= 1 or evento.height <= 1:
            return

        escala_x = evento.width / ancho_anterior[0]
        escala_y = evento.height / alto_anterior[0]

        escena.scale("all", 0, 0, escala_x, escala_y)

        ancho_anterior[0] = evento.width
        alto_anterior[0] = evento.height

    escena.bind("<Configure>", adaptar_escena)

    # Variables de control de la interfaz.
    indice_actual = 0
    velocidad_var = tk.StringVar(value="1x")

    def actualizar_datos(resultados, simulador, evento):
        nonlocal indice_actual

        if not resultados["tiempo"]:
            return

        indice_actual = len(resultados["tiempo"]) - 1

        # Actualizar los indicadores.
        etiqueta_temperatura.config(
            text=(
                f"Temperatura: "
                f"{resultados['temperatura'][indice_actual]:.2f} °C"
            )
        )

        etiqueta_humedad.config(
            text=(
                f"Humedad: "
                f"{resultados['humedad'][indice_actual]:.2f} %"
            )
        )

        etiqueta_luminosidad.config(
            text=(
                f"Luminosidad: "
                f"{resultados['luminosidad_total'][indice_actual]:.2f}"
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

            posicion_x = escalar_x(100 + progreso * 800)
            posicion_y = escalar_y(
                350 - 250 * math.sin(math.pi * progreso)
            )

            radio_x = escalar_x(30)
            radio_y = escalar_y(30)

            escena.coords(
                sol,
                posicion_x - radio_x, posicion_y - radio_y,
                posicion_x + radio_x, posicion_y + radio_y
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

            posicion_x = escalar_x(100 + progreso * 800)
            posicion_y = escalar_y(
                350 - 250 * math.sin(math.pi * progreso)
            )

            radio_x = escalar_x(27)
            radio_y = escalar_y(27)

            escena.coords(
                luna,
                posicion_x - radio_x, posicion_y - radio_y,
                posicion_x + radio_x, posicion_y + radio_y
            )

            escena.itemconfigure(cielo, fill="#172554")

        # Actualizar el tamaño de las plantas.
        altura = (
            25
            + (crecimiento / parametros.crecimiento_limite) * 100
        )

        for x, tallo, hoja_izquierda, hoja_derecha in plantas:
            x_escala = escalar_x(x)
            suelo_y = escalar_y(420)
            punta_tallo = escalar_y(420 - altura)

            escena.coords(
                tallo,
                x_escala, suelo_y,
                x_escala, punta_tallo
            )

            escena.coords(
                hoja_izquierda,
                escalar_x(x - 30), escalar_y(420 - altura - 15),
                x_escala, escalar_y(420 - altura + 5)
            )

            escena.coords(
                hoja_derecha,
                x_escala, escalar_y(420 - altura - 25),
                escalar_x(x + 30), escalar_y(420 - altura - 5)
            )

        indice_actual += 1


    def conectar_sesion(nueva_sesion):
        nonlocal sesion, parametros

        if sesion is not None:
            sesion.desuscribir(actualizar_datos)

        sesion = nueva_sesion
        parametros = sesion.simulador.p

        # Suscribir la ventana a todos los cambios de la simulación.
        # La suscripción también actualiza inmediatamente el estado actual.
        sesion.suscribir(actualizar_datos)


    # Panel de controles.
    panel_controles = ttk.Frame(ventana)
    panel_controles.pack(pady=5)

    # Selección del escenario.
    escenarios = obtener_escenarios()

    ttk.Label(
        panel_controles,
        text="Escenario:"
    ).pack(side="left", padx=5)

    selector_escenario = ttk.Combobox(
        panel_controles,
        values=list(escenarios.keys()),
        state="readonly",
        width=18
    )
    selector_escenario.pack(side="left", padx=5)
    selector_escenario.set("Día normal")

    def ejecutar_escenario():
        if al_ejecutar is None:
            messagebox.showwarning(
                "Simulación no disponible",
                "No se ha conectado el inicio de la simulación."
            )
            return

        nueva_sesion = al_ejecutar(selector_escenario.get())

        if nueva_sesion is not None:
            conectar_sesion(nueva_sesion)

    ttk.Button(
        panel_controles,
        text="Ejecutar simulación",
        command=ejecutar_escenario
    ).pack(side="left", padx=5)

    # Acceso al Control Center.
    ttk.Button(
        panel_controles,
        text="Control Center",
        command=abrir_control_center
        if abrir_control_center is not None else lambda: None
    ).pack(side="left", padx=5)

    # Velocidad de simulación.
    ttk.Label(
        panel_controles,
        text="Velocidad:"
    ).pack(side="left", padx=5)

    velocidad_var = tk.StringVar(value="1x")

    selector_velocidad = ttk.Combobox(
        panel_controles,
        textvariable=velocidad_var,
        values=("1x", "2x", "5x", "10x"),
        state="readonly",
        width=5
    )
    selector_velocidad.pack(side="left", padx=5)

    def cambiar_velocidad(self, intervalo_ms):
        """Cambiar la velocidad sin perder el estado de la simulación."""
        if intervalo_ms <= 0:
            raise ValueError(
                "El intervalo debe ser mayor que cero."
            )

        estaba_en_marcha = self.tarea is not None

        self.intervalo_ms = intervalo_ms

        if estaba_en_marcha:
            self.pausar()
            self.iniciar()

    selector_velocidad.bind(
        "<<ComboboxSelected>>",
        cambiar_velocidad
    )

    def iniciar_simulacion():
        if sesion is None:
            messagebox.showinfo(
                "Simulación no iniciada",
                "Selecciona un escenario y pulsa Ejecutar simulación."
            )
            return

        velocidad = float(
            velocidad_var.get().replace("x", "")
        )
        intervalo = max(1, int(1000 / velocidad))
        sesion.iniciar(intervalo)

    def pausar_simulacion():
        if sesion is not None:
            sesion.pausar()

    def reiniciar_simulacion():
        if sesion is not None:
            sesion.reiniciar()

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


    def cerrar_invernadero():
        if sesion is not None:
            sesion.desuscribir(actualizar_datos)

        ventana.destroy()

    ventana.protocol(
        "WM_DELETE_WINDOW",
        cerrar_invernadero
    )


if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.withdraw()

    escenarios = obtener_escenarios()
    parametros = escenarios["Día normal"]

    sesion = SesionSimulacion(raiz, parametros)

    abrir_invernadero(sesion)

    raiz.mainloop()