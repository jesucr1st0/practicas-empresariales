# Tareas: 007-exportar-acta (CU-07 Exportar acta final)

Orden: de adentro hacia afuera (dominio → aplicación → entradas → pruebas → validación).

Escenarios de spec.md: 1 Coordinador exporta · 2 Estudiante titular · 3 Estudiante ajeno · 4 Rol no autorizado · 5 Acta corregida · 6 Sin acta vigente · 7 Archivo alterado.

---

- [x] **T-01**: Crear el enum `Rol`
  - **Archivo**: `src/modulos/identidad_accesos/dominio/rol.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: ninguna

- [x] **T-02**: Crear el valor `UsuarioAutenticado`
  - **Archivo**: `src/modulos/identidad_accesos/dominio/usuario_autenticado.py`
  - **Escenarios**: 1, 2, 3, 4
  - **Dependencias**: T-01

- [x] **T-03**: Crear el servicio `AutorizadorAccesos` (verificación de rol y registro en bitácora)
  - **Archivo**: `src/modulos/identidad_accesos/aplicacion/autorizador_accesos.py`
  - **Escenarios**: 1, 2, 3, 4, 6, 7
  - **Dependencias**: T-02

- [x] **T-04**: Agregar la regla de alcance del estudiante a `ExportarActaFinal`
  - **Archivo**: `src/modulos/actas/aplicacion/exportar_acta_final.py`
  - **Escenarios**: 1, 2, 3, 5, 6, 7
  - **Dependencias**: ninguna (usa puertos de spec 006)

- [x] **T-05**: Crear el controlador `ControladorExportarActa`
  - **Archivo**: `src/entradas/controlador_exportar_acta.py`
  - **Escenarios**: 1, 2, 3, 4, 5, 6, 7
  - **Dependencias**: T-03, T-04

- [x] **T-06**: Crear pruebas automatizadas para CU-07
  - **Archivo**: `tests/test_exportar_acta.py`
  - **Escenarios**: 1, 2, 3, 4, 5, 6, 7
  - **Dependencias**: T-01 a T-05

- [x] **T-07**: Validación de la especificación (ejecutar `prompts/5-validar.md`)
  - **Archivo**: `specs/007-exportar-acta/validacion.md`
  - **Escenarios**: todos
  - **Dependencias**: T-01 a T-06
