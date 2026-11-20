# Validación: 001-asignar-tutor (CU-01)

## 1. Validación por escenario

| Escenario | Cumple | Evidencia |
|-----------|--------|-----------|
| Sugerencia automática y confirmación directa | Sí | [sugerir_tutor.py](../../src/modulos/tutores_asignacion/aplicacion/sugerir_tutor.py) elige menor carga; [confirmar_asignacion.py](../../src/modulos/tutores_asignacion/aplicacion/confirmar_asignacion.py) persiste el origen y actualiza el tutor vigente. [test_asignacion_tutor.py](../../tests/test_asignacion_tutor.py) cubre carga 4 frente a 7. |
| Coordinador ajusta y elige otro tutor manualmente | Sí | [confirmar_asignacion.py](../../src/modulos/tutores_asignacion/aplicacion/confirmar_asignacion.py) guarda el tutor elegido con origen manual; [test_asignacion_tutor.py](../../tests/test_asignacion_tutor.py) verifica que la sugerencia no confirmada no se persiste. |
| Advertencia por superación de capacidad máxima | Sí | [confirmar_asignacion.py](../../src/modulos/tutores_asignacion/aplicacion/confirmar_asignacion.py) devuelve advertencia sin asignar hasta recibir confirmación explícita y registra carga/capacidad en observaciones. [test_asignacion_tutor.py](../../tests/test_asignacion_tutor.py) cubre 8/8 para Ingeniería Industrial. Corresponde a ADR-012; EAC-01 trata el cambio de horas mínimas. |
| Reasignación de tutor conservando historial | Sí | [confirmar_asignacion.py](../../src/modulos/tutores_asignacion/aplicacion/confirmar_asignacion.py) conserva la asignación previa y guarda la nueva; [adaptador_servicio_practica_memoria.py](../../src/modulos/tutores_asignacion/infraestructura/adaptador_servicio_practica_memoria.py) actualiza el tutor vigente y su alcance. [test_asignacion_tutor.py](../../tests/test_asignacion_tutor.py) verifica que el anterior pierde y el nuevo obtiene el alcance. |

El controlador simula el control de rol y requiere un callback de registro de acceso. La integración con SSO y el adaptador real de bitácora quedan fuera de alcance según `plan.md`.

## 2. Revisión de la regla de dependencia

- **Cumple:** [dominio/](../../src/modulos/tutores_asignacion/dominio/) no importa de aplicación ni infraestructura.
- **Cumple:** los puertos están en [dominio/puertos/](../../src/modulos/tutores_asignacion/dominio/puertos/).
- **Cumple:** los adaptadores están en [infraestructura/](../../src/modulos/tutores_asignacion/infraestructura/).

## 3. Revisión de trazabilidad

- **Cumple:** todas las tareas de `tasks.md` están marcadas `[x]`.
- **Cumple:** los cuatro escenarios aparecen en las tareas T-01 a T-10a.
- **Cumple:** los nombres de las entidades y casos de uso siguen el glosario y el plan.
- **Pruebas:** `python -B -m unittest discover -s tests -v` — 5 pruebas aprobadas.
