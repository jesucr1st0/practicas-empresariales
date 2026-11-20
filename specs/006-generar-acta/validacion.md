# Validación: 006-generar-acta (CU-06 Generar acta final)

## 1. Validación por escenario

| Escenario | Cumple | Evidencia |
|-----------|--------|-----------|
| **1. Generación exitosa de acta final (flujo básico, ADR-010, RN-03)** | Sí | `src/modulos/actas/aplicacion/generar_acta_final.py` verifica precondiciones, genera documento con plantilla oficial versionada, calcula huella SHA-256, persiste en `AlmacenArchivos` y registra en `ActaFinalRepository`. Verificado en `tests/test_generar_acta.py::GenerarActaTests.test_escenario_1_generacion_exitosa_acta_final`. |
| **2. Rechazo por horas validadas insuficientes** | Sí | `GenerarActaFinal` consulta la versión de regla de la práctica vía `ConsultaReglasActa` y rechaza con `ValueError` detallado si las horas validadas no alcanzan el mínimo (EAC-01). Verificado en `tests/test_generar_acta.py::GenerarActaTests.test_escenario_2_rechazo_horas_validadas_insuficientes`. |
| **3. Rechazo por evaluación de empresa pendiente** | Sí | `GenerarActaFinal` valida la presencia de evaluación vía `ConsultaEvaluacionActa` y rechaza la emisión si está ausente. Verificado en `tests/test_generar_acta.py::GenerarActaTests.test_escenario_3_rechazo_evaluacion_empresa_pendiente`. |
| **4. Corrección de acta final generando una nueva y anulando la anterior (ADR-010)** | Sí | Al emitir una nueva acta sobre una práctica con acta previa, la anterior pasa a estado `ANULADA` y se conserva en el repositorio y almacén sin ser editada ni borrada. Verificado en `tests/test_generar_acta.py::GenerarActaTests.test_escenario_4_correccion_acta_anula_anterior_conservando_inmutabilidad`. |
| **5. Exportar y verificar integridad del acta final (CU-07)** | Sí | `src/modulos/actas/aplicacion/exportar_acta_final.py` recupera el archivo original y verifica que su SHA-256 coincida con la huella registrada, alertando si hay alteración (ADR-010). Verificado en `tests/test_generar_acta.py::GenerarActaTests.test_escenario_5_exportar_acta_final_y_verificar_integridad`. |

## 2. Revisión de la regla de dependencia

- `dominio/` no importa nada de `aplicacion/` ni de `infraestructura/` (0 violaciones verificadas estáticamente).
- Los puertos se ubican en `dominio/puertos/` (`acta_final_repository.py`, `almacen_archivos.py`, `consulta_practica_acta.py`, `consulta_horas_acta.py`, `consulta_evaluacion_acta.py`, `consulta_reglas_acta.py`, `generador_plantilla_acta.py`).
- Los adaptadores implementan los puertos en `infraestructura/` (`adaptador_acta_final_memoria.py`, `adaptador_almacen_archivos_memoria.py`, `adaptador_consulta_practica_memoria.py`, `adaptador_consulta_horas_memoria.py`, `adaptador_consulta_evaluacion_memoria.py`, `adaptador_consulta_reglas_memoria.py`, `adaptador_generador_plantilla_oficial.py`).
- El controlador de entrada reside en `src/entradas/` (`controlador_actas.py`).

## 3. Revisión de trazabilidad

- Todas las tareas de `tasks.md` (T-01 a T-22) están completadas y marcadas `[x]`.
- Todos los escenarios de `spec.md` tienen pruebas correspondientes en `tests/test_generar_acta.py`.
- Nombres alineados con el glosario oficial: `ActaFinal`, `EstadoActa`, `AlmacenArchivos`, `ActaFinalRepository`.
- 21 pruebas totales de la suite del proyecto aprobadas sin errores.
