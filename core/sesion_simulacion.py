
from core.simulacion import Simulador


class SesionSimulacion:
    """Coordina una simulación compartida entre varias ventanas."""

    def __init__(self, ventana_raiz, parametros, intervalo_ms=1000):
        self.ventana_raiz = ventana_raiz
        self.parametros = parametros
        self.intervalo_ms = intervalo_ms

        self.simulador = Simulador(parametros)
        self.tarea = None
        self.observadores = []

        # Registrar el estado inicial de la simulación.
        self.simulador.paso()

    @property
    def resultados(self):
        return self.simulador.datos

    def suscribir(self, observador):
        """Registrar una función que actualizará una ventana."""
        if observador not in self.observadores:
            self.observadores.append(observador)

        observador(self.resultados, self.simulador, "actualizacion")

    def desuscribir(self, observador):
        if observador in self.observadores:
            self.observadores.remove(observador)

    def notificar(self, evento="actualizacion"):
        """Informar a las ventanas de un cambio."""
        for observador in tuple(self.observadores):
            observador(self.resultados, self.simulador, evento)

    def iniciar(self, intervalo_ms=None):
        """Iniciar o reanudar el avance compartido."""
        if intervalo_ms is not None:
            self.intervalo_ms = intervalo_ms

        if self.tarea is None and not self.simulador.terminado:
            self.tarea = self.ventana_raiz.after(
                self.intervalo_ms,
                self._avanzar
            )

    def _avanzar(self):
        """Calcular un instante y actualizar todas las ventanas."""
        self.tarea = None

        if self.simulador.terminado:
            return

        self.simulador.paso()
        self.notificar()

        if not self.simulador.terminado:
            self.iniciar()

    def pausar(self):
        """Detener el reloj sin perder el estado actual."""
        if self.tarea is not None:
            self.ventana_raiz.after_cancel(self.tarea)
            self.tarea = None

    def reiniciar(self):
        """Restablecer el modelo y notificar a las ventanas."""
        self.pausar()
        self.simulador.reiniciar()
        self.simulador.paso()
        self.notificar("reinicio")


    def cambiar_velocidad(self, intervalo_ms):
        """Cambiar la velocidad sin perder el estado de la simulación."""
        if isinstance(intervalo_ms, bool) or not isinstance(
            intervalo_ms, (int, float)
        ):
            raise ValueError("El intervalo debe ser un número positivo.")

        if intervalo_ms <= 0:
            raise ValueError("El intervalo debe ser un número positivo.")

        intervalo_ms = max(1, round(intervalo_ms))
        estaba_en_marcha = self.tarea is not None

        if estaba_en_marcha:
            self.pausar()

        self.intervalo_ms = intervalo_ms

        if estaba_en_marcha:
            self.iniciar()

