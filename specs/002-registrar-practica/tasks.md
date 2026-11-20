# Tareas: 002-registrar-practica (CU-02 Registrar práctica)

Orden: de adentro hacia afuera (dominio → aplicación → infraestructura → entradas).

---

- [x] **T-01**: Crear la entidad `ReglaPrograma` en Módulo Reglas
  - **Archivo**: `src/modulos/reglas/dominio/regla_programa.py`
  - **Escenarios**: 1, 4, 5
  - **Dependencias**: ninguna

- [x] **T-02**: Crear el puerto `ReglaRepository` en Módulo Reglas
  - **Archivo**: `src/modulos/reglas/dominio/puertos/regla_repository.py`
  - **Escenarios**: 1, 4, 5
  - **Dependencias**: T-01

- [x] **T-03**: Crear el caso de uso `ResolverReglaVigente` en Módulo Reglas
  - **Archivo**: `src/modulos/reglas/aplicacion/resolver_regla_vigente.py`
  - **Escenarios**: 1, 4, 5
  - **Dependencias**: T-01, T-02

- [x] **T-04**: Crear el adaptador `AdaptadorReglaMemoria` en Módulo Reglas
  - **Archivo**: `src/modulos/reglas/infraestructura/adaptador_regla_memoria.py`
  - **Escenarios**: 1, 4, 5
  - **Dependencias**: T-02

- [x] **T-05**: Crear el enum `EstadoPractica` en Módulo Prácticas
  - **Archivo**: `src/modulos/practicas/dominio/estado_practica.py`
  - **Escenarios**: 1, 2, 5
  - **Dependencias**: ninguna

- [x] **T-06**: Crear la entidad `Practica` en Módulo Prácticas
  - **Archivo**: `src/modulos/practicas/dominio/practica.py`
  - **Escenarios**: 1, 2, 5
  - **Dependencias**: T-05

- [x] **T-07**: Crear el puerto `PracticaRepository` en Módulo Prácticas
  - **Archivo**: `src/modulos/practicas/dominio/puertos/practica_repository.py`
  - **Escenarios**: 1, 2, 5
  - **Dependencias**: T-06

- [x] **T-08**: Crear los puertos `ServicioConsultaPostulacion` y `ServicioConsultaReglas` en Módulo Prácticas
  - **Archivo**: `src/modulos/practicas/dominio/puertos/servicio_consulta_reglas.py` y `src/modulos/practicas/dominio/puertos/servicio_consulta_postulacion.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: ninguna

- [x] **T-09**: Crear los DTOs `RegistrarPracticaDTO` y `ResultadoPracticaDTO` en Módulo Prácticas
  - **Archivo**: `src/modulos/practicas/aplicacion/dto.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-05

- [x] **T-10**: Crear el caso de uso `RegistrarPractica` en Módulo Prácticas
  - **Archivo**: `src/modulos/practicas/aplicacion/registrar_practica.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-06, T-07, T-08, T-09

- [x] **T-11**: Crear los adaptadores en memoria para Prácticas e integraciones
  - **Archivo**: `src/modulos/practicas/infraestructura/adaptador_practica_memoria.py` y `src/modulos/practicas/infraestructura/adaptadores_servicios.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-07, T-08

- [x] **T-12**: Crear el controlador de entrada `ControladorPractica`
  - **Archivo**: `src/entradas/controlador_practica.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-10

- [x] **T-13**: Validación completa de la especificación (ejecutar `prompts/5-validar.md`)
  - **Archivo**: `specs/002-registrar-practica/validacion.md`
  - **Escenarios**: todos (1 al 5)
  - **Dependencias**: T-01 a T-12
