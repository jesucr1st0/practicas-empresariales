# Sistema de Gestión de Prácticas Empresariales

Documentación de arquitectura (taller «Vistas arquitectónicas»): contexto, vistas 4+1 y escenarios, como archivos de texto versionados.

```text
practicas-empresariales/
├── docs/
│   ├── vision.md · drivers.md (incluye §6 Escenarios) · arquitectura.md
│   ├── contexto.md                  # C4 nivel 1 (marco)
│   ├── escenarios.md                # recorrido de validación del +1
│   ├── matriz-cobertura.md          # drivers y ADR por vista
│   ├── adr/                         # ADR-001 … ADR-013, cada uno con «Vistas que modifica»
│   ├── vistas/                      # 01-logica · 02-procesos · 03-desarrollo · 04-fisica (.md)
│   └── diagramas/
│       ├── contexto.puml · 01-logica.puml · 02-procesos.puml · 03-desarrollo.puml · 04-fisica.puml
│       └── secuencias/              # cu01 … cu06 y eac01 (un archivo por escenario)
└── src/
```

Los diagramas son PlantUML (los de C4 usan `!include <C4/...>` de la biblioteca estándar). Para generarlos: `java -jar plantuml.jar -tpng docs/diagramas/*.puml docs/diagramas/secuencias/*.puml`.
