# Plan: 012-consultar-datos-estudiante (CU-12 Consultar datos estudiante)

## 1. Decisiones que aplican

| ADR | Decisión | Impacto en esta funcionalidad |
|-----|----------|-------------------------------|
| [ADR-001](../../docs/adr/ADR-001-monolito-modular.md) | Monolito modular con Clean Architecture | La consulta reside en el Módulo Prácticas; respeta la regla de dependencia `infraestructura → aplicacion → dominio`. |
| [ADR-004](../../docs/adr/ADR-004-autenticacion-sso-institucional.md) | Autenticación institucional SSO | Coordinador de prácticas y Tutores académicos se autentican con su cuenta institucional. |
| [ADR-005](../../docs/adr/ADR-005-autorizacion-por-roles-y-bitacora.md) | Roles y bitácora con regla de alcance | El Coordinador tiene alcance global; el Tutor **solo puede consultar a sus estudiantes asignados** (`practica.tutor_documento == tutor_documento`). El 100 % de los accesos a datos personales (Ley 1581 / RN-01) se registran en la bitácora. |
| [ADR-007](../../docs/adr/ADR-007-integracion-sia-adaptador-aislado.md) | Adaptador aislado hacia el SIA | La verificación de datos académicos (créditos, promedio, semestre, matrícula) se realiza únicamente a través del puerto `ConsultaAcademicaEstudiante`, con 0 conexiones directas a la base del SIA (RT-03) y tiempo de espera de 10 s (EAC-03). |

## 2. Componentes por capa

Componentes alineados con la [vista de desarrollo](../../docs/vistas/03-desarrollo.md):

### dominio/ (Módulo Prácticas)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/practicas/dominio/datos_academicos_estudiante.py` | Value Object `DatosAcademicosEstudiante`: créditos aprobados, promedio acumulado, semestre actual, matrícula activa y estado de respuesta del SIA. |
| `src/modulos/practicas/dominio/puertos/consulta_academica_estudiante.py` | Puerto `ConsultaAcademicaEstudiante`: consulta al servicio docente del SIA con tiempo de espera de 10 s y excepciones `SIATimeoutError` y `SIAError` (ADR-007, RT-03). |
| `src/modulos/practicas/dominio/puertos/practica_repository.py` | Métodos `obtener_activa_por_estudiante`, `obtener_por_estudiante` y `listar_por_tutor` para resolver estado de práctica y alcance del tutor. |

### aplicacion/ (Módulo Prácticas)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/practicas/aplicacion/dto_consulta_estudiante.py` | DTOs de consulta: `DatosEstudianteDTO` y `ResumenEstudianteDTO`. |
| `src/modulos/practicas/aplicacion/consultar_datos_estudiante.py` | Caso de uso `ConsultarDatosEstudiante`: aplica la regla de alcance del tutor (ADR-005), orquesta datos locales de práctica y consulta tolerante a fallos del SIA (EAC-03). |

### infraestructura/ (adaptadores)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/practicas/infraestructura/adaptador_practica_memoria.py` | Implementación en memoria para búsqueda de prácticas por estudiante y por tutor. |
| `src/modulos/practicas/infraestructura/adaptador_sia_estudiante_memoria.py` | Adaptador simulado en memoria del SIA con simulación de timeout (10 s) y errores de comunicación. |

### entradas/

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/entradas/controlador_consulta_estudiante.py` | Controlador web interno: valida rol y alcance (`Coordinador de prácticas` o `Tutor`), registrando el 100 % de los accesos en la bitácora de auditoría (ADR-005, RN-01). |

## 3. Flujo

### Camino principal: Coordinador o Tutor autorizado consulta estudiante

1. El usuario invoca `ControladorConsultaEstudiante.consultar_estudiante(estudiante_documento, usuario_id, rol, tutor_documento, ip, agente)`.
2. Se valida el rol del usuario (`Coordinador de prácticas` o `Tutor`). Si es otro rol (p. ej. `Estudiante`), se rechaza con `PermissionError` y se registra acceso denegado en la bitácora.
3. Se invoca el caso de uso `ConsultarDatosEstudiante.ejecutar(estudiante_documento, usuario_id, rol, tutor_documento)`.
4. El caso de uso consulta la práctica activa del estudiante en `PracticaRepository`.
5. **Regla de alcance (ADR-005)**: Si el rol es `Tutor`:
   - Si el estudiante no tiene práctica o `practica.tutor_documento != tutor_documento`, se lanza `PermissionError("Regla de alcance: el tutor solo puede consultar a sus estudiantes asignados.")`.
6. Se consulta la información académica del estudiante en el SIA vía `ConsultaAcademicaEstudiante.consultar_academica(estudiante_documento)` con timeout de 10 s:
   - Si el SIA responde: se incorporan créditos, promedio, semestre y estado de matrícula.
   - Si ocurre timeout o error: se marcan datos de SIA como `disponible_sia=False` con mensaje de indisponibilidad temporal, sin interrumpir la entrega de los datos locales de la práctica (EAC-03, RT-03).
7. Se construye y retorna `DatosEstudianteDTO`.
8. El controlador registra en la bitácora de auditoría (`RegistroAcceso`) el acceso exitoso.

### Camino alterno: Estudiante sin práctica registrada

1. Si el Coordinador consulta a un estudiante que aún no posee práctica registrada, se consultan sus datos al SIA y se retorna `DatosEstudianteDTO` con `tiene_practica_activa=False`.
2. Se asienta en la bitácora.

## 4. Modelo de datos

- **Practica**: `id: UUID`, `estudiante_documento: str`, `programa: str`, `empresa_id: str`, `supervisor_id: str`, `periodo: str`, `fecha_inicio: date`, `fecha_fin: date`, `estado: EstadoPractica`, `tutor_documento: str | None`.
- **DatosAcademicosEstudiante**: `creditos_aprobados: int`, `promedio_acumulado: float`, `semestre_actual: int`, `matricula_activa: bool`, `disponible_sia: bool`.
- **RegistroAcceso**: `sujeto: str`, `accion: str`, `fecha: datetime`, `ip: str`, `agente_usuario: str`, `exitoso: bool`, `detalle: str`.

## 5. Fuera de alcance

- Registro de una nueva postulación (CU-03).
- Registro o modificación de práctica (CU-02).
- Asignación de tutor (CU-01).
