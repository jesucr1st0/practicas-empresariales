# Fase 2: Planear

## Entrada

- `spec.md` aprobado de la carpeta `specs/<NNN-nombre>/`.
- Los ADR citados en la traza de spec.md (en `docs/adr/`).
- Las vistas de desarrollo y procesos (`docs/vistas/03-desarrollo.md`, `docs/vistas/02-procesos.md`).
- El diagrama de secuencia correspondiente (en `docs/diagramas/secuencias/`).

## Qué producir

Crear `plan.md` dentro de la carpeta `specs/<NNN-nombre>/` indicada.

El archivo contiene:

1. **Decisiones que aplican**: tabla con ADR | Decisión | Impacto en esta funcionalidad.
2. **Componentes por capa**: qué archivos o clases se crean en `dominio/`, `aplicacion/` e `infraestructura/`, citando el módulo de la vista de desarrollo.
3. **Flujo**: descripción paso a paso del camino principal y de los caminos alternos, citando los componentes.
4. **Modelo de datos**: entidades y atributos relevantes para esta funcionalidad.
5. **Fuera de alcance**: qué NO se implementa en esta funcionalidad.

## Reglas

- **No inventar componentes** que no estén en la vista de desarrollo (docs/vistas/03-desarrollo.md).
- **No inventar tecnologías**: si algo no está decidido, dejarlo pendiente.
- Cada componente debe tener un ADR o una vista que lo justifique.
- Si falta una decisión, **no tomarla**: dejarla como pendiente.
- **Detenerse** al terminar para la revisión humana.
