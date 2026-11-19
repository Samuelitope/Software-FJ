"""Clase Cliente con validaciones estrictas y datos personales encapsulados."""

import re  # Expresiones regulares para validar el correo

from src.entidad import Entidad
from src.excepciones import ClienteInvalidoError, ParametroFaltanteError

# Patrón sencillo de correo: texto@dominio.extension
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(Entidad):
    """Cliente de Software FJ. Sus datos personales son privados."""

    def __init__(self, identificador, nombre, documento, correo, telefono):
        # Se inicializa la parte común (identificador) en la clase padre.
        super().__init__(identificador)
        # Atributos privados (doble guion bajo): solo se modifican con validación.
        self.__nombre = None
        self.__documento = None
        self.__correo = None
        self.__telefono = None
        # Se asignan usando las propiedades, que validan cada dato.
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @staticmethod
    def _exigir(valor, parametro):
        """Comprueba que el valor exista y no esté vacío; devuelve el texto limpio."""
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError(parametro)
        return str(valor).strip()

    # ---------- nombre ----------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        texto = self._exigir(valor, "nombre")
        # Debe tener al menos 3 caracteres y solo letras o espacios.
        if len(texto) < 3 or not all(c.isalpha() or c.isspace() for c in texto):
            raise ClienteInvalidoError(f"Nombre inválido: '{texto}' (mínimo 3 letras, sin números ni símbolos)")
        self.__nombre = texto.title()

    # ---------- documento ----------
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        texto = self._exigir(valor, "documento")
        # El documento debe ser numérico y tener entre 5 y 12 dígitos.
        if not texto.isdigit() or not 5 <= len(texto) <= 12:
            raise ClienteInvalidoError(f"Documento inválido: '{texto}' (debe tener entre 5 y 12 dígitos)")
        self.__documento = texto

    # ---------- correo ----------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        texto = self._exigir(valor, "correo")
        if not PATRON_CORREO.match(texto):
            raise ClienteInvalidoError(f"Correo inválido: '{texto}'")
        self.__correo = texto.lower()

    # ---------- teléfono ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        texto = self._exigir(valor, "telefono")
        # Se aceptan teléfonos de 7 a 10 dígitos.
        if not texto.isdigit() or not 7 <= len(texto) <= 10:
            raise ClienteInvalidoError(f"Teléfono inválido: '{texto}' (debe tener entre 7 y 10 dígitos)")
        self.__telefono = texto

    def describir(self):
        """Describe al cliente ocultando parte del documento por privacidad."""
        documento_oculto = "*" * (len(self.__documento) - 3) + self.__documento[-3:]
        return f"Cliente {self.identificador}: {self.__nombre} | Doc: {documento_oculto} | {self.__correo}"
