"""Configuración del archivo de logs (registro de eventos y errores)."""

import logging  # Módulo estándar de Python para registrar eventos
from pathlib import Path  # Manejo de rutas independiente del sistema operativo

# Carpeta logs/ ubicada en la raíz del proyecto (un nivel arriba de src/).
RUTA_LOGS = Path(__file__).resolve().parent.parent / "logs"
# Archivo donde se guardan todos los eventos y errores.
ARCHIVO_LOG = RUTA_LOGS / "eventos.log"


def obtener_logger(nombre="software_fj"):
    """Devuelve un logger que escribe únicamente en logs/eventos.log."""
    # Se obtiene (o crea) el logger con el nombre indicado.
    logger = logging.getLogger(nombre)
    # Si ya fue configurado, se reutiliza para no duplicar líneas en el archivo.
    if logger.handlers:
        return logger
    # Se registran eventos desde el nivel INFO hacia arriba (INFO, WARNING, ERROR...).
    logger.setLevel(logging.INFO)
    # Se asegura que la carpeta logs/ exista antes de crear el archivo.
    RUTA_LOGS.mkdir(parents=True, exist_ok=True)
    # El manejador escribe en el archivo, en modo agregar y con codificación UTF-8.
    manejador = logging.FileHandler(ARCHIVO_LOG, mode="a", encoding="utf-8")
    # Formato de cada línea: fecha y hora | nivel | mensaje.
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S")
    manejador.setFormatter(formato)
    # Se asocia el manejador al logger.
    logger.addHandler(manejador)
    # Se evita que los mensajes también salgan por la consola mediante el logger raíz.
    logger.propagate = False
    return logger
