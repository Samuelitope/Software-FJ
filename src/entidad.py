"""Clase abstracta que representa las entidades generales del sistema."""

from abc import ABC, abstractmethod  # Herramientas para definir clases abstractas

from src.excepciones import ParametroFaltanteError


class Entidad(ABC):
    """Base abstracta de Cliente, Servicio y Reserva.

    Toda entidad tiene un identificador único y debe saber describirse.
    No se puede instanciar directamente porque tiene un método abstracto.
    """

    def __init__(self, identificador):
        # Se rechaza un identificador ausente o formado solo por espacios.
        if identificador is None or str(identificador).strip() == "":
            raise ParametroFaltanteError("identificador")
        # Atributo protegido (encapsulación): se accede mediante la propiedad.
        self._identificador = str(identificador).strip()

    @property
    def identificador(self):
        """Devuelve el identificador (solo lectura)."""
        return self._identificador

    @abstractmethod
    def describir(self):
        """Devuelve un texto que describe la entidad. Cada subclase lo implementa."""

    def __str__(self):
        # Al imprimir cualquier entidad se usa su descripción (polimorfismo).
        return self.describir()
