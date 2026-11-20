# Tareas: 009-registrar-tutor (CU-09 Registrar tutor)

Orden: de adentro hacia afuera (dominio → aplicación → infraestructura → entradas → pruebas → validación).

Escenarios de spec.md: 1 Registro exitoso · 2 Sin contraseña · 3 Documento repetido · 4 Rol no autorizado · 5 Datos incompletos.

---

- [x] **T-01**: Crear el puerto `TutorRepository`
  - **Archivo**: `src/modulos/tutores_asignacion/dominio/puertos/tutor_repository.py`
  - **Escenarios**: 1, 3
  - **Dependencias**: entidad `Tutor` existente (spec 001)

- [x] **T-02**: Crear el DTO de entrada `RegistrarTutorDTO`
  - **Archivo**: `src/modulos/tutores_asignacion/aplicacion/registrar_tutor_dto.py`
  - **Escenarios**: 1, 3, 5
  - **Dependencias**: ninguna

- [x] **T-03**: Crear el DTO de salida `ResultadoTutorDTO`
  - **Archivo**: `src/modulos/tutores_asignacion/aplicacion/resultado_tutor_dto.py`
  - **Escenarios**: 1, 2
  - **Dependencias**: ninguna

- [x] **T-04**: Crear el caso de uso `RegistrarTutor`
  - **Archivo**: `src/modulos/tutores_asignacion/aplicacion/registrar_tutor.py`
  - **Escenarios**: 1, 2, 3, 5
  - **Dependencias**: T-01, T-02, T-03

- [x] **T-05**: Crear el adaptador `AdaptadorTutorMemoria`
  - **Archivo**: `src/modulos/tutores_asignacion/infraestructura/adaptador_tutor_memoria.py`
  - **Escenarios**: 1, 3
  - **Dependencias**: T-01

- [x] **T-06**: Crear el controlador `ControladorTutor`
  - **Archivo**: `src/entradas/controlador_tutor.py`
  - **Escenarios**: 1, 3, 4, 5
  - **Dependencias**: T-04; `AutorizadorAccesos` de spec 007

- [x] **T-07**: Crear pruebas automatizadas para CU-09
  - **Archivo**: `tests/test_registrar_tutor.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-01 a T-06

- [x] **T-08**: Validación de la especificación (ejecutar `prompts/5-validar.md`)
  - **Archivo**: `specs/009-registrar-tutor/validacion.md`
  - **Escenarios**: todos
  - **Dependencias**: T-01 a T-07
