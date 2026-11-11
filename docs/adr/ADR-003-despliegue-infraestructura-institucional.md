# ADR-003: Desplegar en la infraestructura de la Universidad con tecnologías del catálogo

## Estado
Aceptado — 2026-11-01 *(decisión impuesta por restricción)*

## Contexto
**RT-01** obliga a desplegar el sistema en la infraestructura de la Universidad y **RT-04** a usar solo tecnologías del catálogo institucional. **RN-05** excluye servicios de pago recurrente. El sistema maneja datos personales protegidos por **RN-01** (riesgo **RI-04** de la visión).

## Alternativas consideradas
- **A) Nube pública (IaaS/PaaS).** Ventajas: elasticidad y menor operación propia. Desventajas: incumple **RT-01**, genera costo recurrente (**RN-05**) y saca datos personales de la institución.
- **B) Infraestructura propia de la Universidad.** Cumple **RT-01** y **RT-04**, sin costo recurrente adicional.
- **C) Esquema híbrido.** Descartado: añade complejidad operativa sin un driver que lo justifique.

## Decisión
Se elige **B**. La decisión **viene impuesta por RT-01 y RT-04**; se registra para dejar explícitas las consecuencias. El sistema se entrega como un único artefacto de despliegue reproducible (ver [ADR-001](ADR-001-monolito-modular.md)).

## Consecuencias
- **Positivas:** cumplimiento de restricciones; control total de los datos personales; sin costo recurrente.
- **Negativas y costos aceptados:** dependencia del Área de sistemas para aprovisionar, monitorear y respaldar; capacidad fija y sin elasticidad; las librerías y herramientas están limitadas por el catálogo.
- **Riesgos asumidos:** el catálogo y la infraestructura concretos aún no están confirmados (vision.md §5, "pendiente de confirmación"). *Mitigación:* validar con el Área de sistemas antes de fijar versiones de motor y lenguaje.

## Vistas que modifica
- [Procesos](../vistas/02-procesos.md): todos los contenedores son propios, sin servicios de nube.
- [Física](../vistas/04-fisica.md): Centro de datos de la Universidad (RT-01).

Escenarios que lo evidencian: ESC-04 (ver [escenarios.md](../escenarios.md)).
