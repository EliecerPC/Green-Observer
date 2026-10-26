
class Controlador:
    """Controla virtualmente el riego, la ventilación y la iluminación."""

    def __init__(self, p):
        self.p = p

        # Estado inicial de los mecanismos
        self.riego = False
        self.ventilacion = False
        self.luz = False

    def evaluar(self, tiempo, temperatura, humedad, luz_natural, hora):
        """Evalúa las condiciones y registra los cambios de estado."""

        p = self.p
        eventos = []

        if not p.control_activo:
            return eventos

        # Control del riego mediante histéresis
        if not self.riego and humedad <= p.humedad_riego_activar:
            self.riego = True
            eventos.append((
                tiempo,
                "riego_on",
                f"Riego activado: humedad = {humedad:.2f} %"
            ))

        elif self.riego and humedad >= p.humedad_riego_desactivar:
            self.riego = False
            eventos.append((
                tiempo,
                "riego_off",
                f"Riego desactivado: humedad = {humedad:.2f} %"
            ))

        # Control de la ventilación mediante histéresis
        if (
            not self.ventilacion
            and temperatura >= p.temperatura_ventilacion_activar
        ):
            self.ventilacion = True
            eventos.append((
                tiempo,
                "vent_on",
                f"Ventilación activada: temperatura = {temperatura:.2f} °C"
            ))

        elif (
            self.ventilacion
            and temperatura <= p.temperatura_ventilacion_desactivar
        ):
            self.ventilacion = False
            eventos.append((
                tiempo,
                "vent_off",
                f"Ventilación desactivada: temperatura = {temperatura:.2f} °C"
            ))

        # Control de la iluminación artificial
        if p.luz_artificial_activa:
            necesita_luz = (
                luz_natural < p.luminosidad_minima
                and p.hora_luz_inicio <= hora < p.hora_luz_fin
            )

            if necesita_luz and not self.luz:
                self.luz = True
                eventos.append((
                    tiempo,
                    "luz_on",
                    f"Iluminación activada: luz natural = {luz_natural:.1f} %"
                ))

            elif not necesita_luz and self.luz:
                self.luz = False
                eventos.append((
                    tiempo,
                    "luz_off",
                    f"Iluminación desactivada: luz natural = {luz_natural:.1f} %"
                ))

        else:
            # Si se deshabilita la función, la luz debe apagarse.
            if self.luz:
                self.luz = False
                eventos.append((
                    tiempo,
                    "luz_off",
                    "Iluminación desactivada: función deshabilitada"
                ))

        return eventos
