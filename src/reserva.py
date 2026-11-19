"""Clase Reserva: integra cliente, servicio, duración y estado."""

from enum import Enum  # Para definir los estados posibles de una reserva

from src.cliente import Cliente
from src.entidad import Entidad
from src.excepciones import (
    CalculoInconsistenteError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)
from src.logger import obtener_logger
from src.servicios import IVA_POR_DEFECTO, Servicio

log = obtener_logger()


class EstadoReserva(Enum):
    """Estados por los que puede pasar una reserva."""
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


class Reserva(Entidad):
    """Reserva de un servicio por parte de un cliente."""

    def __init__(self, identificador, cliente, servicio, horas):
        super().__init__(identificador)
        # Se comprueban los tipos de los objetos recibidos.
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un servicio válido")
        # No se puede reservar un servicio que no está disponible.
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible")
        try:
            # La duración la valida el propio servicio.
            servicio.validar_duracion(horas)
        except ServicioInvalidoError as error:
            # Encadenamiento de excepciones: se conserva el error original con 'from'.
            raise ReservaInvalidaError(f"No se pudo crear la reserva {identificador}: duración no válida") from error
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = EstadoReserva.PENDIENTE
        self._costo_final = None

    @property
    def estado(self):
        return self._estado

    @property
    def costo_final(self):
        return self._costo_final

    def confirmar(self):
        """Pasa la reserva de Pendiente a Confirmada."""
        if self._estado is not EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva {self.identificador}: estado actual '{self._estado.value}'"
            )
        # El servicio pudo quedar no disponible después de crear la reserva.
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._servicio.nombre}' dejó de estar disponible")
        self._estado = EstadoReserva.CONFIRMADA
        log.info(f"Reserva {self.identificador} confirmada")

    def cancelar(self):
        """Cancela la reserva si aún no fue procesada ni cancelada."""
        if self._estado in (EstadoReserva.PROCESADA, EstadoReserva.CANCELADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva {self.identificador}: estado actual '{self._estado.value}'"
            )
        self._estado = EstadoReserva.CANCELADA
        log.info(f"Reserva {self.identificador} cancelada")

    def procesar(self, impuesto=IVA_POR_DEFECTO, descuento=0.0):
        """Calcula el costo y deja la reserva Procesada.

        Usa try/except/else/finally:
          - try: intenta validar el estado y calcular el costo.
          - except: traduce el error de cálculo a un error de reserva (encadenado).
          - else: solo si no hubo error, actualiza el estado y guarda el costo.
          - finally: siempre deja constancia del intento en el log.
        """
        costo = None
        try:
            if self._estado is not EstadoReserva.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"No se puede procesar la reserva {self.identificador}: debe estar 'Confirmada' "
                    f"y está '{self._estado.value}'"
                )
            costo = self._servicio.calcular_costo(self._horas, impuesto, descuento)
        except CalculoInconsistenteError as error:
            raise ReservaInvalidaError(
                f"Falló el procesamiento de la reserva {self.identificador} por un cálculo inconsistente"
            ) from error
        else:
            self._estado = EstadoReserva.PROCESADA
            self._costo_final = costo
            log.info(f"Reserva {self.identificador} procesada. Costo total: ${costo:,.2f}")
            return costo
        finally:
            log.info(f"Fin del intento de procesamiento de la reserva {self.identificador}")

    def describir(self):
        costo = f"${self._costo_final:,.2f}" if self._costo_final is not None else "sin calcular"
        return (f"Reserva {self.identificador} | {self._cliente.nombre} -> {self._servicio.nombre} | "
                f"{self._horas} h | {self._estado.value} | costo: {costo}")
