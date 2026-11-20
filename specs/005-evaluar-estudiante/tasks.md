# Tareas: 005-evaluar-estudiante (CU-05 Evaluar al estudiante por la empresa)

Orden: de adentro hacia afuera (dominio → aplicación → infraestructura → entradas → pruebas → validación).

---

- [x] **T-01**: Crear la entidad `Evaluacion`
  - **Archivo**: `src/modulos/evaluaciones/dominio/evaluacion.py`
  - **Escenarios**: 1, 5
  - **Dependencias**: ninguna

- [x] **T-02**: Crear el puerto `EvaluacionRepository`
  - **Archivo**: `src/modulos/evaluaciones/dominio/puertos/evaluacion_repository.py`
  - **Escenarios**: 1, 5
  - **Dependencias**: T-01

- [x] **T-03**: Crear el puerto `ServicioActualizacionPracticaEvaluacion`
  - **Archivo**: `src/modulos/evaluaciones/dominio/puertos/servicio_actualizacion_practica_evaluacion.py`
  - **Escenarios**: 1
  - **Dependencias**: ninguna

- [x] **T-04**: Crear el puerto `ServicioInvalidacionEnlace`
  - **Archivo**: `src/modulos/evaluaciones/dominio/puertos/servicio_invalidacion_enlace.py`
  - **Escenarios**: 1, 3
  - **Dependencias**: ninguna

- [x] **T-05**: Crear el puerto `ServicioRecordatorioEvaluacion`
  - **Archivo**: `src/modulos/evaluaciones/dominio/puertos/servicio_recordatorio_evaluacion.py`
  - **Escenarios**: 2
  - **Dependencias**: ninguna

- [x] **T-06**: Crear los DTOs del módulo Evaluaciones
  - **Archivo**: `src/modulos/evaluaciones/aplicacion/dto.py`
  - **Escenarios**: 1, 5
  - **Dependencias**: T-01

- [x] **T-07**: Crear el caso de uso `RegistrarEvaluacion`
  - **Archivo**: `src/modulos/evaluaciones/aplicacion/registrar_evaluacion.py`
  - **Escenarios**: 1, 3, 5
  - **Dependencias**: T-01, T-02, T-03, T-04, T-06

- [x] **T-08**: Crear el caso de uso `ConsultarEvaluacion`
  - **Archivo**: `src/modulos/evaluaciones/aplicacion/consultar_evaluacion.py`
  - **Escenarios**: 1, 5
  - **Dependencias**: T-01, T-02, T-06

- [x] **T-09**: Crear el caso de uso `EnviarRecordatorioEvaluacion`
  - **Archivo**: `src/modulos/evaluaciones/aplicacion/enviar_recordatorio_evaluacion.py`
  - **Escenarios**: 2
  - **Dependencias**: T-02, T-05

- [x] **T-10**: Crear el adaptador `AdaptadorEvaluacionMemoria`
  - **Archivo**: `src/modulos/evaluaciones/infraestructura/adaptador_evaluacion_memoria.py`
  - **Escenarios**: 1, 5
  - **Dependencias**: T-02

- [x] **T-11**: Crear el adaptador `AdaptadorServicioPracticaEvaluacionMemoria`
  - **Archivo**: `src/modulos/evaluaciones/infraestructura/adaptador_servicio_practica_evaluacion_memoria.py`
  - **Escenarios**: 1
  - **Dependencias**: T-03

- [x] **T-12**: Crear el adaptador `AdaptadorServicioInvalidacionEnlaceMemoria`
  - **Archivo**: `src/modulos/evaluaciones/infraestructura/adaptador_servicio_invalidacion_enlace_memoria.py`
  - **Escenarios**: 1, 3
  - **Dependencias**: T-04

- [x] **T-13**: Crear el adaptador `AdaptadorServicioRecordatorioMemoria`
  - **Archivo**: `src/modulos/evaluaciones/infraestructura/adaptador_servicio_recordatorio_memoria.py`
  - **Escenarios**: 2
  - **Dependencias**: T-05

- [x] **T-14**: Crear el controlador `ControladorAccesoExternoEvaluacion`
  - **Archivo**: `src/entradas/controlador_acceso_externo_evaluacion.py`
  - **Escenarios**: 1, 3, 4
  - **Dependencias**: T-07

- [x] **T-15**: Crear pruebas automatizadas para CU-05
  - **Archivo**: `tests/test_evaluar_estudiante.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-01 a T-14

- [x] **T-16**: Validación de la especificación (ejecutar `prompts/5-validar.md`)
  - **Archivo**: `specs/005-evaluar-estudiante/validacion.md`
  - **Escenarios**: todos
  - **Dependencias**: T-01 a T-15
