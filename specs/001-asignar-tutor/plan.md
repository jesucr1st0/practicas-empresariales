# Plan: 001-asignar-tutor (CU-01 Asignar tutor)

## 1. Decisiones que aplican

| ADR | Decisión | Impacto en esta funcionalidad |
|-----|----------|-------------------------------|
| [ADR-012](../../docs/adr/ADR-012-asignacion-tutores-sugerida-con-confirmacion.md) | Asignación de tutores sugerida con confirmación | El sistema calcula y sugiere el tutor con menor carga según programa y regla; el coordinador confirma o ajusta; se guarda origen (`sugerida` o `manual`). |
| [ADR-005](../../docs/adr/ADR-005-autorizacion-por-roles-y-bitacora.md) | Autorización por roles y bitácora de accesos | Solo el Coordinador puede asignar; cada acceso registra en bitácora; la asignación define el alcance de consulta del tutor. |
| [ADR-009](../../docs/adr/ADR-009-reglas-versionadas-por-programa.md) | Reglas versionadas por programa | La capacidad máxima de estudiantes por tutor se consulta de la versión de regla fijada en la práctica. |
| [ADR-001](../../docs/adr/ADR-001-monolito-modular.md) | Monolito modular con Clean Architecture | Módulo `tutores_asignacion` interactúa con `practicas` e `identidad_accesos` mediante contratos limpios sin ciclos. |

## 2. Componentes por capa

Basado en la [vista de desarrollo](../../docs/vistas/03-desarrollo.md):

### dominio/ (Módulo Tutores y Asignación)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/tutores_asignacion/dominio/asignacion_tutor.py` | Entidad `AsignacionTutor`: `id`, `practica_id`, `tutor_documento`, `fecha`, `vigente`, `origen` (`sugerida` / `manual`), `observaciones`. |
| `src/modulos/tutores_asignacion/dominio/origen_asignacion.py` | Enum `OrigenAsignacion`: `SUGERIDA`, `MANUAL`. |
| `src/modulos/tutores_asignacion/dominio/tutor.py` | Entidad de soporte `Tutor`: `documento`, `nombre`, `correo`, `programa`, `activo`. |
| `src/modulos/tutores_asignacion/dominio/puertos/asignacion_repository.py` | Puerto `AsignacionRepository`: guardar asignación, obtener vigente por práctica, obtener historial por práctica, contar asignaciones vigentes por tutor. |
| `src/modulos/tutores_asignacion/dominio/puertos/consulta_practica_asignacion.py` | Puerto `ConsultaPracticaAsignacion`: consultar datos de la práctica (programa, versión de regla) y actualizar el tutor vigente en la práctica (evita dependencia circular con módulo prácticas). |
| `src/modulos/tutores_asignacion/dominio/puertos/consulta_regla_tutor.py` | Puerto `ConsultaReglaTutor`: obtener la capacidad máxima por tutor para una versión de regla de programa. |

### aplicacion/ (Módulo Tutores y Asignación)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/tutores_asignacion/aplicacion/sugerir_tutor.py` | Caso de uso `SugerirTutor`: evalúa tutores activos del programa de la práctica, consulta sus cargas vigentes y sugiere el de menor carga; alerta si todos superan el tope. |
| `src/modulos/tutores_asignacion/aplicacion/confirmar_asignacion.py` | Caso de uso `ConfirmarAsignacion`: desactiva asignación vigente previa si existe, guarda nueva `AsignacionTutor` con origen (`sugerida` o `manual`), y actualiza el tutor vigente en la práctica. |
| `src/modulos/tutores_asignacion/aplicacion/dto.py` | DTOs de entrada y salida: `SugerenciaTutorDTO`, `ConfirmarAsignacionDTO`, `ResultadoAsignacionDTO`. |

### infraestructura/ (adaptadores en memoria)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/tutores_asignacion/infraestructura/adaptador_asignacion_memoria.py` | Implementación en memoria de `AsignacionRepository`. |
| `src/modulos/tutores_asignacion/infraestructura/adaptador_servicio_practica_memoria.py` | Implementación en memoria de `ConsultaPracticaAsignacion`. |
| `src/modulos/tutores_asignacion/infraestructura/adaptador_servicio_reglas_memoria.py` | Implementación en memoria de `ConsultaReglaTutor`. |

### entradas/

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/entradas/controlador_asignacion_tutor.py` | Punto de entrada para sugerir y confirmar tutor desde la interfaz web o pruebas de integración. |

## 3. Flujo

1. **Sugerencia:**
   - El Coordinador solicita sugerencia para `practica_id`.
   - `SugerirTutor` obtiene el programa y regla de la práctica vía `ConsultaPracticaAsignacion`.
   - Obtiene capacidad máxima vía `ConsultaReglaTutor`.
   - Consulta tutores activos del programa y cuenta asignaciones vigentes con `AsignacionRepository`.
   - Retorna el tutor con menor carga actual e indicador de si supera capacidad.

2. **Confirmación:**
   - El Coordinador confirma (usando sugerencia o seleccionando otro tutor manualmente).
   - `ConfirmarAsignacion` pasa la asignación vigente previa a `vigente = False`.
   - Registra la nueva `AsignacionTutor(vigente=True, origen=...)`.
   - Invoca `ConsultaPracticaAsignacion.actualizar_tutor_vigente(practica_id, tutor_documento)`.

## 4. Modelo de datos

```
AsignacionTutor
├── id: UUID
├── practica_id: UUID
├── tutor_documento: str
├── fecha: datetime
├── vigente: bool
├── origen: OrigenAsignacion (SUGERIDA | MANUAL)
└── observaciones: str | None
```

## 5. Fuera de alcance

- Autenticación SSO en vivo (se valida permiso en capa de entrada simulada).
- Interfaz gráfica web (HTML/CSS/JS); solo controlador / servicio de aplicación.
- Base de datos relacional PostgreSQL física (en esta etapa adaptadores en memoria según ADR-002).
