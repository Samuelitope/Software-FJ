"""Excepciones personalizadas del sistema Software FJ.

Todas heredan de SoftwareFJError, de modo que el sistema pueda capturar
cualquier error propio con un solo ``except SoftwareFJError`` y, al mismo
tiempo, distinguir cada caso con una clase específica.
"""


class SoftwareFJError(Exception):
    """Excepción base de la que heredan todos los errores del sistema."""

    def __init__(self, mensaje, codigo="SFJ-000"):
        # Se envía el mensaje a la clase Exception para conservar el comportamiento estándar.
        super().__init__(mensaje)
        # Se guarda el mensaje para poder consultarlo después.
        self.mensaje = mensaje
        # Se guarda un código corto que identifica el tipo de error en los logs.
        self.codigo = codigo

    def __str__(self):
        # Representación legible: incluye el código y el mensaje.
        return f"[{self.codigo}] {self.mensaje}"


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio o llega vacío."""

    def __init__(self, parametro):
        super().__init__(f"Falta el parámetro obligatorio: '{parametro}'", "SFJ-001")


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no cumplen las validaciones."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-002")


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando los parámetros de un servicio o su duración son inválidos."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-003")


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio que no está disponible."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-004")


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no puede crearse o procesarse correctamente."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-005")


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una operación que el estado actual no permite."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-006")


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos produce valores incoherentes."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-007")
