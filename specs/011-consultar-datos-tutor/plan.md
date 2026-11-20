# Plan: 011-consultar-datos-tutor (CU-11 Consultar datos tutor)

## 1. Decisiones que aplican

| ADR | Decisión | Impacto en esta funcionalidad |
|-----|----------|-------------------------------|
| [ADR-001](../../docs/adr/ADR-001-monolito-modular.md) | Monolito modular con Clean Architecture | La consulta reside en el Módulo Tutores y asignación; respeta la regla de dependencia `infraestructura → aplicacion → dominio`. |
| [ADR-004](../../docs/adr/ADR-004-autenticacion-sso-institucional.md) | Autenticación SSO institucional | El Coordinador de prácticas accede autenticado con credenciales institucionales. |
| [ADR-005](../../docs/adr/ADR-005-autorizacion-por-roles-y-bitacora.md) | Roles y bitácora de accesos | Solo el Coordinador de prácticas puede consultar los datos y carga de los tutores; el 100 % de los accesos a datos personales (Ley 1581 / RN-01) se registran en la bitácora. |
| [ADR-007](../../docs/adr/ADR-007-integracion-sia-adaptador-aislado.md) | Adaptador aislado hacia el SIA | La consulta de datos institucionales/docentes se realiza únicamente mediante servicios vía puerto `ConsultaAcademicaTutor`, con 0 conexiones directas a la base de datos del SIA (RT-03) y tiempo de espera de 10 s (EAC-03). |
| [ADR-009](../../docs/adr/ADR-009-reglas-versionadas-por-programa.md) | Reglas versionadas por programa | La capacidad máxima de estudiantes por tutor se obtiene de la regla vigente del programa académico. |
| [ADR-012](../../docs/adr/ADR-012-asignacion-tutores-sugerida-con-confirmacion.md) | Asignación de tutores y balance de carga | La carga docente y disponibilidad se calculan a partir de las asignaciones vigentes e historial. |

## 2. Componentes por capa

Componentes alineados con la [vista de desarrollo](../../docs/vistas/03-desarrollo.md):

### dominio/ (Módulo Tutores y asignación)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/tutores_asignacion/dominio/datos_academicos_tutor.py` | Value Object `DatosAcademicosTutor`: departamento, categoría, dedicación y estado de disponibilidad en SIA. |
| `src/modulos/tutores_asignacion/dominio/puertos/consulta_academica_tutor.py` | Puerto `ConsultaAcademicaTutor`: consultar datos académicos/institucionales del docente en el SIA con timeout de 10 s (ADR-007, RT-03). |
| `src/modulos/tutores_asignacion/dominio/puertos/asignacion_repository.py` | Métodos `obtener_tutor_por_documento` y `obtener_asignaciones_vigentes_por_tutor` para consultar datos y prácticas asignadas. |
| `src/modulos/tutores_asignacion/dominio/puertos/consulta_regla_tutor.py` | Puerto `ConsultaReglaTutor`: consultar capacidad máxima docente por versión de regla de programa (ADR-009). |

### aplicacion/ (Módulo Tutores y asignación)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/tutores_asignacion/aplicacion/dto_consulta_tutor.py` | DTOs de consulta: `DatosTutorDTO`, `ResumenTutorDTO`, `PracticaAsignadaDTO`. |
| `src/modulos/tutores_asignacion/aplicacion/consultar_datos_tutor.py` | Caso de uso `ConsultarDatosTutor`: orquesta consulta local, asignaciones vigentes, regla de capacidad y consulta al SIA tolerante a fallos. |
| `src/modulos/tutores_asignacion/aplicacion/listar_tutores_programa.py` | Caso de uso `ListarTutoresPrograma`: genera la vista consolidada de tutores, cargas y disponibilidad para el tablero de estado. |

### infraestructura/ (adaptadores)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/tutores_asignacion/infraestructura/adaptador_asignacion_memoria.py` | Implementación en memoria de la búsqueda de tutor por documento y listado de asignaciones vigentes por tutor. |
| `src/modulos/tutores_asignacion/infraestructura/adaptador_sia_tutor_memoria.py` | Adaptador en memoria simulado del SIA para datos del docente, con soporte de simulación de timeout (10 s) y errores de conexión (ADR-007, EAC-03). |
| `src/modulos/tutores_asignacion/infraestructura/adaptador_servicio_reglas_memoria.py` | Adaptador de consulta de capacidad de tutores por regla de programa. |

### entradas/

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/entradas/controlador_consulta_tutor.py` | Punto de entrada para la consulta de tutores: valida el rol `Coordinador de prácticas` y registra cada acceso en la bitácora de auditoría (ADR-005, RN-01). |

## 3. Flujo

### Camino principal: Consulta de un tutor individual

1. El Coordinador de prácticas invoca `ControladorConsultaTutor.consultar_tutor(documento, usuario_id, rol, ip, agente)`.
2. El controlador valida el rol institucional (`Coordinador de prácticas`). Si no coincide, rechaza con `PermissionError` y registra el acceso denegado en la bitácora.
3. Se invoca el caso de uso `ConsultarDatosTutor.ejecutar(documento)`.
4. El caso de uso solicita los datos del tutor a `AsignacionRepository.obtener_tutor_por_documento(documento)`. Si no existe, genera `LookupError`.
5. Se obtienen las asignaciones vigentes del tutor mediante `AsignacionRepository.obtener_asignaciones_vigentes_por_tutor(documento)`.
6. Se consulta la capacidad máxima según la versión de regla del programa en `ConsultaReglaTutor`.
7. Se invoca `ConsultaAcademicaTutor.consultar_docente(documento)`:
   - Si el SIA responde exitosamente dentro de 10 s: se extraen departamento, categoría y dedicación institucional.
   - Si ocurre timeout o error en el SIA: se marca `disponible_sia=False` y mensaje de no disponibilidad temporal, sin abortar la operación (EAC-03).
8. Se construye y retorna `DatosTutorDTO` con la carga actual, capacidad, prácticas asignadas y datos del SIA.
9. El controlador registra el acceso exitoso en la bitácora (`RegistroAcceso`).

### Camino alterno: Listado para tablero de estado por programa

1. El Coordinador invoca `ControladorConsultaTutor.listar_tutores_programa(programa, usuario_id, rol, ip, agente)`.
2. El controlador valida rol y registra acceso en la bitácora.
3. El caso de uso `ListarTutoresPrograma.ejecutar(programa)` obtiene los tutores activos del programa y calcula su carga docente actual frente a la capacidad máxima.
4. Retorna una colección de `ResumenTutorDTO` listos para el tablero de estado.

## 4. Modelo de datos

- **Tutor**: `documento: str`, `nombre: str`, `correo: str`, `programa: str`, `activo: bool`.
- **DatosAcademicosTutor**: `departamento: str`, `categoria: str`, `dedicacion: str`, `disponible_sia: bool`.
- **AsignacionTutor**: `id: UUID`, `practica_id: UUID`, `tutor_documento: str`, `vigente: bool`, `fecha: date`, `origen: OrigenAsignacion`.
- **RegistroAcceso**: `sujeto: str`, `accion: str`, `fecha: datetime`, `ip: str`, `agente_usuario: str`, `exitoso: bool`, `detalle: str`.

## 5. Fuera de alcance

- Registro de nuevos tutores docentes (CU-09).
- Asignación manual o sugerida de tutor a práctica (cubierto en CU-01).
- Consulta de datos académicos de estudiantes (cubierto en CU-12).
