# Validación: 003-realizar-postulacion (CU-03 Realizar postulación)

## 1. Validación por escenario

| Escenario | Cumple | Evidencia |
|-----------|:------:|-----------|
| **1. Postulación exitosa** | **Sí** | `RealizarPostulacion.ejecutar()` verifica requisitos en el SIA; cambia estado a `verificada`; envía correo al estudiante y al Coordinador. |
| **2. Estudiante sin requisitos académicos** | **Sí** | Si el SIA retorna incumplimiento de requisitos, la postulación pasa a `rechazada` con el motivo explícito y se notifica al estudiante. |
| **3. SIA no responde en 10 segundos (EAC-03)** | **Sí** | Ante `SIATimeoutError`, la postulación queda en `pendiente de verificación`; se envía aviso al estudiante en < 1 min; 0 postulaciones perdidas (persistida en repo). |
| **4. SIA no responde en 24 horas** | **Sí** | `VerificarPostulacionPendiente` detecta ventana >= 24h de reintentos fallidos y pasa el estado a `revisión manual`, notificando al Coordinador. |
| **5. Respuesta del SIA dentro de los reintentos** | **Sí** | Al restablecerse el SIA, el planificador (`VerificarPostulacionPendiente`) reintenta la verificación, actualiza a `verificada` y notifica al estudiante. |
| **6. Postulación duplicada** | **Sí** | Se lanza `PostulacionDuplicadaError` si el estudiante ya tiene una postulación en curso (`pendiente de verificación` o `verificada`), bloqueando duplicados. |

## 2. Revisión de la regla de dependencia

Verificación de Clean Architecture ejecutada:

- [x] `dominio/` no importa nada de `aplicacion/` ni de `infraestructura/` (0 violaciones encontradas en `src/modulos/postulaciones/dominio/`).
- [x] Los puertos están en `dominio/puertos/` (`PostulacionRepository`, `ConsultaAcademica`, `EnvioCorreo`).
- [x] Los adaptadores están en `infraestructura/` (`AdaptadorPostulacionMemoria`, `AdaptadorSIAMemoria`, `AdaptadorCorreoConsola`).

## 3. Revisión de trazabilidad

- [x] Cada tarea de `tasks.md` está marcada `[x]` (T-01 a T-12 completadas).
- [x] Cada escenario de `spec.md` aparece probado y validado.
- [x] Los nombres del código coinciden con el glosario de `docs/arquitectura.md §10` (`Postulacion`, `EstadoPostulacion`, `ConsultaAcademica`, `EnvioCorreo`).
