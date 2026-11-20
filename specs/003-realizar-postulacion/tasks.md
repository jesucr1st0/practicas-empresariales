# Tareas: 003-realizar-postulacion (CU-03 Realizar postulación)

Orden: de adentro hacia afuera (dominio → aplicación → infraestructura → entradas).

---

- [x] **T-01**: Crear la entidad `Postulacion` y el enum `EstadoPostulacion`
  - **Archivo**: `src/modulos/postulaciones/dominio/postulacion.py` y `src/modulos/postulaciones/dominio/estado_postulacion.py`
  - **Escenarios**: todos (1, 2, 3, 4, 5, 6)
  - **Dependencias**: ninguna

- [x] **T-02**: Crear el puerto `PostulacionRepository`
  - **Archivo**: `src/modulos/postulaciones/dominio/puertos/postulacion_repository.py`
  - **Escenarios**: 1, 2, 3, 6
  - **Dependencias**: T-01

- [x] **T-03**: Crear el puerto `ConsultaAcademica`
  - **Archivo**: `src/modulos/postulaciones/dominio/puertos/consulta_academica.py`
  - **Escenarios**: 1, 2, 3, 5
  - **Dependencias**: ninguna

- [x] **T-04**: Crear el puerto `EnvioCorreo`
  - **Archivo**: `src/modulos/postulaciones/dominio/puertos/envio_correo.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: ninguna

- [x] **T-05**: Crear el caso de uso `RealizarPostulacion`
  - **Archivo**: `src/modulos/postulaciones/aplicacion/realizar_postulacion.py`
  - **Escenarios**: 1, 2, 3, 6
  - **Dependencias**: T-01, T-02, T-03, T-04

- [x] **T-06**: Crear el caso de uso `VerificarPostulacionPendiente`
  - **Archivo**: `src/modulos/postulaciones/aplicacion/verificar_postulacion_pendiente.py`
  - **Escenarios**: 3, 4, 5
  - **Dependencias**: T-01, T-02, T-03, T-04

- [x] **T-07**: Crear los DTOs `PostulacionDTO` y `ResultadoPostulacionDTO`
  - **Archivo**: `src/modulos/postulaciones/aplicacion/dto.py`
  - **Escenarios**: 1, 2, 3, 6
  - **Dependencias**: T-01

- [x] **T-08**: Crear el adaptador `AdaptadorPostulacionMemoria`
  - **Archivo**: `src/modulos/postulaciones/infraestructura/adaptador_postulacion_memoria.py`
  - **Escenarios**: 1, 2, 3, 6
  - **Dependencias**: T-02

- [x] **T-09**: Crear el adaptador `AdaptadorSIAMemoria`
  - **Archivo**: `src/modulos/postulaciones/infraestructura/adaptador_sia_memoria.py`
  - **Escenarios**: 1, 2, 3, 5
  - **Dependencias**: T-03

- [x] **T-10**: Crear el adaptador `AdaptadorCorreoConsola`
  - **Archivo**: `src/modulos/postulaciones/infraestructura/adaptador_correo_consola.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-04

- [x] **T-11**: Crear el controlador `ControladorPostulacion`
  - **Archivo**: `src/entradas/controlador_postulacion.py`
  - **Escenarios**: 1, 2, 3, 6
  - **Dependencias**: T-05, T-07

- [x] **T-12**: Validación (ejecutar `prompts/5-validar.md`)
  - **Archivo**: `specs/003-realizar-postulacion/validacion.md`
  - **Escenarios**: todos
  - **Dependencias**: T-01 a T-11
