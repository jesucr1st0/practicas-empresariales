# Validación: 008-registrar-estudiante (CU-08 Registrar estudiante)

## 1. Validación por escenario

| Escenario | Cumple | Evidencia |
|-----------|--------|-----------|
| **1. Registro exitoso de un estudiante (flujo básico)** | Sí | `src/entradas/controlador_estudiante.py` verifica el rol Administrador e invoca `RegistrarEstudiante` (`src/modulos/practicas/aplicacion/registrar_estudiante.py`), que guarda el `Estudiante` en `EstudianteRepository`. La bitácora guarda quién, qué, cuándo, IP y agente. Prueba: `tests/test_registrar_estudiante.py::test_escenario_1_registro_exitoso`. |
| **2. El registro no guarda contraseña ni datos académicos (ADR-004, ADR-007, RT-03)** | Sí | `src/modulos/practicas/dominio/estudiante.py` solo tiene `documento`, `nombre`, `programa` y `correo`. Prueba: `test_escenario_2_sin_contrasena_ni_datos_academicos`. |
| **3. Rechazo por documento ya registrado** | Sí | `RegistrarEstudiante` consulta `obtener_por_documento` y lanza `ValueError` sin sobrescribir; el controlador registra el intento fallido. Prueba: `test_escenario_3_documento_repetido_es_rechazado`. |
| **4. Rol no autorizado (ADR-005)** | Sí | `AutorizadorAccesos.verificar_rol` (spec 007) registra el intento y lanza `PermissionError` antes del caso de uso. Prueba: `test_escenario_4_rol_no_autorizado`. |
| **5. Rechazo por datos obligatorios incompletos** | Sí | `Estudiante.__post_init__` lanza `ValueError` si un dato está vacío; no se guarda nada y se registra el fallo. Prueba: `test_escenario_5_datos_incompletos`. |

## 2. Revisión de la regla de dependencia

- `practicas/dominio/` no importa de `aplicacion/` ni de `infraestructura/` (búsqueda de imports en `src/modulos/*/dominio`: 0 coincidencias).
- El puerto `EstudianteRepository` está en `practicas/dominio/puertos/`.
- El adaptador `AdaptadorEstudianteMemoria` está en `practicas/infraestructura/`.
- La autorización y la bitácora se aplican en `src/entradas/controlador_estudiante.py` (ADR-005); el Módulo Prácticas no depende del Módulo Identidad y accesos.

## 3. Revisión de trazabilidad

- Tareas T-01 a T-09 de `tasks.md` marcadas `[x]`.
- Los 5 escenarios de `spec.md` aparecen en al menos una tarea y tienen una prueba en `tests/test_registrar_estudiante.py`.
- Nombres alineados con el glosario: `Estudiante`, `EstudianteRepository` (patrón `<Entidad>Repository`), `RegistroAcceso`.
- Suite completa del proyecto: 33 pruebas aprobadas.

## 4. Pendientes declarados en spec.md

- Ubicación de CU-08 en el Módulo Prácticas: `[NECESITA ACLARACIÓN]`, porque la vista de desarrollo no lo asigna a ningún módulo.
- Atributos maestros del estudiante: `[NECESITA ACLARACIÓN]`. Se usaron los de la vista lógica más programa y correo.
