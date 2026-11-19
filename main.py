"""Punto de entrada: simula operaciones válidas e inválidas de Software FJ.

Ejecución:  python main.py
Los errores y eventos quedan registrados en logs/eventos.log
"""

from src.gestor import GestorFJ
from src.logger import ARCHIVO_LOG, obtener_logger
from src.servicios import Asesoria, AlquilerEquipo, ReservaSala


def titulo(texto):
    """Imprime un encabezado para separar los bloques de la simulación."""
    print(f"\n=== {texto} ===")


def main():
    log = obtener_logger()
    log.info("========== INICIO DE LA SIMULACIÓN ==========")
    gestor = GestorFJ()

    # ---------------- CLIENTES ----------------
    titulo("Registro de clientes")
    # 1. Cliente válido.
    ana = gestor.registrar_cliente("C001", "ana maría pérez", "1090123456", "ana.perez@correo.com", "3001234567")
    # 2. Cliente inválido: correo mal escrito.
    gestor.registrar_cliente("C002", "Luis Gómez", "1090654321", "luis.gomez-correo.com", "3109876543")
    # 3. Cliente inválido: documento con letras.
    gestor.registrar_cliente("C003", "Marta Rojas", "10A0987", "marta@correo.com", "3201112233")
    # 4. Cliente con parámetro faltante: el nombre llega vacío (None).
    gestor.registrar_cliente("C004", None, "1090777888", "sin.nombre@correo.com", "3004445566")
    # 5. Cliente válido.
    carlos = gestor.registrar_cliente("C005", "Carlos Mendoza", "88776655", "carlos@correo.com", "3157778899")
    # 6. Llamada incompleta (faltan argumentos): el error imprevisto no detiene el programa.
    gestor.registrar_cliente("C006", "Sofía Díaz")

    # ---------------- SERVICIOS ----------------
    titulo("Creación de servicios")
    # 7. Sala válida.
    sala = gestor.registrar_servicio(ReservaSala, "S01", "Sala Innovación", 50000, 25)
    # 8. Sala inválida: capacidad fuera de rango.
    gestor.registrar_servicio(ReservaSala, "S02", "Sala Imposible", 50000, 500)
    # 9. Equipo válido.
    equipo = gestor.registrar_servicio(AlquilerEquipo, "S03", "Kit Portátiles", 12000, "Portátil", 3)
    # 10. Asesoría válida (senior).
    asesoria = gestor.registrar_servicio(Asesoria, "S04", "Asesoría Python", 80000, "Programación", "senior")
    # 11. Asesoría inválida: nivel inexistente.
    gestor.registrar_servicio(Asesoria, "S05", "Asesoría Mágica", 80000, "Programación", "experto")
    # 12. Servicio inválido: tarifa negativa.
    gestor.registrar_servicio(AlquilerEquipo, "S06", "Proyector", -5000, "Proyector", 1)

    # ---------------- POLIMORFISMO ----------------
    titulo("Polimorfismo: cada servicio se describe y cobra a su manera (2 h)")
    for servicio in gestor.servicios:
        # El mismo método se comporta distinto según la clase concreta.
        print(f"  {servicio.describir()}")
        print(f"     Base: ${servicio.calcular_costo_base(2):,.2f} | "
              f"Con IVA: ${servicio.calcular_costo(2):,.2f} | "
              f"Con IVA y 10 % desc.: ${servicio.calcular_costo(2, 0.19, 0.10):,.2f}")

    # ---------------- RESERVAS ----------------
    titulo("Reservas")
    # 13. Reserva exitosa: crear, confirmar y procesar con 10 % de descuento.
    r1 = gestor.crear_reserva("R001", ana, sala, 3)
    if r1 is not None:
        gestor.ejecutar("Confirmar R001", r1.confirmar)
        gestor.ejecutar("Procesar R001 (10 % descuento)", r1.procesar, descuento=0.10)

    # 14. Reserva fallida: duración fuera de rango (30 h). Error encadenado.
    gestor.crear_reserva("R002", carlos, equipo, 30)

    # 15. Reserva fallida: servicio no disponible.
    asesoria.marcar_disponible(False)
    gestor.crear_reserva("R003", carlos, asesoria, 2)
    asesoria.marcar_disponible(True)

    # 16. Reserva fallida: el cliente no es un objeto Cliente.
    gestor.crear_reserva("R004", "no soy un cliente", sala, 2)

    # 17. Operación no permitida: procesar una reserva sin confirmarla.
    r5 = gestor.crear_reserva("R005", carlos, equipo, 4)
    if r5 is not None:
        gestor.ejecutar("Procesar R005 sin confirmar", r5.procesar)

    # 18. Cálculo inconsistente: descuento del 150 %. Error encadenado.
    if r5 is not None:
        gestor.ejecutar("Confirmar R005", r5.confirmar)
        gestor.ejecutar("Procesar R005 con descuento 150 %", r5.procesar, descuento=1.5)
        # 19. Se reintenta bien: la reserva sigue confirmada y ahora se procesa correctamente.
        gestor.ejecutar("Procesar R005 (reintento correcto)", r5.procesar)

    # 20. Cancelación exitosa y posterior intento de confirmar (no permitido).
    r6 = gestor.crear_reserva("R006", ana, asesoria, 2)
    if r6 is not None:
        gestor.ejecutar("Cancelar R006", r6.cancelar)
        gestor.ejecutar("Confirmar R006 ya cancelada", r6.confirmar)

    # ---------------- RESUMEN ----------------
    titulo("Estado final de las reservas")
    for reserva in gestor.reservas:
        print(f"  {reserva.describir()}")

    titulo("Resumen")
    print(f"  {gestor.resumen()}")
    print(f"  Log de eventos y errores: {ARCHIVO_LOG}")
    log.info(f"Resumen final | {gestor.resumen()}")
    log.info("========== FIN DE LA SIMULACIÓN ==========")


if __name__ == "__main__":
    main()
