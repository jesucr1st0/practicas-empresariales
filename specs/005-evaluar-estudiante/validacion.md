# Validación: 005-evaluar-estudiante (CU-05 Evaluar al estudiante por la empresa)

## 1. Validación por escenario

| Escenario | Cumple | Evidencia |
|-----------|--------|-----------|
| **1. Evaluación exitosa por el supervisor sin cuenta ni contraseña (flujo básico, EAC-02, RN-04)** | Sí | `src/entradas/controlador_acceso_externo_evaluacion.py` y `src/modulos/evaluaciones/aplicacion/registrar_evaluacion.py` registran la `Evaluacion`, notifican a prácticas, invalidan el enlace a `USADO` y registran el acceso en bitácora. Verificado en `tests/test_evaluar_estudiante.py::EvaluarEstudianteTests.test_escenario_1_evaluacion_exitosa_sin_contraseña_invalida_enlace`. |
| **2. Envío de recordatorio periódico de evaluación pendiente (ADR-013)** | Sí | `src/modulos/evaluaciones/aplicacion/enviar_recordatorio_evaluacion.py` envía recordatorio solo si la evaluación no ha sido registrada. Verificado en `tests/test_evaluar_estudiante.py::EvaluarEstudianteTests.test_escenario_2_recordatorio_evaluacion_pendiente`. |
| **3. Intento de reenvío con enlace ya usado (ADR-006, EAC-02)** | Sí | `GestorEnlacesAcceso.validar_token` detecta estado `USADO`, registra el acceso no autorizado en bitácora y lanza error informativo ("enlace no disponible; pida al coordinador que lo reemita"). Verificado en `tests/test_evaluar_estudiante.py::EvaluarEstudianteTests.test_escenario_3_intento_reenvio_con_enlace_ya_usado`. |
| **4. Acceso con enlace vencido por tiempo superior a 30 días (ADR-006)** | Sí | `GestorEnlacesAcceso.validar_token` detecta vencimiento, registra en bitácora y deniega acceso. Verificado en `tests/test_evaluar_estudiante.py::EvaluarEstudianteTests.test_escenario_4_acceso_enlace_vencido_denegado`. |
| **5. Intento de registrar una segunda evaluación en una práctica que ya tiene evaluación** | Sí | `RegistrarEvaluacion` verifica regla 1 a 0..1 del modelo lógico y rechaza evaluación duplicada con `ValueError`. Verificado en `tests/test_evaluar_estudiante.py::EvaluarEstudianteTests.test_escenario_5_rechazo_segunda_evaluacion_misma_practica`. |

## 2. Revisión de la regla de dependencia

- `dominio/` no importa de `aplicacion/` ni de `infraestructura/` (0 violaciones verificadas estáticamente).
- Los puertos se encuentran en `dominio/puertos/` (`evaluacion_repository.py`, `servicio_actualizacion_practica_evaluacion.py`, `servicio_invalidacion_enlace.py`, `servicio_recordatorio_evaluacion.py`).
- Los adaptadores implementan los puertos en `infraestructura/` (`adaptador_evaluacion_memoria.py`, `adaptador_servicio_practica_evaluacion_memoria.py`, `adaptador_servicio_invalidacion_enlace_memoria.py`, `adaptador_servicio_recordatorio_memoria.py`).
- Los adaptadores de entrada residen en `src/entradas/` (`controlador_acceso_externo_evaluacion.py`).

## 3. Revisión de trazabilidad

- Todas las tareas de `tasks.md` (T-01 a T-16) están marcadas `[x]`.
- Todos los escenarios de `spec.md` cuentan con pruebas automatizadas en `tests/test_evaluar_estudiante.py`.
- Nombres alineados con el glosario oficial: `Evaluacion`, `Practica`, `EnlaceAcceso`, `EstadoEnlace`, `RegistroAcceso`.
- 16 pruebas totales de la suite del proyecto aprobadas sin errores.
