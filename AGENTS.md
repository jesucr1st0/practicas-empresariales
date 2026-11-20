# AGENTS.md: Sistema de Gestión de Prácticas Empresariales

## Fuentes de verdad

- **docs/arquitectura.md**: mapa de visión, drivers, ADR, vistas y glosario. Es el punto de entrada para entender el sistema.
- **specs/**: una carpeta por caso de uso de drivers.md, con el mismo número (CU-03 → specs/001-postularse/).
- Si el código contradice una especificación, **gana la especificación**. Si la especificación parece incorrecta, detenerse y preguntar.

## Arquitectura

- **Monolito modular** (ADR-001), con Clean Architecture por dentro.
- `dominio/` no importa nada de `aplicacion/` ni de `infraestructura/`.
- Puertos como interfaces en `dominio/puertos/`.
- Base de datos relacional (ADR-002, candidato PostgreSQL); en esta etapa, adaptadores en memoria.
- Un solo contenedor: Aplicación de prácticas; sin broker de mensajes (ADR-008).
- Reglas de negocio versionadas e inmutables por programa (ADR-009).
- Acta final inmutable con huella de integridad (ADR-010).
- SSO institucional para usuarios internos (ADR-004); enlace de un solo uso para supervisores externos (ADR-006).
- Adaptador aislado hacia el SIA con reintentos (ADR-007, ADR-008).
- Notificaciones por correo institucional (ADR-013).

## Regla de dependencia

```
infraestructura → aplicacion → dominio
```

- Las flechas apuntan hacia el dominio. `dominio/` **nunca** importa de `aplicacion/` ni de `infraestructura/`.
- Los puertos se declaran en `dominio/puertos/`; los adaptadores los implementan en `infraestructura/`.
- Si una dependencia apunta en la dirección contraria, **la arquitectura está rota**.

## Estructura de carpetas en src/

```
src/
├── composicion/                 # arranque: lo único que conoce todas las capas
├── modulos/
│   ├── reglas/
│   ├── identidad_accesos/
│   ├── notificaciones/
│   ├── postulaciones/          # CU-03
│   ├── practicas/
│   ├── tutores_asignacion/
│   ├── horas/
│   ├── evaluaciones/
│   └── actas/
├── entradas/                    # Interfaz web interna, Formulario de acceso externo, Planificador de tareas
└── pruebas/arquitectura/
```

Cada módulo tiene:
- `dominio/` — entidades y reglas de negocio
- `aplicacion/` — casos de uso y puertos
- `infraestructura/` — adaptadores

## Convenciones de código

- Lenguaje y framework: por confirmar contra el catálogo institucional (RT-04). Candidato: Python 3.12.
- Una clase por archivo.
- DTO en la entrada y la salida de los casos de uso.
- Nombres según el glosario (sección 10 de docs/arquitectura.md).
- Los nombres de archivos y carpetas en snake_case.

## Forma de trabajar

- Una tarea de tasks.md a la vez.
- Al terminar: marcar la tarea como completada `[x]`, listar los archivos cambiados y detenerse.
- **No inventar requisitos**: lo que no esté en spec.md se pregunta, se marca con `[NECESITA ACLARACIÓN: ...]`.
- **No adelantar fases**: no escribir código antes de tener spec.md, plan.md y tasks.md aprobados.
- **No modificar docs/ ni specs/ sin autorización**: estos archivos son fuentes de verdad.
- Cada commit tiene el ID de la tarea en el mensaje.
