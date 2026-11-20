# Fase 3: Descomponer

## Entrada

- `spec.md` y `plan.md` aprobados de la carpeta `specs/<NNN-nombre>/`.

## Qué producir

Crear `tasks.md` dentro de la carpeta `specs/<NNN-nombre>/` indicada.

El archivo contiene una lista de tareas numeradas `T-01`, `T-02`, ..., cada una con:

1. **Casilla**: `- [ ] T-xx: <descripción breve>`
2. **Archivo(s)**: qué archivo(s) crea o modifica (uno solo, si es posible).
3. **Escenario(s)**: qué escenario(s) de spec.md atiende.
4. **Dependencia(s)**: qué tarea(s) deben estar listas antes.

## Reglas

- Cada tarea toca **un solo archivo o clase**. Si una tarea necesita dos archivos, se divide.
- El orden va **de adentro hacia afuera**: primero entidades del dominio, luego casos de uso, luego adaptadores, luego entradas.
- Todo escenario de spec.md debe aparecer en al menos una tarea.
- La **última tarea** es la validación (ejecutar `prompts/5-validar.md`).
- **No escribir código**: solo la lista de tareas.
- **Detenerse** al terminar para la revisión humana.
