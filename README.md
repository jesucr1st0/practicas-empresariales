# Sistema de Gestión de Prácticas Empresariales

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
│   ├── vistas/                      # 01-logica · 02-procesos · 03-desarrollo · 04-fisica (.md)
│   └── diagramas/
│       ├── contexto.puml · 01-logica.puml · 02-procesos.puml · 03-desarrollo.puml · 04-fisica.puml
│       └── secuencias/              # cu01 … cu06 y eac01 (un archivo por escenario)
├── specs/
│   └── 001-postularse/              # CU-03: Realizar postulación
│       ├── spec.md                  # Especificación en Gherkin
│       ├── plan.md                  # Plan de implementación
│       ├── tasks.md                 # Tareas descompuestas
│       └── validacion.md            # Validación (pendiente de implementación)
└── src/                             # Código fuente (por implementar)
```

Los diagramas son PlantUML (los de C4 usan `!include <C4/...>` de la biblioteca estándar). Para generarlos: `java -jar plantuml.jar -tpng docs/diagramas/*.puml docs/diagramas/secuencias/*.puml`.
