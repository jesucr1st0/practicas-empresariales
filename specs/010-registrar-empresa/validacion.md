# Validación: 010-registrar-empresa (CU-10 Registrar empresa)

## 1. Validación por escenario

| Escenario | Cumple | Evidencia |
|-----------|--------|-----------|
| **1. Registro exitoso de empresa con supervisor inicial (flujo básico)** | Sí | `src/modulos/practicas/aplicacion/registrar_empresa.py` (líneas 14-68), `src/entradas/controlador_empresa.py` (líneas 27-64) y `tests/test_registrar_empresa.py::test_registro_exitoso_empresa_con_supervisor_inicial`. |
| **2. Intento de registro con NIT duplicado** | Sí | `src/modulos/practicas/aplicacion/registrar_empresa.py` (líneas 27-30), `src/entradas/controlador_empresa.py` (líneas 54-63) y `tests/test_registrar_empresa.py::test_intento_registro_con_nit_duplicado`. |
| **3. Intento de registrar empresa sin supervisor inicial** | Sí | `src/modulos/practicas/aplicacion/registrar_empresa.py` (líneas 23-24) valida la multiplicidad `1..*` del modelo de dominio; `tests/test_registrar_empresa.py::test_intento_registro_sin_supervisor_inicial`. |
| **4. Usuario no autorizado intenta registrar una empresa (ADR-005, RN-01)** | Sí | `src/entradas/controlador_empresa.py` (líneas 37-47) restringe la acción a roles autorizados (`Coordinador de prácticas`, `Administrador`) y asienta en bitácora el acceso denegado; `tests/test_registrar_empresa.py::test_usuario_no_autorizado_es_denegado_y_registrado`. |
| **5. Consulta de empresa registrada por NIT** | Sí | `src/modulos/practicas/aplicacion/consultar_empresa.py` (líneas 13-37), `src/entradas/controlador_empresa.py` (líneas 66-98) y `tests/test_registrar_empresa.py::test_consulta_empresa_registrada_por_nit`. |

## 2. Revisión de la regla de dependencia

- **`dominio/` no importa nada de `aplicacion/` ni de `infraestructura/`**:
  - `src/modulos/practicas/dominio/empresa.py` solo importa `dataclasses` y `uuid`.
  - `src/modulos/practicas/dominio/supervisor.py` solo importa `dataclasses` y `uuid`.
  - `src/modulos/practicas/dominio/puertos/empresa_repository.py` solo importa tipos de la biblioteca estándar y entidades de `dominio/`.
- **Los puertos se declaran en `dominio/puertos/`**:
  - `EmpresaRepository` reside en `src/modulos/practicas/dominio/puertos/`.
- **Los adaptadores están en `infraestructura/`**:
  - `AdaptadorEmpresaMemoria` reside en `src/modulos/practicas/infraestructura/`.
- **Los controladores están en `entradas/`**:
  - `ControladorEmpresa` reside en `src/entradas/`.

## 3. Revisión de trazabilidad

- **Tareas de tasks.md**: Todas las tareas desde `T-01` hasta `T-10` están marcadas como completadas `[x]`.
- **Cobertura de escenarios**: Los 5 escenarios de `spec.md` cuentan con implementación directa y pruebas automatizadas dedicadas que pasan al 100 %.
- **Glosario**:
  - Se utilizan los nombres exactos: `Empresa`, `Supervisor`, `RegistroAcceso`, `Coordinador de prácticas`.
