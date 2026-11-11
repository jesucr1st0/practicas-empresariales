# ADR-012: Sugerir la asignación de tutores y confirmarla manualmente

## Estado
Propuesto — 2026-11-01 *(criterios de asignación por validar con el coordinador de prácticas, riesgo RI-05)*

## Contexto
**CU-01** (asignar tutor) es un caso de uso primario que sustenta **OB-03**: al menos 95 % de los estudiantes con tutor antes de iniciar. Hay ~500 estudiantes y 50 tutores (≈10 por tutor). Los criterios (capacidad máxima, afinidad por programa) pueden cambiar por programa, por lo que se apoyan en [ADR-009](ADR-009-reglas-versionadas-por-programa.md).

## Alternativas consideradas
- **A) Asignación totalmente manual por el coordinador.** Ventaja: control total. Desventaja: no mejora **OB-03** frente al proceso actual en Excel.
- **B) Asignación automática sin intervención.** Ventaja: rápida. Desventaja: ignora criterios que el sistema no conoce y no genera confianza en los tutores.
- **C) El sistema sugiere un tutor según programa y carga actual, y el coordinador confirma o ajusta; todo queda en el historial.**

## Decisión
Se elige **C** porque equilibra el objetivo de eficiencia (**OB-03**) con el criterio humano del coordinador, y las reglas de capacidad se mantienen como datos versionables.

## Consecuencias
- **Positivas:** menos trabajo manual; asignación equilibrada y trazable.
- **Negativas y costos aceptados:** hay que mantener la lógica de sugerencia; el coordinador sigue siendo un paso obligatorio (posible cuello de botella).
- **Riesgos asumidos:** criterios mal entendidos. *Mitigación:* validarlos con el coordinador antes de implementar.

## Vistas que modifica
- [Lógica](../vistas/01-logica.md): AsignacionTutor con historial y origen sugerida o manual.
- [Desarrollo](../vistas/03-desarrollo.md): Módulo Tutores y asignación.

Escenarios que lo evidencian: ESC-01 (ver [escenarios.md](../escenarios.md)).
