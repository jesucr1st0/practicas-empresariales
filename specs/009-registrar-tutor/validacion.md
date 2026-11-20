# Validación: 009-registrar-tutor (CU-09 Registrar tutor)

## 1. Validación por escenario

| Escenario | Cumple | Evidencia |
|-----------|--------|-----------|
| **1. Registro exitoso de un tutor (flujo básico)** | Sí | `src/entradas/controlador_tutor.py` verifica el rol Administrador e invoca `RegistrarTutor` (`src/modulos/tutores_asignacion/aplicacion/registrar_tutor.py`), que guarda el `Tutor` activo en `TutorRepository`. La bitácora guarda quién, qué, cuándo, IP y agente. Prueba: `tests/test_registrar_tutor.py::test_escenario_1_registro_exitoso`. |
| **2. El registro no guarda contraseña (ADR-004)** | Sí | La entidad `Tutor` (`src/modulos/tutores_asignacion/dominio/tutor.py`) solo tiene `documento`, `nombre`, `correo`, `programa` y `activo`. Prueba: `test_escenario_2_sin_contrasena`. |
| **3. Rechazo por documento ya registrado** | Sí | `RegistrarTutor` consulta `obtener_por_documento` y lanza `ValueError` sin sobrescribir; el controlador registra el intento fallido. Prueba: `test_escenario_3_documento_repetido_es_rechazado`. |
| **4. Rol no autorizado (ADR-005)** | Sí | `AutorizadorAccesos.verificar_rol` (spec 007) registra el intento y lanza `PermissionError` antes del caso de uso. Prueba: `test_escenario_4_rol_no_autorizado`. |
| **5. Rechazo por datos obligatorios incompletos** | Sí | `RegistrarTutor` lanza `ValueError` si un dato está vacío; no se guarda nada y se registra el fallo. Prueba: `test_escenario_5_datos_incompletos`. |

## 2. Revisión de la regla de dependencia

- `tutores_asignacion/dominio/` no importa de `aplicacion/` ni de `infraestructura/` (búsqueda de imports en `src/modulos/*/dominio`: 0 coincidencias).
- El puerto `TutorRepository` está en `tutores_asignacion/dominio/puertos/`.
- El adaptador `AdaptadorTutorMemoria` está en `tutores_asignacion/infraestructura/`.
- La autorización y la bitácora se aplican en `src/entradas/controlador_tutor.py` (ADR-005); el Módulo Tutores y asignación no depende del Módulo Identidad y accesos.

## 3. Revisión de trazabilidad

- Tareas T-01 a T-08 de `tasks.md` marcadas `[x]`.
- Los 5 escenarios de `spec.md` aparecen en al menos una tarea y tienen una prueba en `tests/test_registrar_tutor.py`.
- Nombres alineados con el glosario: `Tutor`, `TutorRepository` (patrón `<Entidad>Repository`), `RegistroAcceso`.
- Suite completa del proyecto: 38 pruebas aprobadas.

## 4. Pendientes declarados

- Atributos maestros del tutor: `[NECESITA ACLARACIÓN]` en spec.md. Se reutiliza la entidad `Tutor` existente.
- Conectar `TutorRepository` con `AsignacionRepository.listar_tutores_activos` (CU-01) queda como pendiente de la composición (plan.md §5).
