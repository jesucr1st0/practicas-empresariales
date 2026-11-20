# Validación: 011-consultar-datos-tutor (CU-11 Consultar datos tutor)

## 1. Validación por escenario

| Escenario | Cumple | Evidencia |
|-----------|--------|-----------|
| **1. Consulta exitosa de datos de tutor por el Coordinador de prácticas (flujo básico)** | Sí | `src/modulos/tutores_asignacion/aplicacion/consultar_datos_tutor.py` (líneas 21-87), `src/entradas/controlador_consulta_tutor.py` (líneas 27-66) y `tests/test_consultar_datos_tutor.py::test_consulta_exitosa_datos_tutor_con_sia_y_bitacora`. |
| **2. Consulta de tutor inexistente** | Sí | `src/modulos/tutores_asignacion/aplicacion/consultar_datos_tutor.py` (líneas 26-28), `src/entradas/controlador_consulta_tutor.py` (líneas 54-65) y `tests/test_consultar_datos_tutor.py::test_consulta_tutor_inexistente_registra_en_bitacora`. |
| **3. Usuario no autorizado intenta consultar datos de tutor (ADR-005, RN-01)** | Sí | `src/entradas/controlador_consulta_tutor.py` (líneas 37-47) valida rol `Coordinador de prácticas` y registra en bitácora el acceso denegado; `tests/test_consultar_datos_tutor.py::test_usuario_no_autorizado_es_denegado_y_registrado_en_bitacora`. |
| **4. SIA no responde o se encuentra caído (tolerancia a fallos, RT-03, EAC-03, PA-01)** | Sí | `src/modulos/tutores_asignacion/aplicacion/consultar_datos_tutor.py` (líneas 41-58) captura `SIATimeoutError`, `SIAError` y retorna datos locales con estado no disponible; `tests/test_consultar_datos_tutor.py::test_tolerancia_a_fallos_cuando_sia_no_responde_o_timeout`. |
| **5. Listar tutores por programa para el tablero de estado (CU-11, ADR-012)** | Sí | `src/modulos/tutores_asignacion/aplicacion/listar_tutores_programa.py` (líneas 10-53), `src/entradas/controlador_consulta_tutor.py` (líneas 68-96) y `tests/test_consultar_datos_tutor.py::test_listar_tutores_por_programa_para_tablero_de_estado`. |

## 2. Revisión de la regla de dependencia

- **`dominio/` no importa nada de `aplicacion/` ni de `infraestructura/`**:
  - `src/modulos/tutores_asignacion/dominio/datos_academicos_tutor.py` solo importa `dataclasses`.
  - `src/modulos/tutores_asignacion/dominio/puertos/consulta_academica_tutor.py` solo importa tipos de la biblioteca estándar y `DatosAcademicosTutor` de `dominio/`.
  - `src/modulos/tutores_asignacion/dominio/puertos/asignacion_repository.py` solo importa tipos estándar y entidades de `dominio/`.
  - `src/modulos/tutores_asignacion/dominio/puertos/consulta_regla_tutor.py` solo importa `Protocol`.
- **Los puertos se declaran en `dominio/puertos/`**:
  - `ConsultaAcademicaTutor`, `AsignacionRepository` y `ConsultaReglaTutor` residen en `src/modulos/tutores_asignacion/dominio/puertos/`.
- **Los adaptadores están en `infraestructura/`**:
  - `AdaptadorSIATutorMemoria`, `AdaptadorAsignacionMemoria` y `AdaptadorServicioReglasMemoria` residen en `src/modulos/tutores_asignacion/infraestructura/`.
- **Los controladores están en `entradas/`**:
  - `ControladorConsultaTutor` reside en `src/entradas/`.

## 3. Revisión de trazabilidad

- **Tareas de tasks.md**: Todas las tareas desde `T-01` hasta `T-11` están marcadas como completadas `[x]`.
- **Cobertura de escenarios**: Los 5 escenarios de `spec.md` tienen implementación de código y pruebas automatizadas dedicadas que pasan al 100 %.
- **Glosario**:
  - Se utilizan los términos oficiales: `Tutor`, `AsignacionTutor`, `RegistroAcceso`, `ReglaPrograma`, `ConsultaAcademicaTutor`.
  - Los roles respetan el catálogo: `Coordinador de prácticas`, `Estudiante`.
