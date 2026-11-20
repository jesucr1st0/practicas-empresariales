# Tareas: 004-seguimiento-horas (CU-04 Realizar seguimiento en horas)

Orden: de adentro hacia afuera (dominio → aplicación → infraestructura → entradas → pruebas → validación).

---

- [x] **T-01**: Crear el enum `EstadoValidacionHoras`
  - **Archivo**: `src/modulos/horas/dominio/estado_validacion_horas.py`
  - **Escenarios**: 1, 2, 5
  - **Dependencias**: ninguna

- [x] **T-02**: Crear la entidad `RegistroHoras`
  - **Archivo**: `src/modulos/horas/dominio/registro_horas.py`
  - **Escenarios**: 1, 2, 5
  - **Dependencias**: T-01

- [x] **T-03**: Crear el enum `EstadoEnlace`
  - **Archivo**: `src/modulos/identidad_accesos/dominio/estado_enlace.py`
  - **Escenarios**: 4, 5, 6
  - **Dependencias**: ninguna

- [x] **T-04**: Crear la entidad `EnlaceAcceso`
  - **Archivo**: `src/modulos/identidad_accesos/dominio/enlace_acceso.py`
  - **Escenarios**: 4, 5, 6
  - **Dependencias**: T-03

- [x] **T-05**: Crear la entidad `RegistroAcceso`
  - **Archivo**: `src/modulos/identidad_accesos/dominio/registro_acceso.py`
  - **Escenarios**: 3, 5, 6
  - **Dependencias**: ninguna

- [x] **T-06**: Crear el puerto `RegistroHorasRepository`
  - **Archivo**: `src/modulos/horas/dominio/puertos/registro_horas_repository.py`
  - **Escenarios**: 1, 2, 5
  - **Dependencias**: T-02

- [x] **T-07**: Crear el puerto `ConsultaAsignacionTutor`
  - **Archivo**: `src/modulos/horas/dominio/puertos/consulta_asignacion_tutor.py`
  - **Escenarios**: 2, 3
  - **Dependencias**: ninguna

- [x] **T-08**: Crear el puerto `ServicioEnlaceHoras`
  - **Archivo**: `src/modulos/horas/dominio/puertos/servicio_enlace_horas.py`
  - **Escenarios**: 4
  - **Dependencias**: ninguna

- [x] **T-09**: Crear el puerto `ServicioNotificacionHoras`
  - **Archivo**: `src/modulos/horas/dominio/puertos/servicio_notificacion_horas.py`
  - **Escenarios**: 4
  - **Dependencias**: ninguna

- [x] **T-10**: Crear el puerto `EnlaceAccesoRepository`
  - **Archivo**: `src/modulos/identidad_accesos/dominio/puertos/enlace_acceso_repository.py`
  - **Escenarios**: 4, 5, 6
  - **Dependencias**: T-04

- [x] **T-11**: Crear el puerto `BitacoraAccesoRepository`
  - **Archivo**: `src/modulos/identidad_accesos/dominio/puertos/bitacora_acceso_repository.py`
  - **Escenarios**: 3, 5, 6
  - **Dependencias**: T-05

- [x] **T-12**: Crear los DTOs del módulo Horas
  - **Archivo**: `src/modulos/horas/aplicacion/dto.py`
  - **Escenarios**: 1, 2, 3, 5
  - **Dependencias**: T-01, T-02

- [x] **T-13**: Crear el caso de uso `RegistrarHoras`
  - **Archivo**: `src/modulos/horas/aplicacion/registrar_horas.py`
  - **Escenarios**: 1
  - **Dependencias**: T-02, T-06, T-12

- [x] **T-14**: Crear el caso de uso `ConsultarHorasTutor`
  - **Archivo**: `src/modulos/horas/aplicacion/consultar_horas_tutor.py`
  - **Escenarios**: 2, 3
  - **Dependencias**: T-02, T-06, T-07, T-11, T-12

- [x] **T-15**: Crear el servicio `GestorEnlacesAcceso`
  - **Archivo**: `src/modulos/identidad_accesos/aplicacion/gestor_enlaces_acceso.py`
  - **Escenarios**: 4, 5, 6
  - **Dependencias**: T-04, T-05, T-10, T-11

- [x] **T-16**: Crear el caso de uso `SolicitarValidacionSupervisor`
  - **Archivo**: `src/modulos/horas/aplicacion/solicitar_validacion_supervisor.py`
  - **Escenarios**: 4
  - **Dependencias**: T-06, T-08, T-09

- [x] **T-17**: Crear el caso de uso `ConsultarHorasSupervisor`
  - **Archivo**: `src/modulos/horas/aplicacion/consultar_horas_supervisor.py`
  - **Escenarios**: 5
  - **Dependencias**: T-06, T-12

- [x] **T-18**: Crear el caso de uso `ValidarHorasSupervisor`
  - **Archivo**: `src/modulos/horas/aplicacion/validar_horas_supervisor.py`
  - **Escenarios**: 5
  - **Dependencias**: T-02, T-06, T-12

- [x] **T-19**: Crear el adaptador `AdaptadorRegistroHorasMemoria`
  - **Archivo**: `src/modulos/horas/infraestructura/adaptador_registro_horas_memoria.py`
  - **Escenarios**: 1, 2, 5
  - **Dependencias**: T-06

- [x] **T-20**: Crear el adaptador `AdaptadorEnlaceAccesoMemoria`
  - **Archivo**: `src/modulos/identidad_accesos/infraestructura/adaptador_enlace_acceso_memoria.py`
  - **Escenarios**: 4, 5, 6
  - **Dependencias**: T-10

- [x] **T-21**: Crear el adaptador `AdaptadorBitacoraMemoria`
  - **Archivo**: `src/modulos/identidad_accesos/infraestructura/adaptador_bitacora_memoria.py`
  - **Escenarios**: 3, 5, 6
  - **Dependencias**: T-11

- [x] **T-22**: Crear el adaptador `AdaptadorConsultaAsignacionMemoria`
  - **Archivo**: `src/modulos/horas/infraestructura/adaptador_consulta_asignacion_memoria.py`
  - **Escenarios**: 2, 3
  - **Dependencias**: T-07

- [x] **T-23**: Crear el adaptador `AdaptadorServicioEnlaceMemoria`
  - **Archivo**: `src/modulos/horas/infraestructura/adaptador_servicio_enlace_memoria.py`
  - **Escenarios**: 4
  - **Dependencias**: T-08, T-15

- [x] **T-24**: Crear el adaptador `AdaptadorServicioNotificacionMemoria`
  - **Archivo**: `src/modulos/horas/infraestructura/adaptador_servicio_notificacion_memoria.py`
  - **Escenarios**: 4
  - **Dependencias**: T-09

- [x] **T-25**: Crear el controlador `ControladorHorasInterno`
  - **Archivo**: `src/entradas/controlador_horas_interno.py`
  - **Escenarios**: 1, 2, 3
  - **Dependencias**: T-13, T-14

- [x] **T-26**: Crear el controlador `ControladorAccesoExternoHoras`
  - **Archivo**: `src/entradas/controlador_acceso_externo_horas.py`
  - **Escenarios**: 5, 6
  - **Dependencias**: T-15, T-17, T-18

- [x] **T-27**: Crear pruebas automatizadas para los escenarios de CU-04
  - **Archivo**: `tests/test_seguimiento_horas.py`
  - **Escenarios**: 1, 2, 3, 4, 5, 6
  - **Dependencias**: T-01 a T-26

- [x] **T-28**: Validación de la especificación (ejecutar `prompts/5-validar.md`)
  - **Archivo**: `specs/004-seguimiento-horas/validacion.md`
  - **Escenarios**: todos
  - **Dependencias**: T-01 a T-27
