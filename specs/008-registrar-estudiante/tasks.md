# Tareas: 008-registrar-estudiante (CU-08 Registrar estudiante)

Orden: de adentro hacia afuera (dominio → aplicación → infraestructura → entradas → pruebas → validación).

Escenarios de spec.md: 1 Registro exitoso · 2 Sin contraseña ni datos académicos · 3 Documento repetido · 4 Rol no autorizado · 5 Datos incompletos.

---

- [x] **T-01**: Crear la entidad `Estudiante`
  - **Archivo**: `src/modulos/practicas/dominio/estudiante.py`
  - **Escenarios**: 1, 2, 5
  - **Dependencias**: ninguna

- [x] **T-02**: Crear el puerto `EstudianteRepository`
  - **Archivo**: `src/modulos/practicas/dominio/puertos/estudiante_repository.py`
  - **Escenarios**: 1, 3
  - **Dependencias**: T-01

- [x] **T-03**: Crear el DTO de entrada `RegistrarEstudianteDTO`
  - **Archivo**: `src/modulos/practicas/aplicacion/registrar_estudiante_dto.py`
  - **Escenarios**: 1, 3, 5
  - **Dependencias**: ninguna

- [x] **T-04**: Crear el DTO de salida `ResultadoEstudianteDTO`
  - **Archivo**: `src/modulos/practicas/aplicacion/resultado_estudiante_dto.py`
  - **Escenarios**: 1, 2
  - **Dependencias**: ninguna

- [x] **T-05**: Crear el caso de uso `RegistrarEstudiante`
  - **Archivo**: `src/modulos/practicas/aplicacion/registrar_estudiante.py`
  - **Escenarios**: 1, 2, 3, 5
  - **Dependencias**: T-01, T-02, T-03, T-04

- [x] **T-06**: Crear el adaptador `AdaptadorEstudianteMemoria`
  - **Archivo**: `src/modulos/practicas/infraestructura/adaptador_estudiante_memoria.py`
  - **Escenarios**: 1, 3
  - **Dependencias**: T-02

- [x] **T-07**: Crear el controlador `ControladorEstudiante`
  - **Archivo**: `src/entradas/controlador_estudiante.py`
  - **Escenarios**: 1, 3, 4, 5
  - **Dependencias**: T-05; `AutorizadorAccesos` de spec 007

- [x] **T-08**: Crear pruebas automatizadas para CU-08
  - **Archivo**: `tests/test_registrar_estudiante.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-01 a T-07

- [x] **T-09**: Validación de la especificación (ejecutar `prompts/5-validar.md`)
  - **Archivo**: `specs/008-registrar-estudiante/validacion.md`
  - **Escenarios**: todos
  - **Dependencias**: T-01 a T-08
