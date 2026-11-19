# Software FJ: Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto de Programación orientada a objetos en Python, desarrollado de forma individual Autoria: **Samuel David Meneses** (UNAD, ECBTI).

El sistema gestiona clientes, servicios (salas, equipos y asesorías) y reservas para la empresa ficticia **Software FJ**, sin usar bases de datos. Todo se maneja con objetos y listas en memoria; los archivos se usan únicamente para el registro de eventos y errores (logs).

## Objetivos

- Aplicar abstracción, herencia, polimorfismo y encapsulación.
- Manejar excepciones de forma avanzada: excepciones personalizadas, `try/except/else/finally` y encadenamiento (`raise ... from ...`).
- Mantener la aplicación estable aunque ocurran errores, registrándolos en un archivo de logs.
- Simular al menos 10 operaciones completas (válidas e inválidas).

## Estructura del proyecto

```
software-fj/
├── README.md
├── .gitignore
├── main.py                  # Punto de entrada y simulación de operaciones
├── src/
│   ├── __init__.py
│   ├── excepciones.py       # Excepciones personalizadas
│   ├── entidad.py           # Clase abstracta Entidad
│   ├── cliente.py           # Clase Cliente
│   ├── servicios.py         # Servicio (abstracta) y servicios especializados
│   ├── reserva.py           # Clase Reserva
│   └── logger.py            # Configuración del archivo de logs
├── logs/
│   └── .gitkeep             # Aquí se genera eventos.log
└── docs/
    └── informe/             # Portada, introducción, conclusiones y referencias APA
```

## Requisitos

- Python 3.10 o superior
- No requiere librerías externas

## Ejecución

```bash
python main.py
```

El archivo `logs/eventos.log` se genera automáticamente con todos los eventos y errores.

## Estado del desarrollo

- [x] Estructura del repositorio
- [ ] Excepciones personalizadas
- [ ] Clase abstracta Entidad y clase Cliente
- [ ] Clase abstracta Servicio y tres servicios especializados
- [ ] Clase Reserva
- [ ] Logger y simulación de 10 operaciones
- [ ] Informe (portada, introducción, enlace, conclusiones, referencias APA)

## Autor

Samuel David Meneses, Estudiante UNAD, Norte de Santander (2026).
