# Plan: 003-realizar-postulacion (CU-03 Realizar postulación)

## 1. Decisiones que aplican

| ADR | Decisión | Impacto en esta funcionalidad |
|-----|----------|-------------------------------|
| [ADR-007](../../docs/adr/ADR-007-integracion-sia-adaptador-aislado.md) | Adaptador aislado hacia el SIA | La verificación de datos académicos se hace a través del puerto `ConsultaAcademica`; solo el `AdaptadorSIA` conoce al SIA |
| [ADR-008](../../docs/adr/ADR-008-verificacion-asincrona-con-reintentos.md) | Verificación asíncrona con reintentos | Si el SIA no responde en 10 s, la postulación queda «pendiente de verificación»; reintentos cada 15 min durante 24 h; cola en la base de datos |
| [ADR-013](../../docs/adr/ADR-013-notificaciones-por-correo-institucional.md) | Notificaciones por correo institucional | Se envía correo al estudiante (confirmación, rechazo, pendiente) y al coordinador (revisión manual) |
| [ADR-001](../../docs/adr/ADR-001-monolito-modular.md) | Monolito modular | La funcionalidad vive en el Módulo Postulaciones; respeta los límites entre módulos |

## 2. Componentes por capa

Los componentes vienen de la [vista de desarrollo](../../docs/vistas/03-desarrollo.md).

### dominio/ (Módulo Postulaciones)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/postulaciones/dominio/postulacion.py` | Entidad `Postulacion`: fecha, estado, documento del estudiante, programa, fecha de último intento, número de reintentos |
| `src/modulos/postulaciones/dominio/estado_postulacion.py` | Enum `EstadoPostulacion`: `PENDIENTE_VERIFICACION`, `VERIFICADA`, `RECHAZADA`, `REVISION_MANUAL` |
| `src/modulos/postulaciones/dominio/puertos/postulacion_repository.py` | Puerto `PostulacionRepository`: guardar, buscar por ID, buscar activa por documento |
| `src/modulos/postulaciones/dominio/puertos/consulta_academica.py` | Puerto `ConsultaAcademica`: verificar requisitos de un estudiante en el SIA |
| `src/modulos/postulaciones/dominio/puertos/envio_correo.py` | Puerto `EnvioCorreo`: enviar notificación por correo institucional |

### aplicacion/ (Módulo Postulaciones)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/postulaciones/aplicacion/realizar_postulacion.py` | Caso de uso `RealizarPostulacion`: crea la postulación, intenta verificar con el SIA, maneja el timeout |
| `src/modulos/postulaciones/aplicacion/verificar_postulacion_pendiente.py` | Caso de uso `VerificarPostulacionPendiente`: reintenta la verificación de postulaciones pendientes; si se agotan los 24 h, pasa a revisión manual |
| `src/modulos/postulaciones/aplicacion/dto.py` | DTOs de entrada y salida: `PostulacionDTO`, `ResultadoPostulacionDTO` |

### infraestructura/ (adaptadores)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/postulaciones/infraestructura/adaptador_postulacion_memoria.py` | `AdaptadorPostulacionMemoria`: implementa `PostulacionRepository` con un diccionario en memoria (esta etapa) |
| `src/modulos/postulaciones/infraestructura/adaptador_sia_memoria.py` | `AdaptadorSIAMemoria`: implementa `ConsultaAcademica` con datos simulados; permite simular timeout |
| `src/modulos/postulaciones/infraestructura/adaptador_correo_consola.py` | `AdaptadorCorreoConsola`: implementa `EnvioCorreo` imprimiendo en consola (esta etapa) |

### entradas/

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/entradas/controlador_postulacion.py` | Punto de entrada para la postulación; recibe la solicitud, invoca el caso de uso y devuelve el resultado |

## 3. Flujo

### Camino principal (postulación exitosa)

1. El estudiante envía la solicitud a través de la **Interfaz web interna** → `ControladorPostulacion`.
2. El controlador crea un `PostulacionDTO` y llama a `RealizarPostulacion.ejecutar(dto)`.
3. `RealizarPostulacion` verifica que no haya una postulación activa (`PostulacionRepository.buscar_activa_por_documento`).
4. Crea una `Postulacion` en estado `PENDIENTE_VERIFICACION` y la guarda (`PostulacionRepository.guardar`).
5. Llama a `ConsultaAcademica.verificar_requisitos(documento, programa)` con timeout de 10 s.
6. Si el SIA responde positivamente → cambia el estado a `VERIFICADA` y guarda.
7. Envía correo al estudiante confirmando → `EnvioCorreo.enviar(...)`.
8. Notifica al Coordinador.

### Camino alterno: estudiante sin requisitos

- En el paso 6, el SIA responde que el estudiante no cumple → estado `RECHAZADA` → correo con el motivo.

### Camino alterno: SIA no responde (EAC-03)

- En el paso 5, el SIA no responde en 10 s → la postulación permanece en `PENDIENTE_VERIFICACION`.
- Se programa un reintento en el Planificador de tareas.
- Se envía correo al estudiante indicando que la verificación está pendiente (en ≤ 1 min).

### Camino alterno: 24 h sin respuesta del SIA

- Después de 24 h de reintentos fallidos → `VerificarPostulacionPendiente` cambia el estado a `REVISION_MANUAL`.
- Envía correo al Coordinador para revisión manual.

### Camino alterno: postulación duplicada

- En el paso 3, se encuentra una postulación activa → se rechaza la solicitud sin crear una nueva.

## 4. Modelo de datos

```
Postulacion
├── id: UUID
├── documento_estudiante: str
├── programa: str
├── fecha_creacion: datetime
├── estado: EstadoPostulacion
├── fecha_ultimo_intento: datetime | None
├── numero_reintentos: int
└── motivo_rechazo: str | None
```

## 5. Fuera de alcance

- **Interfaz gráfica**: solo se implementa el punto de entrada (controlador); no hay pantallas ni HTML.
- **Persistencia en base de datos real**: se usan adaptadores en memoria (ADR-002, candidato PostgreSQL; pendiente de confirmar RT-04).
- **Integración real con el SIA**: se usa un adaptador simulado; el protocolo y los endpoints están por confirmar.
- **Integración real con el correo**: se usa un adaptador de consola.
- **Autenticación SSO**: se asume que el estudiante ya está autenticado.
- **Planificador de tareas real**: el mecanismo de reintentos se modela en el caso de uso `VerificarPostulacionPendiente`, pero la ejecución periódica queda fuera de alcance en esta etapa.
