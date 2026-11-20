# Tareas: 012-consultar-datos-estudiante (CU-12 Consultar datos estudiante)

Orden: de adentro hacia afuera (dominio → aplicación → infraestructura → entradas → pruebas → validación).

---

- [x] **T-01**: Crear el Value Object `DatosAcademicosEstudiante`
  - **Archivo**: `src/modulos/practicas/dominio/datos_academicos_estudiante.py`
  - **Escenarios**: 1, 2, 4, 5
  - **Dependencias**: ninguna

- [x] **T-02**: Crear el puerto `ConsultaAcademicaEstudiante` con excepciones de timeout y error SIA
  - **Archivo**: `src/modulos/practicas/dominio/puertos/consulta_academica_estudiante.py`
  - **Escenarios**: 1, 2, 4, 5
  - **Dependencias**: T-01

- [x] **T-03**: Actualizar el puerto `PracticaRepository` con métodos para consultar prácticas por tutor
  - **Archivo**: `src/modulos/practicas/dominio/puertos/practica_repository.py`
  - **Escenarios**: 2, 3
  - **Dependencias**: ninguna

- [x] **T-04**: Crear los DTOs de consulta de estudiante (`dto_consulta_estudiante.py`)
  - **Archivo**: `src/modulos/practicas/aplicacion/dto_consulta_estudiante.py`
  - **Escenarios**: 1, 2, 4, 5
  - **Dependencias**: T-01

- [x] **T-05**: Crear el caso de uso `ConsultarDatosEstudiante`
  - **Archivo**: `src/modulos/practicas/aplicacion/consultar_datos_estudiante.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-01, T-02, T-03, T-04

- [x] **T-06**: Actualizar el adaptador `AdaptadorPracticaMemoria`
  - **Archivo**: `src/modulos/practicas/infraestructura/adaptador_practica_memoria.py`
  - **Escenarios**: 2, 3
  - **Dependencias**: T-03

- [x] **T-07**: Crear el adaptador `AdaptadorSIAEstudianteMemoria`
  - **Archivo**: `src/modulos/practicas/infraestructura/adaptador_sia_estudiante_memoria.py`
  - **Escenarios**: 1, 2, 4, 5
  - **Dependencias**: T-02

- [x] **T-08**: Crear el controlador de entrada `ControladorConsultaEstudiante` con validación de roles, regla de alcance y bitácora
  - **Archivo**: `src/entradas/controlador_consulta_estudiante.py`
  - **Escenarios**: 1, 2, 3, 4, 5, 6
  - **Dependencias**: T-05

- [x] **T-09**: Crear las pruebas automatizadas para CU-12 (Consultar datos estudiante)
  - **Archivo**: `tests/test_consultar_datos_estudiante.py`
  - **Escenarios**: 1, 2, 3, 4, 5, 6
  - **Dependencias**: T-01 a T-08

- [x] **T-10**: Validación de la especificación (ejecutar `prompts/5-validar.md`)
  - **Archivo**: `specs/012-consultar-datos-estudiante/validacion.md`
  - **Escenarios**: todos
  - **Dependencias**: T-01 a T-09
