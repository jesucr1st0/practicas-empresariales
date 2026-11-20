# Tareas: 006-generar-acta (CU-06 Generar acta final)

Orden: de adentro hacia afuera (dominio → aplicación → infraestructura → entradas → pruebas → validación).

---

- [x] **T-01**: Crear el enum `EstadoActa`
  - **Archivo**: `src/modulos/actas/dominio/estado_acta.py`
  - **Escenarios**: 1, 4, 5
  - **Dependencias**: ninguna

- [x] **T-02**: Crear la entidad `ActaFinal`
  - **Archivo**: `src/modulos/actas/dominio/acta_final.py`
  - **Escenarios**: 1, 4, 5
  - **Dependencias**: T-01

- [x] **T-03**: Crear el puerto `ActaFinalRepository`
  - **Archivo**: `src/modulos/actas/dominio/puertos/acta_final_repository.py`
  - **Escenarios**: 1, 4, 5
  - **Dependencias**: T-02

- [x] **T-04**: Crear el puerto `AlmacenArchivos`
  - **Archivo**: `src/modulos/actas/dominio/puertos/almacen_archivos.py`
  - **Escenarios**: 1, 4, 5
  - **Dependencias**: ninguna

- [x] **T-05**: Crear el puerto `ConsultaPracticaActa`
  - **Archivo**: `src/modulos/actas/dominio/puertos/consulta_practica_acta.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: ninguna

- [x] **T-06**: Crear el puerto `ConsultaHorasActa`
  - **Archivo**: `src/modulos/actas/dominio/puertos/consulta_horas_acta.py`
  - **Escenarios**: 1, 2, 4
  - **Dependencias**: ninguna

- [x] **T-07**: Crear el puerto `ConsultaEvaluacionActa`
  - **Archivo**: `src/modulos/actas/dominio/puertos/consulta_evaluacion_acta.py`
  - **Escenarios**: 1, 3, 4
  - **Dependencias**: ninguna

- [x] **T-08**: Crear el puerto `ConsultaReglasActa`
  - **Archivo**: `src/modulos/actas/dominio/puertos/consulta_reglas_acta.py`
  - **Escenarios**: 1, 2, 4
  - **Dependencias**: ninguna

- [x] **T-09**: Crear el puerto `GeneradorPlantillaActa`
  - **Archivo**: `src/modulos/actas/dominio/puertos/generador_plantilla_acta.py`
  - **Escenarios**: 1, 4
  - **Dependencias**: ninguna

- [x] **T-10**: Crear los DTOs del módulo Actas
  - **Archivo**: `src/modulos/actas/aplicacion/dto.py`
  - **Escenarios**: 1, 4, 5
  - **Dependencias**: T-01, T-02

- [x] **T-11**: Crear el caso de uso `GenerarActaFinal`
  - **Archivo**: `src/modulos/actas/aplicacion/generar_acta_final.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-02, T-03, T-04, T-05, T-06, T-07, T-08, T-09, T-10

- [x] **T-12**: Crear el caso de uso `ExportarActaFinal`
  - **Archivo**: `src/modulos/actas/aplicacion/exportar_acta_final.py`
  - **Escenarios**: 5
  - **Dependencias**: T-02, T-03, T-04, T-10

- [x] **T-13**: Crear el adaptador `AdaptadorActaFinalMemoria`
  - **Archivo**: `src/modulos/actas/infraestructura/adaptador_acta_final_memoria.py`
  - **Escenarios**: 1, 4, 5
  - **Dependencias**: T-03

- [x] **T-14**: Crear el adaptador `AdaptadorAlmacenArchivosMemoria`
  - **Archivo**: `src/modulos/actas/infraestructura/adaptador_almacen_archivos_memoria.py`
  - **Escenarios**: 1, 4, 5
  - **Dependencias**: T-04

- [x] **T-15**: Crear el adaptador `AdaptadorConsultaPracticaMemoria`
  - **Archivo**: `src/modulos/actas/infraestructura/adaptador_consulta_practica_memoria.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-05

- [x] **T-16**: Crear el adaptador `AdaptadorConsultaHorasMemoria`
  - **Archivo**: `src/modulos/actas/infraestructura/adaptador_consulta_horas_memoria.py`
  - **Escenarios**: 1, 2, 4
  - **Dependencias**: T-06

- [x] **T-17**: Crear el adaptador `AdaptadorConsultaEvaluacionMemoria`
  - **Archivo**: `src/modulos/actas/infraestructura/adaptador_consulta_evaluacion_memoria.py`
  - **Escenarios**: 1, 3, 4
  - **Dependencias**: T-07

- [x] **T-18**: Crear el adaptador `AdaptadorConsultaReglasMemoria`
  - **Archivo**: `src/modulos/actas/infraestructura/adaptador_consulta_reglas_memoria.py`
  - **Escenarios**: 1, 2, 4
  - **Dependencias**: T-08

- [x] **T-19**: Crear el adaptador `AdaptadorGeneradorPlantillaOficial`
  - **Archivo**: `src/modulos/actas/infraestructura/adaptador_generador_plantilla_oficial.py`
  - **Escenarios**: 1, 4
  - **Dependencias**: T-09

- [x] **T-20**: Crear el controlador `ControladorActas`
  - **Archivo**: `src/entradas/controlador_actas.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-11, T-12

- [x] **T-21**: Crear pruebas automatizadas para CU-06 y CU-07
  - **Archivo**: `tests/test_generar_acta.py`
  - **Escenarios**: 1, 2, 3, 4, 5
  - **Dependencias**: T-01 a T-20

- [x] **T-22**: Validación de la especificación (ejecutar `prompts/5-validar.md`)
  - **Archivo**: `specs/006-generar-acta/validacion.md`
  - **Escenarios**: todos
  - **Dependencias**: T-01 a T-21
