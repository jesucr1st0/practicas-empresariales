# Validación: 007-exportar-acta (CU-07 Exportar acta final)

## 1. Validación por escenario

| Escenario | Cumple | Evidencia |
|-----------|--------|-----------|
| **1. Exportación del acta vigente por el Coordinador (flujo básico, ADR-010)** | Sí | `src/entradas/controlador_exportar_acta.py` verifica el rol con `AutorizadorAccesos` e invoca `ExportarActaFinal`, que recupera el archivo guardado en CU-06 y compara su SHA-256 con la huella registrada. La bitácora guarda quién, qué, cuándo, IP y agente. Prueba: `tests/test_exportar_acta.py::test_escenario_1_coordinador_exporta_acta_vigente`. |
| **2. Exportación por el estudiante titular (ADR-005)** | Sí | `ExportarActaFinal._verificar_alcance_estudiante` consulta `ConsultaPracticaActa` y permite la exportación cuando el documento coincide. Prueba: `test_escenario_2_estudiante_titular_exporta_su_acta`. |
| **3. Estudiante intenta exportar el acta de una práctica ajena (ADR-005, RN-01)** | Sí | `ExportarActaFinal` lanza `PermissionError` por alcance; el controlador registra el intento fallido. Prueba: `test_escenario_3_estudiante_ajeno_es_denegado`. |
| **4. Rol no autorizado (ADR-005)** | Sí | `AutorizadorAccesos.verificar_rol` registra el intento fallido y lanza `PermissionError` antes de consultar el Módulo Actas. Prueba: `test_escenario_4_rol_no_autorizado_es_denegado`. |
| **5. Exportación después de una corrección (ADR-010)** | Sí | `ActaFinalRepository.buscar_vigente_por_practica` solo retorna el acta `VIGENTE`; la huella entregada es la del acta corregida. Prueba: `test_escenario_5_exporta_solo_el_acta_vigente_tras_correccion`. |
| **6. Práctica sin acta vigente** | Sí | `ExportarActaFinal` lanza `ValueError`; el controlador registra el intento fallido. Prueba: `test_escenario_6_practica_sin_acta_vigente`. |
| **7. Archivo del acta alterado (PA-04, ADR-010, ADR-011)** | Sí | La comparación de huella falla, no se retorna el archivo y la bitácora guarda el motivo de integridad. Prueba: `test_escenario_7_archivo_alterado_no_se_entrega`. |

## 2. Revisión de la regla de dependencia

- `dominio/` no importa de `aplicacion/` ni de `infraestructura/` (verificado con búsqueda de imports en `src/modulos/*/dominio`: 0 coincidencias).
- `rol.py` y `usuario_autenticado.py` están en `identidad_accesos/dominio/`; `AutorizadorAccesos` está en `identidad_accesos/aplicacion/` y depende solo del puerto `BitacoraAccesoRepository`.
- `ExportarActaFinal` depende solo de puertos de `actas/dominio/puertos/`; no importa del Módulo Identidad y accesos.
- La autorización y la bitácora se aplican en el adaptador de entrada `src/entradas/controlador_exportar_acta.py`, como pide la vista de desarrollo (RN-01 / ADR-005).

## 3. Revisión de trazabilidad

- Tareas T-01 a T-07 de `tasks.md` marcadas `[x]`.
- Los 7 escenarios de `spec.md` aparecen en al menos una tarea y tienen una prueba en `tests/test_exportar_acta.py`.
- Nombres alineados con el glosario: `ActaFinal`, `EstadoActa`, `AlmacenArchivos`, `RegistroAcceso`, `ActaFinalRepository`.
- Suite completa del proyecto: 28 pruebas aprobadas.

## 4. Observación (fuera del alcance de CU-07)

- `GenerarActaFinal` (spec 006) arma la ruta del archivo con la marca de tiempo en segundos (`actas/<practica>_<segundos>.pdf`). Si una corrección se emite en el mismo segundo que el acta anterior, el archivo nuevo sobrescribe al anterior en el almacén, y el acta anulada pierde su documento original (escenario 4 de spec 006: «conserva ambas actas»). No afecta a CU-07 porque solo se exporta el acta vigente; se reporta para que lo corrija el responsable del spec 006.
