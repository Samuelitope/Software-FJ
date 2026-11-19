"""Servicio abstracto y tres servicios especializados de Software FJ."""

from abc import ABC, abstractmethod

from src.entidad import Entidad
from src.excepciones import (
    CalculoInconsistenteError,
    ParametroFaltanteError,
    ServicioInvalidoError,
)

# Impuesto (IVA) que se aplica por defecto al calcular el costo total.
IVA_POR_DEFECTO = 0.19


def _es_numero(valor):
    """True si el valor es int o float real (se excluye bool, que en Python es int)."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


class Servicio(Entidad, ABC):
    """Clase abstracta de la que heredan todos los servicios."""

    # Duración máxima permitida por reserva, en horas.
    HORAS_MAXIMAS = 12

    def __init__(self, identificador, nombre, tarifa_hora):
        super().__init__(identificador)
        # El nombre es obligatorio.
        if nombre is None or str(nombre).strip() == "":
            raise ParametroFaltanteError("nombre")
        # La tarifa debe ser un número mayor que cero.
        if not _es_numero(tarifa_hora) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa por hora inválida: {tarifa_hora!r} (debe ser un número > 0)")
        self._nombre = str(nombre).strip()
        self._tarifa_hora = float(tarifa_hora)
        # Todo servicio nace disponible; puede marcarse como no disponible después.
        self._disponible = True

    # ---------- propiedades (encapsulación) ----------
    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    def marcar_disponible(self, estado):
        """Cambia la disponibilidad del servicio (True o False)."""
        if not isinstance(estado, bool):
            raise ServicioInvalidoError("La disponibilidad debe ser True o False")
        self._disponible = estado

    # ---------- métodos abstractos (cada servicio los sobrescribe) ----------
    @abstractmethod
    def validar_parametros(self):
        """Valida los parámetros propios del servicio especializado."""

    @abstractmethod
    def calcular_costo_base(self, horas):
        """Calcula el costo antes de impuestos y descuentos."""

    # ---------- validación de duración ----------
    def validar_duracion(self, horas):
        """Comprueba que la duración sea un número entre 0 (exclusivo) y HORAS_MAXIMAS."""
        if not _es_numero(horas):
            raise ServicioInvalidoError(f"Duración inválida: {horas!r} (debe ser numérica)")
        if horas <= 0 or horas > self.HORAS_MAXIMAS:
            raise ServicioInvalidoError(
                f"Duración fuera de rango: {horas} h (permitido: mayor que 0 y hasta {self.HORAS_MAXIMAS} h)"
            )

    # ---------- método sobrecargado ----------
    def calcular_costo(self, horas, impuesto=IVA_POR_DEFECTO, descuento=0.0):
        """Calcula el costo total. Python no tiene sobrecarga nativa, así que se
        simula con parámetros opcionales. Variantes de llamada:

            servicio.calcular_costo(3)                 -> base + IVA por defecto (19 %)
            servicio.calcular_costo(3, 0.05)           -> base + impuesto del 5 %
            servicio.calcular_costo(3, 0.19, 0.10)     -> base - 10 % de descuento + IVA 19 %
            servicio.calcular_costo(3, descuento=0.10) -> igual, solo con descuento
        """
        self.validar_duracion(horas)
        # Impuesto y descuento deben ser proporciones entre 0 y 1 (0 % a 100 %).
        if not _es_numero(impuesto) or not 0 <= impuesto <= 1:
            raise CalculoInconsistenteError(f"Impuesto inconsistente: {impuesto!r} (debe estar entre 0 y 1)")
        if not _es_numero(descuento) or not 0 <= descuento < 1:
            raise CalculoInconsistenteError(f"Descuento inconsistente: {descuento!r} (debe estar entre 0 y 1)")
        # Costo base calculado por la subclase (polimorfismo).
        base = self.calcular_costo_base(horas)
        # Se aplica primero el descuento y luego el impuesto.
        total = base * (1 - descuento) * (1 + impuesto)
        # Un total no positivo indica un cálculo incoherente.
        if total <= 0:
            raise CalculoInconsistenteError(f"El costo calculado no es positivo: {total}")
        return round(total, 2)

    def estado_texto(self):
        return "Disponible" if self._disponible else "No disponible"


class ReservaSala(Servicio):
    """Servicio de reserva de salas de reuniones."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad):
        super().__init__(identificador, nombre, tarifa_hora)
        self._capacidad = capacidad
        # Se validan los parámetros propios al crear el objeto.
        self.validar_parametros()

    def validar_parametros(self):
        # La capacidad debe ser un entero entre 1 y 100 personas.
        if not isinstance(self._capacidad, int) or isinstance(self._capacidad, bool) \
                or not 1 <= self._capacidad <= 100:
            raise ServicioInvalidoError(f"Capacidad inválida: {self._capacidad!r} (entero entre 1 y 100)")

    def calcular_costo_base(self, horas):
        costo = self._tarifa_hora * horas
        # Las salas grandes (más de 20 personas) llevan un recargo del 15 %.
        if self._capacidad > 20:
            costo *= 1.15
        return costo

    def describir(self):
        return (f"Sala '{self._nombre}' | capacidad {self._capacidad} personas | "
                f"${self._tarifa_hora:,.0f}/h | {self.estado_texto()}")


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos (portátiles, proyectores, etc.)."""

    def __init__(self, identificador, nombre, tarifa_hora, equipo, cantidad):
        super().__init__(identificador, nombre, tarifa_hora)
        self._equipo = equipo
        self._cantidad = cantidad
        self.validar_parametros()

    def validar_parametros(self):
        if self._equipo is None or str(self._equipo).strip() == "":
            raise ParametroFaltanteError("equipo")
        # Se pueden alquilar entre 1 y 10 unidades por reserva.
        if not isinstance(self._cantidad, int) or isinstance(self._cantidad, bool) \
                or not 1 <= self._cantidad <= 10:
            raise ServicioInvalidoError(f"Cantidad inválida: {self._cantidad!r} (entero entre 1 y 10)")

    def calcular_costo_base(self, horas):
        subtotal = self._tarifa_hora * horas * self._cantidad
        # Se suma un seguro del 5 % sobre el subtotal.
        return subtotal * 1.05

    def describir(self):
        return (f"Equipo '{self._nombre}' | {self._cantidad} x {self._equipo} | "
                f"${self._tarifa_hora:,.0f}/h c/u | {self.estado_texto()}")


class Asesoria(Servicio):
    """Servicio de asesoría especializada, con nivel junior o senior."""

    NIVELES = {"junior": 1.0, "senior": 1.5}  # Factor multiplicador por nivel

    def __init__(self, identificador, nombre, tarifa_hora, especialidad, nivel):
        super().__init__(identificador, nombre, tarifa_hora)
        self._especialidad = especialidad
        self._nivel = str(nivel).strip().lower() if nivel is not None else None
        self.validar_parametros()

    def validar_parametros(self):
        if self._especialidad is None or str(self._especialidad).strip() == "":
            raise ParametroFaltanteError("especialidad")
        if self._nivel not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel inválido: {self._nivel!r} (permitidos: {', '.join(self.NIVELES)})"
            )

    def calcular_costo_base(self, horas):
        # Un asesor senior cuesta 1.5 veces la tarifa; uno junior, la tarifa normal.
        return self._tarifa_hora * horas * self.NIVELES[self._nivel]

    def describir(self):
        return (f"Asesoría '{self._nombre}' | {self._especialidad} ({self._nivel}) | "
                f"${self._tarifa_hora:,.0f}/h | {self.estado_texto()}")
