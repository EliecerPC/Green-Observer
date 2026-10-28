
import tkinter as tk
from tkinter import ttk
import csv
from tkinter import filedialog, messagebox

from core.escenarios import obtener_escenarios
from core.simulacion import simular
from core.sesion_simulacion import SesionSimulacion

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dataclasses import replace
from virtual_greenhouse.main import abrir_invernadero


def main():
    ventana = tk.Tk()
    ventana.title("Green Observer")
    ventana.geometry("1100x700")
    ventana.minsize(800, 550)

    # --------------------------------------------------
    # PANTALLA DE BIENVENIDA
    # --------------------------------------------------

    inicio = ttk.Frame(ventana, padding=30)
    inicio.pack(fill="both", expand=True)

    ttk.Label(
        inicio,
        text="GREEN OBSERVER",
        font=("Arial", 26, "bold")
    ).pack(pady=(80, 10))

    ttk.Label(
        inicio,
        text="Simulador matemático de un invernadero virtual",
        font=("Arial", 13)
    ).pack(pady=(0, 35))

    ttk.Label(
        inicio,
        text=(
            "Explora las condiciones ambientales, observa los resultados "
            "y analiza el comportamiento del modelo."
        ),
        wraplength=600,
        justify="center"
    ).pack(pady=(0, 30))

    # --------------------------------------------------
    # CONTENEDOR DEL CONTROL CENTER
    # --------------------------------------------------

    # Permanece oculto hasta que se abra el Control Center.
    contenido = ttk.Frame(ventana)

    def abrir_control_center():
        inicio.pack_forget()
        contenido.pack(fill="both", expand=True)

    def abrir_invernadero_virtual():
        if sesion_actual is None:
            messagebox.showwarning(
                "Simulación no iniciada",
                "Primero inicia una simulación desde el Control Center."
            )
            return

        abrir_invernadero(sesion_actual)

    ttk.Button(
        inicio,
        text="Abrir Control Center",
        command=abrir_control_center
    ).pack(pady=10, ipadx=25, ipady=10)

    ttk.Button(
        inicio,
        text="Abrir invernadero virtual",
        command=abrir_invernadero_virtual
    ).pack(pady=10, ipadx=25, ipady=10)

    # --------------------------------------------------
    # CONFIGURACIÓN DE ESCENARIOS
    # --------------------------------------------------

    escenarios = obtener_escenarios()

    # Barra superior: selección y ejecución.
    # Ahora pertenece a contenido, no directamente a ventana.
    barra = ttk.Frame(contenido, padding=8)
    barra.pack(fill="x")

    ttk.Label(
        barra,
        text="Escenario:"
    ).pack(side="left")

    selector = ttk.Combobox(
        barra,
        values=list(escenarios.keys()),
        state="readonly",
        width=28
    )
    selector.pack(side="left", padx=6)
    selector.set("Día normal")

    boton_ejecutar = ttk.Button(
        barra,
        text="Ejecutar simulación"
    )
    boton_ejecutar.pack(side="left", padx=6)

    boton_invernadero = ttk.Button(
        barra,
        text="Abrir invernadero virtual",
        command=abrir_invernadero_virtual
    )
    boton_invernadero.pack(side="left", padx=6)

    # Estado general.
    estado = ttk.Label(
        contenido,
        text="Selecciona un escenario y ejecuta la simulación."
    )
    estado.pack(fill="x", padx=10, pady=4)

    # Pestañas principales.
    pestañas = ttk.Notebook(contenido)
    pestañas.pack(fill="both", expand=True, padx=8, pady=8)

    panel = ttk.Frame(pestañas, padding=15)
    graficas = ttk.Frame(pestañas, padding=10)
    calculos = ttk.Frame(pestañas, padding=15)
    control = ttk.Frame(pestañas, padding=15)
    datos = ttk.Frame(pestañas, padding=15)
    parametros = ttk.Frame(pestañas, padding=15)

    pestañas.add(panel, text="Panel")
    pestañas.add(graficas, text="Gráficas")
    pestañas.add(calculos, text="Cálculos")
    pestañas.add(control, text="Control y eventos")
    pestañas.add(datos, text="Datos")
    pestañas.add(parametros, text="Parámetros")

    # --------------------------------------------------
    # PANEL: indicadores principales
    # --------------------------------------------------

    ttk.Label(
        panel,
        text="Estado del invernadero",
        font=("Arial", 16, "bold")
    ).pack(pady=(5, 20))

    indicadores = ttk.Frame(panel)
    indicadores.pack(fill="x", pady=10)

    indicador_temperatura = ttk.Label(
        indicadores,
        text="Temperatura\n-- °C",
        font=("Arial", 13, "bold"),
        anchor="center"
    )
    indicador_temperatura.pack(
        side="left", expand=True, fill="x", padx=5
    )

    indicador_humedad = ttk.Label(
        indicadores,
        text="Humedad del suelo\n-- %",
        font=("Arial", 13, "bold"),
        anchor="center"
    )
    indicador_humedad.pack(
        side="left", expand=True, fill="x", padx=5
    )

    indicador_crecimiento = ttk.Label(
        indicadores,
        text="Crecimiento\n--",
        font=("Arial", 13, "bold"),
        anchor="center"
    )
    indicador_crecimiento.pack(
        side="left", expand=True, fill="x", padx=5
    )

    estado_riego = ttk.Label(panel, text="Riego: --")
    estado_riego.pack(anchor="w", pady=4)

    estado_ventilacion = ttk.Label(panel, text="Ventilación: --")
    estado_ventilacion.pack(anchor="w", pady=4)

    estado_luz = ttk.Label(
        panel,
        text="Iluminación artificial: --"
    )
    estado_luz.pack(anchor="w", pady=4)

    # --------------------------------------------------
    # GRÁFICAS: cuatro gráficas en una cuadrícula
    # --------------------------------------------------

    figura = Figure(figsize=(10, 6), dpi=100)

    ejes = figura.subplots(2, 2)
    eje_temperatura, eje_humedad, eje_luz, eje_crecimiento = (
        ejes.flatten()
    )

    # Gráfica 1: temperatura
    eje_temperatura.set_title("Temperatura")
    eje_temperatura.set_xlabel("Tiempo (minutos)")
    eje_temperatura.set_ylabel("Temperatura (°C)")
    eje_temperatura.grid(True, alpha=0.3)

    # Gráfica 2: humedad
    eje_humedad.set_title("Humedad del suelo")
    eje_humedad.set_xlabel("Tiempo (minutos)")
    eje_humedad.set_ylabel("Humedad (%)")
    eje_humedad.grid(True, alpha=0.3)

    # Gráfica 3: luminosidad
    eje_luz.set_title("Luminosidad")
    eje_luz.set_xlabel("Tiempo (minutos)")
    eje_luz.set_ylabel("Luminosidad")
    eje_luz.grid(True, alpha=0.3)

    # Gráfica 4: crecimiento
    eje_crecimiento.set_title("Crecimiento de la planta")
    eje_crecimiento.set_xlabel("Tiempo (minutos)")
    eje_crecimiento.set_ylabel("Crecimiento")
    eje_crecimiento.grid(True, alpha=0.3)

    figura.tight_layout()

    lienzo = FigureCanvasTkAgg(
        figura,
        master=graficas
    )
    lienzo.get_tk_widget().pack(
        fill="both",
        expand=True
    )

    # --------------------------------------------------
    # OTRAS PESTAÑAS
    # --------------------------------------------------

    ttk.Label(
        calculos,
        text="Cálculos paso a paso",
        font=("Arial", 15, "bold")
    ).pack(anchor="w", pady=(0, 10))

    ttk.Label(
        calculos,
        text="Selecciona un instante para consultar las operaciones "
             "realizadas por el modelo."
    ).pack(anchor="w")

    # Selector del registro que queremos consultar
    selector_paso = ttk.Scale(
        calculos,
        from_=0,
        to=0,
        orient="horizontal"
    )
    selector_paso.pack(fill="x", pady=(10, 0))

    etiqueta_paso = ttk.Label(
        calculos,
        text="Instante: sin simulación"
    )
    etiqueta_paso.pack(anchor="w", pady=(0, 10))

    # Área desplazable para mostrar las explicaciones
    marco_explicacion = ttk.Frame(calculos)
    marco_explicacion.pack(fill="both", expand=True)

    barra_explicacion = ttk.Scrollbar(
        marco_explicacion,
        orient="vertical"
    )
    barra_explicacion.pack(side="right", fill="y")

    texto_calculos = tk.Text(
        marco_explicacion,
        wrap="word",
        height=18,
        state="disabled",
        yscrollcommand=barra_explicacion.set
    )
    texto_calculos.pack(side="left", fill="both", expand=True)

    barra_explicacion.config(command=texto_calculos.yview)

    def mostrar_calculos(resultados, p, indice):
        """Presenta los cálculos registrados para un instante."""

        ultimo_indice = len(resultados["tiempo"]) - 1

        if ultimo_indice < 0:
            return

        indice = max(0, min(int(indice), ultimo_indice))

        tiempo = resultados["tiempo"][indice]
        hora = resultados["hora"][indice]

        temperatura = resultados["temperatura"][indice]
        temperatura_ambiental = resultados["temperatura_ambiental"][indice]
        humedad = resultados["humedad"][indice]
        crecimiento = resultados["crecimiento"][indice]

        luz_natural = resultados["luminosidad_natural"][indice]
        luz_total = resultados["luminosidad_total"][indice]

        evaporacion = resultados["evaporacion"][indice]
        aporte_riego = resultados["aporte_riego"][indice]

        tasa_humedad = resultados["tasa_humedad"][indice]
        tasa_temperatura = resultados["tasa_temperatura"][indice]
        tasa_crecimiento = resultados["tasa_crecimiento"][indice]

        dt = resultados["paso_aplicado"][indice]

        riego = resultados["riego"][indice]
        ventilacion = resultados["ventilacion"][indice]
        luz_artificial = resultados["luz_artificial"][indice]

        # Calcular el siguiente estado mediante Euler.
        # Se muestran los valores sin aplicar los límites físicos.
        humedad_siguiente = humedad + tasa_humedad * dt
        temperatura_siguiente = temperatura + tasa_temperatura * dt
        crecimiento_siguiente = crecimiento + tasa_crecimiento * dt

        if dt > 0:
            humedad_limitada = min(100.0, max(0.0, humedad_siguiente))
            crecimiento_limitado = min(
                p.crecimiento_limite,
                max(0.0, crecimiento_siguiente)
            )
        else:
            humedad_limitada = humedad
            crecimiento_limitado = crecimiento
            temperatura_siguiente = temperatura

        contenido = f"""INSTANTE SELECCIONADO

    Tiempo transcurrido: {tiempo:.2f} minutos
    Hora del día: {hora:.2f}

    1. CONDICIONES DEL MODELO

    Temperatura interior: {temperatura:.4f} °C
    Temperatura ambiental: {temperatura_ambiental:.4f} °C
    Humedad del suelo: {humedad:.4f} %
    Crecimiento de la planta: {crecimiento:.6f}
    Luminosidad natural: {luz_natural:.4f}
    Luminosidad total: {luz_total:.4f}

    2. ESTADO DE LOS CONTROLES

    Riego: {"Activo" if riego else "Inactivo"}
    Ventilación: {"Activa" if ventilacion else "Inactiva"}
    Iluminación artificial: {"Activa" if luz_artificial else "Inactiva"}

    Aporte de riego: {aporte_riego:.6f}
    Evaporación calculada: {evaporacion:.6f}

    3. CAMBIO DE HUMEDAD

    Ecuación: dH/dt = R - E

    Tasa de humedad = {aporte_riego:.6f} - {evaporacion:.6f}
    Tasa de humedad = {tasa_humedad:.6f}

    4. CAMBIO DE TEMPERATURA

    Ecuación de Euler: T siguiente = T actual + tasa × dt

    Temperatura actual: {temperatura:.6f} °C
    Tasa de temperatura: {tasa_temperatura:.6f} °C/min
    Intervalo de tiempo: {dt:.6f} min

    Temperatura siguiente sin límites = {temperatura:.6f}
        + ({tasa_temperatura:.6f} × {dt:.6f})
    Temperatura siguiente = {temperatura_siguiente:.6f} °C

    5. APLICACIÓN DE EULER A LA HUMEDAD

    H siguiente = H actual + tasa × dt

    H siguiente = {humedad:.6f}
        + ({tasa_humedad:.6f} × {dt:.6f})
    H siguiente sin límites = {humedad_siguiente:.6f} %

    H siguiente tras aplicar límites = {humedad_limitada:.6f} %

    6. CRECIMIENTO DE LA PLANTA

    P siguiente = P actual + tasa × dt

    Crecimiento actual: {crecimiento:.6f}
    Tasa de crecimiento: {tasa_crecimiento:.8f}
    Intervalo de tiempo: {dt:.6f} min

    Crecimiento siguiente sin límites = {crecimiento_siguiente:.6f}
    Crecimiento siguiente tras aplicar límites = {crecimiento_limitado:.6f}

    """

        if dt == 0:
            contenido += (
                "\nEste es el último instante de la simulación. "
                "No se ejecuta un paso de Euler posterior.\n"
            )

        texto_calculos.config(state="normal")
        texto_calculos.delete("1.0", "end")
        texto_calculos.insert("1.0", contenido)
        texto_calculos.config(state="disabled")

        etiqueta_paso.config(
            text=f"Instante: {indice} de {ultimo_indice} | "
                 f"Tiempo: {tiempo:.2f} min"
        )

    # Resumen de los mecanismos de control
    ttk.Label(
        control,
        text="Resumen de controles",
        font=("Arial", 15, "bold")
    ).pack(anchor="w", pady=(0, 10))

    resumen_controles = ttk.Label(
        control,
        text="Ejecuta una simulación para consultar los controles."
    )
    resumen_controles.pack(anchor="w", pady=(0, 12))

    ttk.Label(
        control,
        text="Historial de eventos",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", pady=(0, 5))

    marco_historial = ttk.Frame(control)
    marco_historial.pack(fill="both", expand=True)

    barra_historial = ttk.Scrollbar(
        marco_historial,
        orient="vertical"
    )
    barra_historial.pack(side="right", fill="y")

    historial = tk.Text(
        marco_historial,
        height=16,
        state="disabled",
        wrap="word",
        yscrollcommand=barra_historial.set
    )
    historial.pack(side="left", fill="both", expand=True)

    barra_historial.config(command=historial.yview)

    # Tabla de resultados de la simulación
    columnas = (
        "tiempo",
        "temperatura",
        "humedad",
        "luminosidad",
        "crecimiento",
        "evaporacion",
        "riego",
        "ventilacion",
        "luz_artificial"
    )

    tabla = ttk.Treeview(
        datos,
        columns=columnas,
        show="headings"
    )

    encabezados = {
        "tiempo": "Tiempo (min)",
        "temperatura": "Temp. (°C)",
        "humedad": "Humedad (%)",
        "luminosidad": "Luz",
        "crecimiento": "Crecimiento",
        "evaporacion": "Evaporación",
        "riego": "Riego",
        "ventilacion": "Ventilación",
        "luz_artificial": "Luz artificial"
    }

    for columna, titulo_columna in encabezados.items():
        tabla.heading(columna, text=titulo_columna)
        tabla.column(columna, width=105, anchor="center")

    barra_vertical = ttk.Scrollbar(
        datos,
        orient="vertical",
        command=tabla.yview
    )

    barra_horizontal = ttk.Scrollbar(
        datos,
        orient="horizontal",
        command=tabla.xview
    )

    tabla.configure(
        yscrollcommand=barra_vertical.set,
        xscrollcommand=barra_horizontal.set
    )

    tabla.grid(row=0, column=0, sticky="nsew")
    barra_vertical.grid(row=0, column=1, sticky="ns")
    barra_horizontal.grid(row=1, column=0, sticky="ew")

    datos.rowconfigure(0, weight=1)
    datos.columnconfigure(0, weight=1)

    # --------------------------------------------------
    # PARÁMETROS: configuración del escenario
    # --------------------------------------------------

    ttk.Label(
        parametros,
        text="Parámetros de la simulación",
        font=("Arial", 15, "bold")
    ).pack(anchor="w", pady=(0, 10))

    ttk.Label(
        parametros,
        text="Estos valores se aplicarán a la siguiente ejecución."
    ).pack(anchor="w", pady=(0, 12))

    marco_parametros = ttk.Frame(parametros)
    marco_parametros.pack(fill="both", expand=True)

    # Campos numéricos que se podrán modificar.
    campos_parametros = {
        "temperatura_inicial": (
            "Temperatura inicial (°C)", "temperatura_inicial"
        ),
        "humedad_inicial": (
            "Humedad inicial (%)", "humedad_inicial"
        ),
        "crecimiento_inicial": (
            "Crecimiento inicial", "crecimiento_inicial"
        ),
        "duracion": (
            "Duración (minutos)", "duracion"
        ),
        "paso_tiempo": (
            "Paso de tiempo (minutos)", "paso_tiempo"
        ),
        "nubosidad": (
            "Nubosidad (0 a 1)", "nubosidad"
        ),
        "temperatura_media": (
            "Temperatura ambiental media (°C)", "temperatura_media"
        ),
        "amplitud_temperatura": (
            "Amplitud térmica (°C)", "amplitud_temperatura"
        ),
    }

    entradas_parametros = {}

    for fila, (clave, (etiqueta, atributo)) in enumerate(
            campos_parametros.items()
    ):
        ttk.Label(
            marco_parametros,
            text=etiqueta
        ).grid(
            row=fila,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        entrada = ttk.Entry(marco_parametros, width=18)
        entrada.grid(
            row=fila,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )

        entradas_parametros[clave] = entrada

    fila_opciones = len(campos_parametros)

    control_automatico = tk.BooleanVar(value=True)
    luz_artificial_configurada = tk.BooleanVar(value=False)

    ttk.Checkbutton(
        marco_parametros,
        text="Activar control automático",
        variable=control_automatico
    ).grid(
        row=fila_opciones,
        column=0,
        columnspan=2,
        sticky="w",
        padx=5,
        pady=5
    )

    ttk.Checkbutton(
        marco_parametros,
        text="Permitir iluminación artificial",
        variable=luz_artificial_configurada
    ).grid(
        row=fila_opciones + 1,
        column=0,
        columnspan=2,
        sticky="w",
        padx=5,
        pady=5
    )

    mensaje_parametros = ttk.Label(
        marco_parametros,
        text="Selecciona un escenario para cargar sus valores."
    )
    mensaje_parametros.grid(
        row=fila_opciones + 2,
        column=0,
        columnspan=2,
        sticky="w",
        padx=5,
        pady=10
    )

    def cargar_parametros():
        """Cargar los valores del escenario seleccionado."""
        p = escenarios[selector.get()]

        for clave, entrada in entradas_parametros.items():
            entrada.delete(0, "end")
            entrada.insert(0, str(getattr(p, clave)))

        control_automatico.set(p.control_activo)
        luz_artificial_configurada.set(p.luz_artificial_activa)

        mensaje_parametros.config(
            text=f"Valores cargados: {selector.get()}"
        )

    def obtener_parametros_configurados():
        """Crear una copia del escenario con los valores de la interfaz."""
        p = escenarios[selector.get()]
        cambios = {}

        for clave, entrada in entradas_parametros.items():
            texto = entrada.get().strip()

            if not texto:
                raise ValueError(
                    f"El campo '{clave}' no puede estar vacío."
                )

            try:
                cambios[clave] = float(texto)
            except ValueError:
                raise ValueError(
                    f"El campo '{clave}' debe contener un número válido."
                )

        cambios["control_activo"] = control_automatico.get()
        cambios["luz_artificial_activa"] = (
            luz_artificial_configurada.get()
        )

        configuracion = replace(p, **cambios)
        configuracion.validar()

        return configuracion

    def aplicar_parametros():
        """Validar la configuración y confirmar que puede utilizarse."""
        try:
            configuracion = obtener_parametros_configurados()
        except (ValueError, TypeError) as error:
            mensaje_parametros.config(
                text=f"Error en los parámetros: {error}"
            )
            return

        mensaje_parametros.config(
            text="Parámetros válidos. Se usarán en la próxima simulación."
        )

    ttk.Button(
        marco_parametros,
        text="Aplicar y validar",
        command=aplicar_parametros
    ).grid(
        row=fila_opciones + 3,
        column=0,
        sticky="w",
        padx=5,
        pady=10
    )

    ttk.Button(
        marco_parametros,
        text="Cargar escenario seleccionado",
        command=cargar_parametros
    ).grid(
        row=fila_opciones + 3,
        column=1,
        sticky="w",
        padx=5,
        pady=10
    )

    selector.bind("<<ComboboxSelected>>", lambda evento: cargar_parametros())

    cargar_parametros()

    # --------------------------------------------------
    # EJECUCIÓN DE LA SIMULACIÓN
    # --------------------------------------------------

    datos_simulacion_actual = {
        "resultados": None,
        "parametros": None
    }
    sesion_actual = None

    def actualizar_control_center(resultados, simulador, evento):
        """Actualizar el Control Center con los datos disponibles."""

        nonlocal sesion_actual

        p = simulador.p

        # Guardar los datos parciales de la sesión compartida.
        datos_simulacion_actual["resultados"] = resultados
        datos_simulacion_actual["parametros"] = p

        # Si se reinicia, borrar los registros visuales anteriores.
        if evento == "reinicio":
            for fila in tabla.get_children():
                tabla.delete(fila)

            historial.config(state="normal")
            historial.delete("1.0", "end")
            historial.config(state="disabled")

        cantidad = len(resultados["tiempo"])

        if cantidad == 0:
            return

        i = cantidad - 1

        # Actualizar los indicadores con el instante más reciente.
        indicador_temperatura.config(
            text=f"Temperatura\n{resultados['temperatura'][i]:.2f} °C"
        )
        indicador_humedad.config(
            text=f"Humedad del suelo\n{resultados['humedad'][i]:.2f} %"
        )
        indicador_crecimiento.config(
            text=f"Crecimiento\n{resultados['crecimiento'][i]:.4f}"
        )

        estado_riego.config(
            text=f"Riego: {'Activo' if resultados['riego'][i] else 'Inactivo'}"
        )
        estado_ventilacion.config(
            text=(
                "Ventilación: "
                f"{'Activa' if resultados['ventilacion'][i] else 'Inactiva'}"
            )
        )
        estado_luz.config(
            text=(
                "Iluminación artificial: "
                f"{'Activa' if resultados['luz_artificial'][i] else 'Inactiva'}"
            )
        )

        # Insertar solamente las filas que todavía no aparecen en la tabla.
        filas_actuales = len(tabla.get_children())

        if evento == "reinicio":
            filas_actuales = 0

        for j in range(filas_actuales, cantidad):
            tabla.insert(
                "",
                "end",
                values=(
                    f"{resultados['tiempo'][j]:.1f}",
                    f"{resultados['temperatura'][j]:.2f}",
                    f"{resultados['humedad'][j]:.2f}",
                    f"{resultados['luminosidad_natural'][j]:.2f}",
                    f"{resultados['crecimiento'][j]:.4f}",
                    f"{resultados['evaporacion'][j]:.4f}",
                    "Activo" if resultados["riego"][j] else "Inactivo",
                    "Activa" if resultados["ventilacion"][j] else "Inactiva",
                    "Activa" if resultados["luz_artificial"][j] else "Inactiva",
                ),
            )

        # Reconstruir las gráficas con todos los datos disponibles.
        eje_temperatura.clear()
        eje_temperatura.plot(
            resultados["tiempo"],
            resultados["temperatura"],
            label="Temperatura interior",
        )
        eje_temperatura.plot(
            resultados["tiempo"],
            resultados["temperatura_ambiental"],
            label="Temperatura ambiental",
            linestyle="--",
        )
        eje_temperatura.set_title("Temperatura")
        eje_temperatura.set_xlabel("Tiempo (minutos)")
        eje_temperatura.set_ylabel("Temperatura (°C)")
        eje_temperatura.legend(fontsize=8)
        eje_temperatura.grid(True, alpha=0.3)

        eje_humedad.clear()
        eje_humedad.plot(
            resultados["tiempo"],
            resultados["humedad"],
            label="Humedad del suelo",
        )
        eje_humedad.set_title("Humedad del suelo")
        eje_humedad.set_xlabel("Tiempo (minutos)")
        eje_humedad.set_ylabel("Humedad (%)")
        eje_humedad.set_ylim(0, 100)
        eje_humedad.legend(fontsize=8)
        eje_humedad.grid(True, alpha=0.3)

        eje_luz.clear()
        eje_luz.plot(
            resultados["tiempo"],
            resultados["luminosidad_natural"],
            label="Luz natural",
        )
        eje_luz.plot(
            resultados["tiempo"],
            resultados["luminosidad_total"],
            label="Luz total",
            linestyle="--",
        )
        eje_luz.set_title("Luminosidad")
        eje_luz.set_xlabel("Tiempo (minutos)")
        eje_luz.set_ylabel("Luminosidad")
        eje_luz.legend(fontsize=8)
        eje_luz.grid(True, alpha=0.3)

        eje_crecimiento.clear()
        eje_crecimiento.plot(
            resultados["tiempo"],
            resultados["crecimiento"],
            label="Crecimiento de la planta",
        )
        eje_crecimiento.set_title("Crecimiento de la planta")
        eje_crecimiento.set_xlabel("Tiempo (minutos)")
        eje_crecimiento.set_ylabel("Crecimiento")
        eje_crecimiento.legend(fontsize=8)
        eje_crecimiento.grid(True, alpha=0.3)

        figura.tight_layout()
        lienzo.draw_idle()

        # Permitir consultar cualquier instante registrado hasta ahora.
        selector_paso.configure(from_=0, to=cantidad - 1)

        if evento == "reinicio":
            selector_paso.set(0)

        mostrar_calculos(
            resultados,
            p,
            int(float(selector_paso.get())),
        )

        # Mostrar el resumen de los eventos acumulados.
        eventos = resultados["eventos"]

        resumen_controles.config(
            text=(
                f"Eventos registrados: {len(eventos)}\n"
                f"Eventos relacionados con riego: "
                f"{sum(1 for _, tipo, _ in eventos if 'riego' in tipo.lower())}\n"
                f"Eventos relacionados con ventilación: "
                f"{sum(1 for _, tipo, _ in eventos if 'ventil' in tipo.lower())}\n"
                f"Eventos relacionados con iluminación: "
                f"{sum(1 for _, tipo, _ in eventos if 'luz' in tipo.lower() or 'ilumin' in tipo.lower())}"
            )
        )

        historial.config(state="normal")
        historial.delete("1.0", "end")

        for evento_registrado in eventos:
            historial.insert(
                "end",
                formatear_evento(evento_registrado, p) + "\n",
            )

        if not eventos:
            historial.insert(
                "end",
                "La simulación no ha registrado eventos de control.\n",
            )

        historial.config(state="disabled")

        estado.config(
            text=(
                    f"Simulación en el minuto {resultados['tiempo'][-1]:.2f} "
                    f"de {p.duracion:.2f}."
                    + (" Finalizada." if simulador.terminado else "")
            )
        )

    def cambiar_paso(valor):
        resultados = datos_simulacion_actual["resultados"]
        p = datos_simulacion_actual["parametros"]

        if resultados is not None and p is not None:
            mostrar_calculos(resultados, p, int(float(valor)))

    selector_paso.configure(command=cambiar_paso)


    def ejecutar_simulacion():
        nonlocal sesion_actual

        try:
            parametros_escenario = obtener_parametros_configurados()

            # Detener la sesión anterior, si existe.
            if sesion_actual is not None:
                sesion_actual.pausar()

            # Crear una nueva sesión con los parámetros seleccionados.
            sesion_actual = SesionSimulacion(
                ventana,
                parametros_escenario
            )

            # Registrar el estado inicial y preparar las vistas.
            datos_simulacion_actual["resultados"] = (
                sesion_actual.resultados
            )
            datos_simulacion_actual["parametros"] = (
                parametros_escenario
            )

            sesion_actual.suscribir(actualizar_control_center)

            # Comenzar a avanzar paso a paso.
            sesion_actual.iniciar()

        except (ValueError, TypeError) as error:
            mensaje_parametros.config(
                text=f"Error en los parámetros: {error}"
            )
            estado.config(
                text="No se pudo iniciar la simulación. Revisa los parámetros."
            )
            messagebox.showerror(
                "Error de simulación",
                str(error)
            )



    def exportar_csv():
        resultados = datos_simulacion_actual["resultados"]

        if resultados is None:
            messagebox.showwarning(
                "Sin resultados",
                "Primero debes ejecutar una simulación."
            )
            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar resultados de la simulación",
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")],
            initialfile="resultados_green_observer.csv"
        )

        if not ruta:
            return

        try:
            # Excluir los eventos porque no tienen una fila por instante.
            columnas = [
                nombre
                for nombre in resultados
                if nombre != "eventos"
            ]

            with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(columnas)

                cantidad = len(resultados["tiempo"])

                for i in range(cantidad):
                    fila = [
                        resultados[columna][i]
                        for columna in columnas
                    ]
                    escritor.writerow(fila)

            messagebox.showinfo(
                "Exportación completada",
                f"Los resultados se guardaron correctamente en:\n{ruta}"
            )

        except OSError as error:
            messagebox.showerror(
                "Error al exportar",
                f"No se pudo guardar el archivo:\n{error}"
            )

    def formatear_evento(evento, p):
        tiempo, tipo, mensaje = evento

        # Convertir los minutos simulados en una hora del día.
        minutos_totales = round(p.hora_inicio * 60 + tiempo)
        hora = (minutos_totales // 60) % 24
        minuto = minutos_totales % 60

        # Traducir el código del evento a un nombre legible.
        nombres = {
            "riego_on": "Riego activado",
            "riego_off": "Riego desactivado",
            "vent_on": "Ventilación activada",
            "vent_off": "Ventilación desactivada",
            "luz_on": "Iluminación activada",
            "luz_off": "Iluminación desactivada",
        }

        nombre = nombres.get(tipo, tipo)

        return (
            f"Minuto {tiempo:g} | "
            f"{hora:02d}:{minuto:02d} | "
            f"{nombre} | {mensaje}"
        )

    def generar_informe():
        resultados = datos_simulacion_actual["resultados"]
        p = datos_simulacion_actual["parametros"]

        if resultados is None or p is None:
            messagebox.showwarning(
                "Sin resultados",
                "Primero debes ejecutar una simulación."
            )
            return

        # Obtener los datos registrados durante la simulación.
        temperatura = resultados["temperatura"]
        humedad = resultados["humedad"]
        crecimiento = resultados["crecimiento"]
        luminosidad = resultados["luminosidad_total"]

        # Calcular estadísticas.
        temperatura_min = min(temperatura)
        temperatura_max = max(temperatura)
        humedad_min = min(humedad)
        humedad_max = max(humedad)
        crecimiento_min = min(crecimiento)
        crecimiento_max = max(crecimiento)

        # Contar los eventos registrados.
        eventos = resultados.get("eventos", [])
        total_eventos = len(eventos)

        eventos_riego = sum(
            1 for evento in eventos
            if "riego" in str(evento).lower()
        )
        eventos_ventilacion = sum(
            1 for evento in eventos
            if "ventil" in str(evento).lower()
        )
        eventos_luz = sum(
            1 for evento in eventos
            if "luz" in str(evento).lower()
            or "ilumin" in str(evento).lower()
        )

        # Preparar observaciones basadas en los resultados.
        observaciones = []

        if temperatura_max >= p.temperatura_ventilacion_activar:
            observaciones.append(
                "Se alcanzó una temperatura que activa el umbral "
                "de ventilación configurado."
            )

        if humedad_min <= p.humedad_riego_activar:
            observaciones.append(
                "La humedad alcanzó o bajó del umbral de activación "
                "del riego."
            )

        if luminosidad and max(luminosidad) == 0:
            observaciones.append(
                "No se registró luminosidad total durante la simulación."
            )

        if crecimiento[-1] > crecimiento[0]:
            observaciones.append(
                "El crecimiento aumentó durante el periodo simulado."
            )
        elif crecimiento[-1] < crecimiento[0]:
            observaciones.append(
                "El crecimiento disminuyó durante el periodo simulado."
            )
        else:
            observaciones.append(
                "El crecimiento terminó en el mismo valor inicial."
            )

        if not observaciones:
            observaciones.append(
                "No se identificaron las condiciones anteriores."
            )

        # Construir el contenido del informe.
        lineas = [
            "GREEN OBSERVER",
            "INFORME DE SIMULACIÓN DEL INVERNADERO",
            "=" * 50,
            "",
            "1. CONFIGURACIÓN",
            f"Duración: {p.duracion} minutos",
            f"Paso de tiempo configurado: {p.paso_tiempo} minutos",
            f"Temperatura inicial: {p.temperatura_inicial} °C",
            f"Humedad inicial: {p.humedad_inicial} %",
            f"Crecimiento inicial: {p.crecimiento_inicial}",
            f"Nubosidad: {p.nubosidad * 100:.1f} %",
            f"Control automático: {'Sí' if p.control_activo else 'No'}",
            "",
            "2. RESULTADOS FINALES",
            f"Temperatura final: {temperatura[-1]:.2f} °C",
            f"Humedad final: {humedad[-1]:.2f} %",
            f"Crecimiento final: {crecimiento[-1]:.4f}",
            "",
            "3. ESTADÍSTICAS DEL PERIODO",
            f"Temperatura mínima: {temperatura_min:.2f} °C",
            f"Temperatura máxima: {temperatura_max:.2f} °C",
            f"Humedad mínima: {humedad_min:.2f} %",
            f"Humedad máxima: {humedad_max:.2f} %",
            f"Crecimiento mínimo: {crecimiento_min:.4f}",
            f"Crecimiento máximo: {crecimiento_max:.4f}",
            "",
            "4. EVENTOS DE CONTROL",
            f"Total de registros de eventos: {total_eventos}",
            f"Eventos relacionados con riego: {eventos_riego}",
            f"Eventos relacionados con ventilación: {eventos_ventilacion}",
            f"Eventos relacionados con iluminación: {eventos_luz}",
            "",
            "5. OBSERVACIONES AUTOMÁTICAS",
        ]

        for observacion in observaciones:
            lineas.append(f"- {observacion}")

        lineas.extend([
            "",
            "6. HISTORIAL DETALLADO DE EVENTOS",
        ])

        if eventos:
            for evento in eventos:
                lineas.append(formatear_evento(evento, p))
        else:
            lineas.append("No se registraron eventos de control.")

        lineas.extend([
            "",
            "6. NOTA METODOLÓGICA",
            "Los resultados corresponden a una simulación matemática,",
            "no a mediciones tomadas de un invernadero real.",
            "Las observaciones son orientativas y no sustituyen",
            "la evaluación agronómica de un cultivo.",
            "",
            "Fin del informe.",
        ])

        contenido = "\n".join(lineas)

        # Elegir dónde guardar el informe.
        ruta = filedialog.asksaveasfilename(
            title="Guardar informe de simulación",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")],
            initialfile="informe_green_observer.txt"
        )

        if not ruta:
            return

        try:
            with open(ruta, "w", encoding="utf-8-sig") as archivo:
                archivo.write(contenido)

            messagebox.showinfo(
                "Informe generado",
                f"El informe se guardó correctamente en:\n{ruta}"
            )

        except OSError as error:
            messagebox.showerror(
                "Error al guardar",
                f"No se pudo guardar el informe:\n{error}"
            )

    boton_exportar = ttk.Button(
        barra,
        text="Exportar CSV",
        command=exportar_csv
    )
    boton_exportar.pack(side="left", padx=5)

    boton_informe = ttk.Button(
        barra,
        text="Generar informe",
        command=generar_informe
    )
    boton_informe.pack(side="left", padx=5)

    boton_ejecutar.config(command=ejecutar_simulacion)

    ventana.mainloop()


if __name__ == "__main__":
    main()
