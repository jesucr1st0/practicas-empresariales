# Fase 5: Validar

## Entrada

- `spec.md`, `plan.md` y `tasks.md` de la carpeta `specs/<NNN-nombre>/`.
- El código fuente en `src/`.

## Qué producir

Crear `validacion.md` dentro de la carpeta `specs/<NNN-nombre>/` indicada.

El archivo contiene:

### 1. Validación por escenario

Una tabla con:

| Escenario | Cumple | Evidencia |
|-----------|--------|-----------|

Para cada escenario de spec.md:
- **Cumple**: Sí o No.
- **Evidencia**: qué archivo o línea demuestra que se cumple (o por qué no).

### 2. Revisión de la regla de dependencia

Verificar que:
- `dominio/` no importa de `aplicacion/` ni de `infraestructura/`.
- Los puertos están en `dominio/puertos/`.
- Los adaptadores están en `infraestructura/`.

### 3. Revisión de trazabilidad

- Cada tarea de tasks.md está marcada `[x]`.
- Cada escenario de spec.md aparece en al menos una tarea.
- Los nombres del código coinciden con el glosario.

## Reglas

- **No corregir nada**: solo reportar.
- Si algo no cumple, indicar qué falta y en qué archivo.
- **Detenerse** al terminar para la revisión humana.
