# Validación: 004-seguimiento-horas (CU-04 Realizar seguimiento en horas)

## 1. Validación por escenario

| Escenario | Cumple | Evidencia |
|-----------|--------|-----------|
| **1. Registro de horas por el estudiante (flujo básico)** | Sí | `src/modulos/horas/aplicacion/registrar_horas.py` crea `RegistroHoras` con estado `PENDIENTE` y persiste vía `RegistroHorasRepository`. Verificado en `tests/test_seguimiento_horas.py::SeguimientoHorasTests.test_escenario_1_registro_horas_estudiante_exitoso`. |
| **2. Consulta y seguimiento de horas por el tutor asignado (ADR-005)** | Sí | `src/modulos/horas/aplicacion/consultar_horas_tutor.py` valida asignación mediante `ConsultaAsignacionTutor` y retorna resumen acumulado y registros detallados. Verificado en `tests/test_seguimiento_horas.py::SeguimientoHorasTests.test_escenario_2_consulta_horas_tutor_asignado`. |
| **3. Tutor intenta consultar horas de una práctica no asignada (ADR-005)** | Sí | `src/modulos/horas/aplicacion/consultar_horas_tutor.py` deniega con `PermissionError` y registra acceso fallido en `BitacoraAccesoRepository`. Verificado en `tests/test_seguimiento_horas.py::SeguimientoHorasTests.test_escenario_3_tutor_no_asignado_denegado`. |
| **4. Emisión y envío de enlace de validación al supervisor (ADR-006, ADR-013)** | Sí | `src/modulos/horas/aplicacion/solicitar_validacion_supervisor.py` y `src/modulos/identidad_accesos/aplicacion/gestor_enlaces_acceso.py` generan token criptográfico (≥128 bits), guardan hash SHA-256 con vencimiento a 30 días y envían correo mediante `ServicioNotificacionHoras`. Verificado en `tests/test_seguimiento_horas.py::SeguimientoHorasTests.test_escenario_4_emision_y_envio_enlace_supervisor`. |
| **5. Validación de horas por el supervisor sin cuenta ni contraseña (EAC-02, RN-04, ADR-006)** | Sí | `src/entradas/controlador_acceso_externo_horas.py` y `src/modulos/horas/aplicacion/validar_horas_supervisor.py` permiten consultar y validar horas sin contraseña; el 100 % de accesos se registran en `BitacoraAccesoRepository`. Verificado en `tests/test_seguimiento_horas.py::SeguimientoHorasTests.test_escenario_5_validacion_supervisor_sin_cuenta`. |
| **6. Acceso con enlace vencido, usado o revocado (EAC-02, ADR-006)** | Sí | `src/modulos/identidad_accesos/aplicacion/gestor_enlaces_acceso.py` verifica vigencia, registra el intento denegado en bitácora y lanza error informativo ("enlace no disponible; pida al coordinador que lo reemita"). Verificado en `tests/test_seguimiento_horas.py::SeguimientoHorasTests.test_escenario_6_enlace_vencido_usado_o_revocado_denegado`. |

## 2. Revisión de la regla de dependencia

- `dominio/` no importa nada de `aplicacion/` ni de `infraestructura/` (0 violaciones verificadas mediante script estático).
- Los puertos se declaran en `dominio/puertos/` (`registro_horas_repository.py`, `consulta_asignacion_tutor.py`, `servicio_enlace_horas.py`, `servicio_notificacion_horas.py`, `enlace_acceso_repository.py`, `bitacora_acceso_repository.py`).
- Los adaptadores implementan los puertos en `infraestructura/` (`adaptador_registro_horas_memoria.py`, `adaptador_enlace_acceso_memoria.py`, `adaptador_bitacora_memoria.py`, `adaptador_consulta_asignacion_memoria.py`, `adaptador_servicio_enlace_memoria.py`, `adaptador_servicio_notificacion_memoria.py`).
- Los adaptadores de entrada residen en `src/entradas/` (`controlador_horas_interno.py`, `controlador_acceso_externo_horas.py`).

## 3. Revisión de trazabilidad

- Cada tarea de `tasks.md` (T-01 a T-28) se encuentra completada y marcada `[x]`.
- Cada escenario de `spec.md` tiene cobertura en al menos una tarea y una prueba automatizada unitaria/de integración en `tests/test_seguimiento_horas.py`.
- Los nombres del código respetan rigurosamente el glosario de arquitectura: `RegistroHoras`, `EstadoValidacionHoras`, `EnlaceAcceso`, `EstadoEnlace`, `RegistroAcceso`, `ConsultaAsignacionTutor`, `BitacoraAccesoRepository`, etc.
- 11 pruebas automatizadas del proyecto ejecutadas y aprobadas en 0.004s.
