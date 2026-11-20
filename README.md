# Sistema de Gestión de Prácticas Empresariales

<<<<<<< HEAD
Documentación de arquitectura (taller «Vistas arquitectónicas»): contexto, vistas 4+1 y escenarios, como archivos de texto versionados.

```text
practicas-empresariales/
├── docs/
│   ├── vision.md · drivers.md (incluye §6 Escenarios) · arquitectura.md
│   ├── contexto.md                  # C4 nivel 1 (marco)
│   ├── escenarios.md                # recorrido de validación del +1
│   ├── matriz-cobertura.md          # drivers y ADR por vista
│   ├── adr/                         # ADR-001 … ADR-013, cada uno con «Vistas que modifica»
=======
Documentación de arquitectura y desarrollo orientado por especificaciones (SDD) para el sistema de gestión de prácticas empresariales de la Facultad de Ingenierías.

```text
practicas-empresariales/
├── AGENTS.md                        # Reglas permanentes para agentes de IA
├── prompts/                         # Instrucciones por fase SDD
│   ├── 0-arranque.md                # Mensaje de inicio de cada sesión
│   ├── 1-especificar.md             # Fase 1: crear spec.md
│   ├── 2-planear.md                 # Fase 2: crear plan.md
│   ├── 3-descomponer.md             # Fase 3: crear tasks.md
│   ├── 4-implementar.md             # Fase 4: generar código tarea por tarea
│   └── 5-validar.md                 # Fase 5: crear validacion.md
├── docs/
│   ├── arquitectura.md              # Mapa completo (10 secciones, arc42)
│   ├── vision.md · drivers.md       # Visión y drivers arquitectónicos
│   ├── contexto.md                  # C4 nivel 1 (marco)
│   ├── escenarios.md                # Recorrido de validación del +1
│   ├── matriz-cobertura.md          # Drivers y ADR por vista
│   ├── adr/                         # ADR-001 … ADR-013
>>>>>>> 4079cdcf847bf9e14e5404e439ca80000d774749
│   ├── vistas/                      # 01-logica · 02-procesos · 03-desarrollo · 04-fisica (.md)
│   └── diagramas/
│       ├── contexto.puml · 01-logica.puml · 02-procesos.puml · 03-desarrollo.puml · 04-fisica.puml
│       └── secuencias/              # cu01 … cu06 y eac01 (un archivo por escenario)
<<<<<<< HEAD
└── src/
=======
├── specs/
│   ├── 001-asignar-tutor/           # CU-01: Asignar tutor
│   │   ├── spec.md                  # Especificación en Gherkin
│   │   ├── plan.md                  # Plan de implementación
│   │   ├── tasks.md                 # Tareas descompuestas
│   │   └── validacion.md            # Validación
│   ├── 002-registrar-practica/      # CU-02: Registrar práctica
│   │   ├── spec.md                  # Especificación en Gherkin
│   │   ├── plan.md                  # Plan de implementación
│   │   ├── tasks.md                 # Tareas descompuestas
│   │   └── validacion.md            # Validación
│   └── 003-realizar-postulacion/    # CU-03: Realizar postulación
│       ├── spec.md                  # Especificación en Gherkin
│       ├── plan.md                  # Plan de implementación
│       ├── tasks.md                 # Tareas descompuestas
│       └── validacion.md            # Validación
└── src/                             # Código fuente (por implementar)
>>>>>>> 4079cdcf847bf9e14e5404e439ca80000d774749
```

Los diagramas son PlantUML (los de C4 usan `!include <C4/...>` de la biblioteca estándar). Para generarlos: `java -jar plantuml.jar -tpng docs/diagramas/*.puml docs/diagramas/secuencias/*.puml`.
