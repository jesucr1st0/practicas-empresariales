# Tareas: 010-registrar-empresa (CU-10 Registrar empresa)

Orden: de adentro hacia afuera (dominio → aplicación → infraestructura → entradas → pruebas → validación).

---

- [x] **T-01**: Crear la entidad `Supervisor`
  - **Archivo**: `src/modulos/practicas/dominio/supervisor.py`
  - **Escenarios**: 1, 3, 5
  - **Dependencias**: ninguna

- [x] **T-02**: Crear la entidad `Empresa`
  - **Archivo**: `src/modulos/practicas/dominio/empresa.py`
  - **Escenarios**: 1, 2, 3, 5
  - **Dependencias**: ninguna

- [x] **T-03**: Crear el puerto `EmpresaRepository`
  - **Archivo**: `src/modulos/practicas/dominio/puertos/empresa_repository.py`
  - **Escenarios**: 1, 2, 5
  - **Dependencias**: T-01, T-02

- [x] **T-04**: Crear los DTOs del módulo para empresas (`dto_empresa.py`)
  - **Archivo**: `src/modulos/practicas/aplicacion/dto_empresa.py`
  - **Escenarios**: 1, 2, 3, 5
  - **Dependencias**: ninguna

- [x] **T-05**: Crear el caso de uso `RegistrarEmpresa`
  - **Archivo**: `src/modulos/practicas/aplicacion/registrar_empresa.py`
  - **Escenarios**: 1, 2, 3
  - **Dependencias**: T-01, T-02, T-03, T-04

- [x] **T-06**: Crear el caso de uso `ConsultarEmpresa`
  - **Archivo**: `src/modulos/practicas/aplicacion/consultar_empresa.py`
  - **Escenarios**: 5
  - **Dependencias**: T-01, T-02, T-03, T-04

- [x] **T-07**: Crear el adaptador en memoria `AdaptadorEmpresaMemoria`
  - **Archivo**: `src/modulos/practicas/infraestructura/adaptador_empresa_memoria.py`
  - **Escenarios**: 1, 2, 5
  - **Dependencias**: T-01, T-02, T-03

- [x] **T-08**: Crear el controlador de entrada `ControladorEmpresa` con validación de roles y bitácora
  - **Archivo**: `src/entradas/controlador_empresa.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-05, T-06

- [x] **T-09**: Crear las pruebas automatizadas para CU-10 (Registrar empresa)
  - **Archivo**: `tests/test_registrar_empresa.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-01 a T-08

- [x] **T-10**: Validación de la especificación (ejecutar `prompts/5-validar.md`)
  - **Archivo**: `specs/010-registrar-empresa/validacion.md`
  - **Escenarios**: todos
  - **Dependencias**: T-01 a T-09
