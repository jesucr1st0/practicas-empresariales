# Tareas: 001-asignar-tutor (CU-01 Asignar tutor)

Orden: de adentro hacia afuera (dominio → aplicación → infraestructura → entradas).

---

- [x] **T-01**: Crear el enum `OrigenAsignacion`
  - **Archivo**: `src/modulos/tutores_asignacion/dominio/origen_asignacion.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: ninguna

- [x] **T-02**: Crear la entidad `AsignacionTutor`
  - **Archivo**: `src/modulos/tutores_asignacion/dominio/asignacion_tutor.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-01

- [x] **T-02a**: Crear la entidad `Tutor`
  - **Archivo**: `src/modulos/tutores_asignacion/dominio/tutor.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-01

- [x] **T-03**: Crear el puerto `AsignacionRepository`
  - **Archivo**: `src/modulos/tutores_asignacion/dominio/puertos/asignacion_repository.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-02, T-02a

- [x] **T-04**: Crear el puerto `ConsultaPracticaAsignacion`
  - **Archivo**: `src/modulos/tutores_asignacion/dominio/puertos/consulta_practica_asignacion.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: ninguna

- [x] **T-04a**: Crear el puerto `ConsultaReglaTutor`
  - **Archivo**: `src/modulos/tutores_asignacion/dominio/puertos/consulta_regla_tutor.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: ninguna

- [x] **T-05a**: Crear `ConfirmarAsignacionDTO`
  - **Archivo**: `src/modulos/tutores_asignacion/aplicacion/confirmar_asignacion_dto.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-01

- [x] **T-05b**: Crear `ResultadoAsignacionDTO`
  - **Archivo**: `src/modulos/tutores_asignacion/aplicacion/resultado_asignacion_dto.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-02

- [x] **T-05c**: Crear `SugerenciaTutorDTO`
  - **Archivo**: `src/modulos/tutores_asignacion/aplicacion/sugerencia_tutor_dto.py`
  - **Escenarios**: 1, 2, 3
  - **Dependencias**: T-02a

- [x] **T-05**: Crear el módulo público de DTOs
  - **Archivo**: `src/modulos/tutores_asignacion/aplicacion/dto.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-05a, T-05b, T-05c

- [x] **T-06**: Crear el caso de uso `SugerirTutor`
  - **Archivo**: `src/modulos/tutores_asignacion/aplicacion/sugerir_tutor.py`
  - **Escenarios**: 1, 2, 3
  - **Dependencias**: T-02, T-02a, T-03, T-04, T-04a, T-05, T-05c

- [x] **T-07**: Crear el caso de uso `ConfirmarAsignacion`
  - **Archivo**: `src/modulos/tutores_asignacion/aplicacion/confirmar_asignacion.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-02, T-02a, T-03, T-04, T-04a, T-05, T-05a, T-05b, T-05c

- [x] **T-08**: Crear el adaptador de persistencia en memoria `AdaptadorAsignacionMemoria`
  - **Archivo**: `src/modulos/tutores_asignacion/infraestructura/adaptador_asignacion_memoria.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-02a, T-03

- [x] **T-09**: Crear el adaptador auxiliar en memoria para consulta de práctica
  - **Archivo**: `src/modulos/tutores_asignacion/infraestructura/adaptador_servicio_practica_memoria.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-04

- [x] **T-09a**: Crear el adaptador en memoria para consulta de regla
  - **Archivo**: `src/modulos/tutores_asignacion/infraestructura/adaptador_servicio_reglas_memoria.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-04a

- [x] **T-10**: Crear el controlador de entrada `ControladorAsignacionTutor`
  - **Archivo**: `src/entradas/controlador_asignacion_tutor.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-06, T-07

- [x] **T-10a**: Agregar pruebas de los cuatro escenarios de asignación
  - **Archivo**: `tests/test_asignacion_tutor.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-01 a T-10, T-02a, T-04a, T-05a, T-05b, T-05c, T-09a

- [x] **T-11**: Validación de la especificación (ejecutar `prompts/5-validar.md`)
  - **Archivo**: `specs/001-asignar-tutor/validacion.md`
  - **Escenarios**: todos
  - **Dependencias**: T-01 a T-10, T-02a, T-04a, T-05a, T-05b, T-05c, T-09a, T-10a
