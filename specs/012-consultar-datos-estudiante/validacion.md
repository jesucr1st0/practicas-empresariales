# Validación: 012-consultar-datos-estudiante (CU-12 Consultar datos estudiante)

## 1. Validación por escenario

| Escenario | Cumple | Evidencia |
|-----------|--------|-----------|
| **1. Coordinador consulta datos de estudiante con práctica activa y datos del SIA (flujo básico)** | Sí | `src/modulos/practicas/aplicacion/consultar_datos_estudiante.py` (líneas 18-93), `src/entradas/controlador_consulta_estudiante.py` (líneas 24-63) y `tests/test_consultar_datos_estudiante.py::test_coordinador_consulta_estudiante_con_practica_y_sia`. |
| **2. Tutor consulta los datos de un estudiante asignado a su cargo (regla de alcance, ADR-005)** | Sí | `src/modulos/practicas/aplicacion/consultar_datos_estudiante.py` (líneas 37-46) y `tests/test_consultar_datos_estudiante.py::test_tutor_consulta_estudiante_asignado_por_regla_de_alcance`. |
| **3. Tutor intenta consultar un estudiante no asignado a su cargo (violación de regla de alcance, ADR-005)** | Sí | `src/modulos/practicas/aplicacion/consultar_datos_estudiante.py` (líneas 43-46) y `tests/test_consultar_datos_estudiante.py::test_tutor_intenta_consultar_estudiante_ajeno_violando_regla_de_alcance`. |
| **4. SIA no responde dentro del tiempo límite de 10 segundos (tolerancia a fallos, RT-03, EAC-03, PA-01)** | Sí | `src/modulos/practicas/aplicacion/consultar_datos_estudiante.py` (líneas 50-65) captura `SIATimeoutError`, `SIAError` y retorna datos locales con `disponible_sia=False`; `tests/test_consultar_datos_estudiante.py::test_tolerancia_a_fallos_cuando_sia_presenta_timeout`. |
| **5. Consulta de estudiante sin práctica registrada en el sistema** | Sí | `src/modulos/practicas/aplicacion/consultar_datos_estudiante.py` (líneas 67-78) y `tests/test_consultar_datos_estudiante.py::test_consulta_estudiante_sin_practica_registrada`. |
| **6. Usuario no autorizado intenta consultar datos de estudiante (ADR-005, RN-01)** | Sí | `src/entradas/controlador_consulta_estudiante.py` (líneas 34-44) valida roles autorizados (`Coordinador de prácticas`, `Administrador`, `Tutor`) y asienta en bitácora el acceso denegado; `tests/test_consultar_datos_estudiante.py::test_usuario_no_autorizado_es_denegado_y_registrado`. |

## 2. Revisión de la regla de dependencia

- **`dominio/` no importa nada de `aplicacion/` ni de `infraestructura/`**:
  - `src/modulos/practicas/dominio/datos_academicos_estudiante.py` solo importa `dataclasses`.
  - `src/modulos/practicas/dominio/puertos/consulta_academica_estudiante.py` solo importa tipos de la biblioteca estándar y `DatosAcademicosEstudiante` de `dominio/`.
  - `src/modulos/practicas/dominio/puertos/practica_repository.py` solo importa tipos estándar y entidades de `dominio/`.
- **Los puertos se declaran en `dominio/puertos/`**:
  - `ConsultaAcademicaEstudiante` y `PracticaRepository` residen en `src/modulos/practicas/dominio/puertos/`.
- **Los adaptadores están en `infraestructura/`**:
  - `AdaptadorSIAEstudianteMemoria` y `AdaptadorPracticaMemoria` residen en `src/modulos/practicas/infraestructura/`.
- **Los controladores están en `entradas/`**:
  - `ControladorConsultaEstudiante` reside en `src/entradas/`.

## 3. Revisión de trazabilidad

- **Tareas de tasks.md**: Todas las tareas desde `T-01` hasta `T-10` están marcadas como completadas `[x]`.
- **Cobertura de escenarios**: Los 6 escenarios de `spec.md` cuentan con pruebas automatizadas dedicadas que pasan al 100 %.
- **Glosario**:
  - Se utilizan los términos oficiales: `Estudiante`, `Practica`, `Tutor`, `RegistroAcceso`, `Coordinador de prácticas`.
