# Plan: 005-evaluar-estudiante (CU-05 Evaluar al estudiante por la empresa)

## 1. Decisiones que aplican

| ADR | Decisión | Impacto en esta funcionalidad |
|-----|----------|-------------------------------|
| [ADR-001](../../docs/adr/ADR-001-monolito-modular.md) | Monolito modular con Clean Architecture | Módulo `evaluaciones` encapsula el registro y consulta de evaluaciones de la empresa; se comunica con `identidad_accesos`, `practicas` y `notificaciones` mediante puertos sin acoplamientos circulares. |
| [ADR-002](../../docs/adr/ADR-002-persistencia-relacional.md) | Persistencia relacional | Repositorio en memoria en esta etapa para `Evaluacion`. |
| [ADR-005](../../docs/adr/ADR-005-autorizacion-por-roles-y-bitacora.md) | Autorización por roles y bitácora de accesos | Todo acceso externo del supervisor queda registrado al 100 % en la bitácora con IP, agente y resultado (concedido o denegado). |
| [ADR-006](../../docs/adr/ADR-006-acceso-externo-enlace-un-solo-uso.md) | Enlace de un solo uso con vencimiento | Acceso por token seguro sin contraseña (RN-04); el enlace se invalida pasando a estado "usado" tras enviar la evaluación. |
| [ADR-013](../../docs/adr/ADR-013-notificaciones-por-correo-institucional.md) | Notificaciones por correo institucional | Envíos de recordatorios periódicos con el enlace cuando la evaluación esté pendiente y el enlace siga vigente. |

## 2. Componentes por capa

Basado en la [vista de desarrollo](../../docs/vistas/03-desarrollo.md):

### dominio/ (`src/modulos/evaluaciones/dominio/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `evaluacion.py` | Entidad `Evaluacion`: `id`, `practica_id`, `fecha`, `calificacion`, `observaciones`. Regla: una por práctica, inmutable una vez guardada. |
| `puertos/evaluacion_repository.py` | Puerto `EvaluacionRepository`: guardar, buscar por práctica, verificar existencia. |
| `puertos/servicio_actualizacion_practica_evaluacion.py` | Puerto `ServicioActualizacionPracticaEvaluacion`: notificar al módulo Prácticas la recepción de la evaluación. |
| `puertos/servicio_invalidacion_enlace.py` | Puerto `ServicioInvalidacionEnlace`: solicitar a Identidad y accesos la invalidación del token tras el envío. |
| `puertos/servicio_recordatorio_evaluacion.py` | Puerto `ServicioRecordatorioEvaluacion`: enviar correo con recordatorio y enlace al supervisor. |

### aplicacion/ (`src/modulos/evaluaciones/aplicacion/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `dto.py` | DTOs: `RegistrarEvaluacionDTO`, `EvaluacionDTO`, `ResultadoEvaluacionDTO`. |
| `registrar_evaluacion.py` | Caso de uso `RegistrarEvaluacion`: verifica que no exista evaluación previa, crea `Evaluacion`, notifica a Prácticas, invalida enlace vía `ServicioInvalidacionEnlace`. |
| `consultar_evaluacion.py` | Caso de uso `ConsultarEvaluacion`: consulta la evaluación de una práctica. |
| `enviar_recordatorio_evaluacion.py` | Caso de uso `EnviarRecordatorioEvaluacion`: envía recordatorio al supervisor si la evaluación sigue pendiente. |

### infraestructura/ (`src/modulos/evaluaciones/infraestructura/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `adaptador_evaluacion_memoria.py` | Implementación en memoria de `EvaluacionRepository`. |
| `adaptador_servicio_practica_evaluacion_memoria.py` | Adaptador en memoria que registra recepción de evaluación para la práctica. |
| `adaptador_servicio_invalidacion_enlace_memoria.py` | Adaptador que conecta con `GestorEnlacesAcceso` para marcar enlace como `USADO`. |
| `adaptador_servicio_recordatorio_memoria.py` | Adaptador en memoria para el envío de recordatorios. |

### entradas/ (`src/entradas/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `controlador_acceso_externo_evaluacion.py` | Adaptador de entrada (Formulario de acceso externo): valida el token del supervisor, recibe la evaluación y confirma el registro sin credenciales. |

## 3. Flujo

### 1. Registro de evaluación por el supervisor (Camino principal)
1. El supervisor abre el enlace en su navegador móvil con IP y agente de usuario.
2. `ControladorAccesoExternoEvaluacion` valida el token con `GestorEnlacesAcceso` (verifica que esté vigente y contenga la acción "evaluar") y registra el acceso en la bitácora.
3. El supervisor diligencia y envía la calificación y observaciones.
4. `RegistrarEvaluacion`:
   - Verifica que la práctica no tenga evaluación previa (regla 1 a 0..1 de vista lógica).
   - Crea y persiste la entidad `Evaluacion`.
   - Notifica a `ServicioActualizacionPracticaEvaluacion` para actualizar el estado de la práctica.
   - Invoca `ServicioInvalidacionEnlace` para pasar el enlace a estado `USADO` (ADR-006).
5. Retorna confirmación exitosa al supervisor.

### 2. Intento de reenvío con enlace ya usado
1. El supervisor intenta abrir o enviar de nuevo con el mismo enlace.
2. `GestorEnlacesAcceso` detecta que el enlace está en estado `USADO`.
3. Registra el intento denegado en la bitácora.
4. Lanza error con el mensaje: "enlace no disponible; pida al coordinador que lo reemita".

### 3. Recordatorio periódico
1. El planificador ejecuta `EnviarRecordatorioEvaluacion`.
2. Verifica si la práctica tiene evaluación pendiente y enlace vigente.
3. Envía el correo con el enlace y registra el envío.

## 4. Modelo de datos

```
Evaluacion
├── id: UUID
├── practica_id: UUID
├── fecha: date
├── calificacion: float
└── observaciones: str
```

## 5. Fuera de alcance

- Pantallas HTML o diseño visual web.
- Servidor SMTP real (adaptador simulado en memoria).
- Generación de acta final (CU-06).
