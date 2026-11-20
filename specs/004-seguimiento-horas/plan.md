# Plan: 004-seguimiento-horas (CU-04 Realizar seguimiento en horas)

## 1. Decisiones que aplican

| ADR | Decisión | Impacto en esta funcionalidad |
|-----|----------|-------------------------------|
| [ADR-001](../../docs/adr/ADR-001-monolito-modular.md) | Monolito modular con Clean Architecture | Módulo `horas` gestiona el registro y validación de horas; se comunica con `identidad_accesos` y `notificaciones` mediante puertos sin acoplamiento circular. |
| [ADR-002](../../docs/adr/ADR-002-persistencia-relacional.md) | Persistencia relacional (PostgreSQL en prod, memoria en pruebas) | Adaptadores en memoria para repositorios de `RegistroHoras`, `EnlaceAcceso` y `RegistroAcceso` (bitácora). |
| [ADR-005](../../docs/adr/ADR-005-autorizacion-por-roles-y-bitacora.md) | Autorización por roles y bitácora de accesos | El tutor solo puede consultar prácticas asignadas a él (regla de alcance); el 100 % de los accesos a datos personales y por enlace se registran en la bitácora de solo inserción. |
| [ADR-006](../../docs/adr/ADR-006-acceso-externo-enlace-un-solo-uso.md) | Enlace de un solo uso con vencimiento para supervisores | Token aleatorio opaco (≥ 128 bits), almacenamiento exclusivo de su hash criptográfico, vigencia de 30 días, cero contraseñas para supervisores (RN-04, EAC-02). |
| [ADR-013](../../docs/adr/ADR-013-notificaciones-por-correo-institucional.md) | Notificaciones por correo institucional | Envío del enlace de validación al correo del supervisor y registro del envío. |

## 2. Componentes por capa

Basado en la [vista de desarrollo](../../docs/vistas/03-desarrollo.md):

### dominio/

#### Módulo Horas (`src/modulos/horas/dominio/`)
| Archivo | Responsabilidad |
|---------|-----------------|
| `registro_horas.py` | Entidad `RegistroHoras`: `id`, `practica_id`, `estudiante_documento`, `fecha`, `cantidad_horas`, `evidencia`, `estado_validacion`, `fecha_registro`. |
| `estado_validacion_horas.py` | Enum `EstadoValidacionHoras`: `PENDIENTE`, `VALIDADO_SUPERVISOR`, `RECHAZADO`. |
| `puertos/registro_horas_repository.py` | Puerto `RegistroHorasRepository`: guardar, buscar por id, listar por práctica. |
| `puertos/consulta_asignacion_tutor.py` | Puerto `ConsultaAsignacionTutor`: verificar si un tutor tiene asignada una práctica específica (alcance de tutor). |
| `puertos/servicio_enlace_horas.py` | Puerto `ServicioEnlaceHoras`: solicitar la generación de enlace de validación a Identidad y accesos. |
| `puertos/servicio_notificacion_horas.py` | Puerto `ServicioNotificacionHoras`: notificar al supervisor el enlace generado. |

#### Módulo Identidad y Accesos (`src/modulos/identidad_accesos/dominio/`)
| Archivo | Responsabilidad |
|---------|-----------------|
| `enlace_acceso.py` | Entidad `EnlaceAcceso`: `id`, `token_hash`, `practica_id`, `email_destinatario`, `fecha_emision`, `fecha_vencimiento`, `estado`, `acciones_permitidas`. |
| `estado_enlace.py` | Enum `EstadoEnlace`: `VIGENTE`, `USADO`, `VENCIDO`, `REVOCADO`. |
| `registro_acceso.py` | Entidad `RegistroAcceso`: `id`, `sujeto`, `accion`, `fecha`, `ip`, `agente_usuario`, `exitoso`, `detalle`. |
| `puertos/enlace_acceso_repository.py` | Puerto `EnlaceAccesoRepository`: guardar, buscar por hash, actualizar. |
| `puertos/bitacora_acceso_repository.py` | Puerto `BitacoraAccesoRepository`: registrar acceso (solo inserción), listar accesos. |

### aplicacion/

#### Módulo Horas (`src/modulos/horas/aplicacion/`)
| Archivo | Responsabilidad |
|---------|-----------------|
| `registrar_horas.py` | Caso de uso `RegistrarHoras`: registra horas realizadas por el estudiante en estado `PENDIENTE`. |
| `consultar_horas_tutor.py` | Caso de uso `ConsultarHorasTutor`: valida alcance del tutor vía `ConsultaAsignacionTutor` y retorna horas acumuladas y detalle. |
| `solicitar_validacion_supervisor.py` | Caso de uso `SolicitarValidacionSupervisor`: emite enlace de validación vía `ServicioEnlaceHoras` y envía notificación vía `ServicioNotificacionHoras`. |
| `consultar_horas_supervisor.py` | Caso de uso `ConsultarHorasSupervisor`: retorna horas pendientes de la práctica asociada al enlace validado. |
| `validar_horas_supervisor.py` | Caso de uso `ValidarHorasSupervisor`: aprueba horas pendientes de la práctica. |
| `dto.py` | DTOs de entrada y salida: `RegistrarHorasDTO`, `RegistroHorasDTO`, `ResumenHorasTutorDTO`, `ValidarHorasDTO`. |

#### Módulo Identidad y Accesos (`src/modulos/identidad_accesos/aplicacion/`)
| Archivo | Responsabilidad |
|---------|-----------------|
| `gestor_enlaces_acceso.py` | Servicio / Caso de uso para emitir tokens seguros (≥128 bits), calcular SHA-256, fijar vigencia de 30 días, y validar vigencia de token registrando en bitácora. |

### infraestructura/

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/horas/infraestructura/adaptador_registro_horas_memoria.py` | Implementación en memoria de `RegistroHorasRepository`. |
| `src/modulos/horas/infraestructura/adaptador_servicio_enlace_memoria.py` | Implementación de `ServicioEnlaceHoras` conectado al gestor de enlaces. |
| `src/modulos/horas/infraestructura/adaptador_servicio_notificacion_memoria.py` | Implementación de `ServicioNotificacionHoras` en memoria / simulación. |
| `src/modulos/horas/infraestructura/adaptador_consulta_asignacion_memoria.py` | Implementación de `ConsultaAsignacionTutor` en memoria. |
| `src/modulos/identidad_accesos/infraestructura/adaptador_enlace_acceso_memoria.py` | Implementación en memoria de `EnlaceAccesoRepository`. |
| `src/modulos/identidad_accesos/infraestructura/adaptador_bitacora_memoria.py` | Implementación en memoria de `BitacoraAccesoRepository`. |

### entradas/

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/entradas/controlador_horas_interno.py` | Interfaz web interna: controladores para registro de horas (estudiante) y seguimiento (tutor). |
| `src/entradas/controlador_acceso_externo_horas.py` | Formulario de acceso externo: controlador liviano para consulta y validación por enlace del supervisor sin contraseña. |

## 3. Flujo

### 1. Registro de horas (Estudiante con SSO)
1. El estudiante envía cantidad de horas, fecha y evidencia a `ControladorHorasInterno`.
2. `RegistrarHoras` crea la entidad `RegistroHoras(estado=PENDIENTE)` y la persiste en `RegistroHorasRepository`.
3. Retorna confirmación al estudiante.

### 2. Consulta de horas por el tutor (Tutor con SSO)
1. El tutor solicita seguimiento de horas de una práctica a `ControladorHorasInterno`.
2. `ConsultarHorasTutor` verifica con `ConsultaAsignacionTutor` si el tutor está asignado a la práctica.
   - Si no está asignado: deniega la consulta y registra en bitácora intento no autorizado (ADR-005).
   - Si está asignado: obtiene registros de `RegistroHorasRepository` y retorna resumen y lista detallada.

### 3. Emisión de enlace al supervisor
1. `SolicitarValidacionSupervisor` solicita al `ServicioEnlaceHoras` generar enlace para la práctica con 30 días de vigencia.
2. `GestorEnlacesAcceso` genera un token aleatorio seguro (≥128 bits), guarda el hash con estado `VIGENTE` y fecha de expiración en `EnlaceAccesoRepository`.
3. `SolicitarValidacionSupervisor` envía el correo al supervisor con el enlace a través de `ServicioNotificacionHoras`.

### 4. Acceso y validación del supervisor (Acceso externo sin cuenta)
1. El supervisor abre el enlace en `ControladorAccesoExternoHoras` con su IP y agente de usuario.
2. El gestor valida el token contra su hash en `EnlaceAccesoRepository` y registra el acceso en `BitacoraAccesoRepository`:
   - Si el enlace está vencido (> 30 días), usado o revocado: deniega acceso con mensaje "enlace no disponible; pida al coordinador que lo reemita".
   - Si el enlace está vigente: autoriza acceso exclusivamente para la práctica del enlace.
3. El supervisor consulta horas pendientes de la práctica.
4. El supervisor confirma la validación de horas.
5. `ValidarHorasSupervisor` cambia el estado de los registros pendientes a `VALIDADO_SUPERVISOR`.

## 4. Modelo de datos

```
RegistroHoras
├── id: UUID
├── practica_id: UUID
├── estudiante_documento: str
├── fecha: date
├── cantidad_horas: int
├── evidencia: str
├── estado_validacion: EstadoValidacionHoras (PENDIENTE | VALIDADO_SUPERVISOR | RECHAZADO)
└── fecha_registro: datetime

EnlaceAcceso
├── id: UUID
├── token_hash: str (SHA-256)
├── practica_id: UUID
├── email_destinatario: str
├── fecha_emision: datetime
├── fecha_vencimiento: datetime
├── estado: EstadoEnlace (VIGENTE | USADO | VENCIDO | REVOCADO)
└── acciones_permitidas: list[str]

RegistroAcceso
├── id: UUID
├── sujeto: str (identificador de usuario o token_hash)
├── accion: str
├── fecha: datetime
├── ip: str
├── agente_usuario: str
├── exitoso: bool
└── detalle: str
```

## 5. Fuera de alcance

- Formularios HTML y plantillas web visuales (solo controladores y DTOs).
- Envío real de correos mediante servidor SMTP físico (adaptador simulado/memoria).
- Conexión física a base de datos PostgreSQL.
- Gestión de evaluación final de empresa (cubierto en CU-05).
