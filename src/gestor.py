"""Gestor central: guarda las listas internas y ejecuta cada operación de forma segura."""

from src.cliente import Cliente
from src.excepciones import SoftwareFJError
from src.logger import obtener_logger
from src.reserva import Reserva


class GestorFJ:
    """Administra clientes, servicios y reservas sin usar bases de datos."""

    def __init__(self):
        self._log = obtener_logger()
        # Listas internas: reemplazan a una base de datos.
        self._clientes = []
        self._servicios = []
        self._reservas = []
        # Contadores para el resumen final.
        self._exitosas = 0
        self._fallidas = 0

    # ---------- consultas ----------
    @property
    def clientes(self):
        return list(self._clientes)  # Se devuelve una copia para proteger la lista interna

    @property
    def servicios(self):
        return list(self._servicios)

    @property
    def reservas(self):
        return list(self._reservas)

    # ---------- núcleo: ejecución segura ----------
    def ejecutar(self, descripcion, funcion, *args, **kwargs):
        """Ejecuta una operación sin dejar que un error detenga el programa.

        Devuelve el resultado, o None si hubo un fallo (que queda en el log).
        """
        try:
            resultado = funcion(*args, **kwargs)
        except SoftwareFJError as error:
            # Error previsto: se registra con su código y, si existe, la causa original.
            self._fallidas += 1
            causa = f" | causa: {error.__cause__}" if error.__cause__ else ""
            self._log.error(f"{descripcion} | {error}{causa}")
            print(f"  [ERROR] {descripcion}: {error}")
            return None
        except Exception as error:  # noqa: BLE001 - red de seguridad para errores imprevistos
            self._fallidas += 1
            self._log.critical(f"{descripcion} | Error inesperado {type(error).__name__}: {error}")
            print(f"  [ERROR INESPERADO] {descripcion}: {type(error).__name__}: {error}")
            return None
        else:
            # Solo se llega aquí si no hubo ninguna excepción.
            self._exitosas += 1
            self._log.info(f"{descripcion} | OK")
            print(f"  [OK] {descripcion}")
            return resultado
        finally:
            self._log.info(f"Operación finalizada: {descripcion}")

    # ---------- operaciones de registro ----------
    def registrar_cliente(self, *args, **kwargs):
        cliente = self.ejecutar("Registrar cliente", Cliente, *args, **kwargs)
        if cliente is not None:
            self._clientes.append(cliente)
        return cliente

    def registrar_servicio(self, clase_servicio, *args, **kwargs):
        servicio = self.ejecutar(f"Crear servicio {clase_servicio.__name__}", clase_servicio, *args, **kwargs)
        if servicio is not None:
            self._servicios.append(servicio)
        return servicio

    def crear_reserva(self, *args, **kwargs):
        reserva = self.ejecutar("Crear reserva", Reserva, *args, **kwargs)
        if reserva is not None:
            self._reservas.append(reserva)
        return reserva

    # ---------- resumen ----------
    def resumen(self):
        return (f"Operaciones exitosas: {self._exitosas} | Operaciones fallidas: {self._fallidas} | "
                f"Clientes: {len(self._clientes)} | Servicios: {len(self._servicios)} | "
                f"Reservas: {len(self._reservas)}")
