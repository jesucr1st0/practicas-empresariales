# Tareas: 011-consultar-datos-tutor (CU-11 Consultar datos tutor)

Orden: de adentro hacia afuera (dominio → aplicación → infraestructura → entradas → pruebas → validación).

---

- [x] **T-01**: Crear el Value Object `DatosAcademicosTutor`
  - **Archivo**: `src/modulos/tutores_asignacion/dominio/datos_academicos_tutor.py`
  - **Escenarios**: 1, 4
  - **Dependencias**: ninguna

- [x] **T-02**: Crear el puerto `ConsultaAcademicaTutor` con excepciones de timeout y error SIA
  - **Archivo**: `src/modulos/tutores_asignacion/dominio/puertos/consulta_academica_tutor.py`
  - **Escenarios**: 1, 4
  - **Dependencias**: T-01

- [x] **T-03**: Actualizar el puerto `AsignacionRepository` con métodos para consultar tutor por documento y asignaciones vigentes por tutor
  - **Archivo**: `src/modulos/tutores_asignacion/dominio/puertos/asignacion_repository.py`
  - **Escenarios**: 1, 2, 5
  - **Dependencias**: ninguna

- [x] **T-04**: Crear los DTOs de consulta de tutor (`DatosTutorDTO`, `ResumenTutorDTO`, `PracticaAsignadaDTO`)
  - **Archivo**: `src/modulos/tutores_asignacion/aplicacion/dto_consulta_tutor.py`
  - **Escenarios**: 1, 2, 4, 5
  - **Dependencias**: T-01

- [x] **T-05**: Crear el caso de uso `ConsultarDatosTutor`
  - **Archivo**: `src/modulos/tutores_asignacion/aplicacion/consultar_datos_tutor.py`
  - **Escenarios**: 1, 2, 4
  - **Dependencias**: T-01, T-02, T-03, T-04

- [x] **T-06**: Crear el caso de uso `ListarTutoresPrograma`
  - **Archivo**: `src/modulos/tutores_asignacion/aplicacion/listar_tutores_programa.py`
  - **Escenarios**: 5
  - **Dependencias**: T-03, T-04

- [x] **T-07**: Actualizar el adaptador `AdaptadorAsignacionMemoria` para implementar las nuevas operaciones del repositorio
  - **Archivo**: `src/modulos/tutores_asignacion/infraestructura/adaptador_asignacion_memoria.py`
  - **Escenarios**: 1, 2, 5
  - **Dependencias**: T-03

- [x] **T-08**: Crear el adaptador `AdaptadorSIATutorMemoria` para simular la integración con el SIA
  - **Archivo**: `src/modulos/tutores_asignacion/infraestructura/adaptador_sia_tutor_memoria.py`
  - **Escenarios**: 1, 4
  - **Dependencias**: T-02

- [x] **T-09**: Crear el controlador de entrada `ControladorConsultaTutor` con validación de roles y bitácora
  - **Archivo**: `src/entradas/controlador_consulta_tutor.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-05, T-06

- [x] **T-10**: Crear las pruebas automatizadas de consulta de datos del tutor para CU-11
  - **Archivo**: `tests/test_consultar_datos_tutor.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-01 a T-09

- [x] **T-11**: Validación de la especificación (ejecutar `prompts/5-validar.md`)
  - **Archivo**: `specs/011-consultar-datos-tutor/validacion.md`
  - **Escenarios**: todos
  - **Dependencias**: T-01 a T-10
