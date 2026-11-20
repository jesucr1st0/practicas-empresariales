# Fase 1: Especificar

## Entrada

- La fila del caso de uso en `docs/drivers.md` (sección 1) y sus escenarios de atributos de calidad (sección 2).
- Los ADR que cita la fila del caso de uso (en `docs/adr/`).
- El diagrama de secuencia del escenario correspondiente (en `docs/diagramas/secuencias/`).

## Qué producir

Crear `spec.md` dentro de la carpeta `specs/<NNN-nombre>/` indicada.

El archivo usa **Gherkin en español** (`# language: es`) y contiene:

1. **Línea de traza**: `# Traza: CU-xx, EAC-xx, ADR-xxx, ...` con todos los IDs relevantes.
2. **Característica**: el nombre del caso de uso, con una descripción breve en formato de historia de usuario (_Como... quiero... para..._).
3. **Escenarios**:
   - El **flujo básico** del caso de uso.
   - Un escenario por cada **flujo alterno o excepción**.
   - Un escenario por cada **EAC** que toca este caso de uso, con su medida de respuesta.
4. Cada escenario tiene: `Dado`, `Cuando`, `Entonces` (y `Y` / `Pero` si hace falta).
5. Los datos son **concretos**, no genéricos.

## Reglas

- **No inventar** lo que no está en los documentos. Lo que falte se marca con `# [NECESITA ACLARACIÓN: ...]`.
- **No adelantar fases**: no escribir plan.md ni código.
- Usar los mismos nombres del glosario (sección 10 de `docs/arquitectura.md`).
- **Detenerse** al terminar para la revisión humana.
