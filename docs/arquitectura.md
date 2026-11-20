# Documento de arquitectura: Sistema de Gestión de Prácticas Empresariales

> Versión 1.0 | Estado: en construcción

## 1. Introducción y objetivos

Sistema para centralizar la gestión de las prácticas empresariales de la Facultad de Ingenierías: postulación, asignación de tutores, seguimiento de horas, evaluación de la empresa y generación del acta final. El problema y la oportunidad están en [vision.md §1](vision.md#1-problema-u-oportunidad) y los objetivos de negocio (OB-01 a OB-05) en [vision.md §2](vision.md#2-objetivos-de-negocio). Los stakeholders están en [vision.md §4](vision.md#4-stakeholders).

## 2. Restricciones

Las restricciones vigentes (RT-01 a RT-04 y RN-01 a RN-05) están en [drivers.md §3](drivers.md#3-restricciones). Cada una se atiende en los ADR indicados en la sección 7.

## 3. Contexto del sistema

El sistema como caja negra, con sus cinco actores (Estudiante, Tutor académico, Coordinador de prácticas, Administrador, Supervisor de empresa) y tres sistemas externos (SIA, SSO institucional y Servidor de correo institucional), está en [contexto.md](contexto.md), con su diagrama C4 nivel 1 en [diagramas/contexto.puml](diagramas/contexto.puml).

## 4. Estrategia de solución

Resumen de las decisiones de alto nivel extraídas de los ADR:

| Driver | Enfoque | ADR |
|--------|---------|-----|
| PA-05: carga moderada (~250 prácticas activas, 4 desarrolladores) | Monolito modular: un solo artefacto desplegable, con módulos de límites explícitos | [ADR-001](adr/ADR-001-monolito-modular.md) |
| PA-01: integración con el SIA y tolerancia a sus fallos | Adaptador aislado con reintentos cada 15 min durante 24 h; cola en la base de datos | [ADR-007](adr/ADR-007-integracion-sia-adaptador-aislado.md), [ADR-008](adr/ADR-008-verificacion-asincrona-con-reintentos.md) |
| PA-02: doble acceso (internos y externos) | SSO institucional para usuarios internos; enlace de un solo uso para supervisores | [ADR-004](adr/ADR-004-autenticacion-sso-institucional.md), [ADR-006](adr/ADR-006-acceso-externo-enlace-un-solo-uso.md) |
| PA-03: reglas variables por programa y periodo | Reglas versionadas e inmutables; la práctica referencia la versión vigente al registrarse | [ADR-009](adr/ADR-009-reglas-versionadas-por-programa.md) |
| PA-04: integridad, trazabilidad y retención del acta | Acta inmutable con huella de integridad; retención parametrizable | [ADR-010](adr/ADR-010-acta-final-plantilla-oficial-inmutable.md), [ADR-011](adr/ADR-011-retencion-documental-y-datos-personales.md) |
| EAC-01: cambio de reglas en ≤ 8 h-persona, 1 módulo, ≤ 5 min parada | Módulo Reglas aislado; redespliegue de un único artefacto | [ADR-001](adr/ADR-001-monolito-modular.md), [ADR-009](adr/ADR-009-reglas-versionadas-por-programa.md) |
| EAC-02: acceso externo sin cuenta, ≤ 3 s, 100 % registrado | Formulario liviano con enlace de un solo uso; bitácora de solo inserción | [ADR-006](adr/ADR-006-acceso-externo-enlace-un-solo-uso.md), [ADR-005](adr/ADR-005-autorizacion-por-roles-y-bitacora.md) |
| EAC-03: tolerancia a fallos del SIA, 0 postulaciones perdidas | Cola en base de datos, reintentos programados, estado «pendiente de verificación» | [ADR-007](adr/ADR-007-integracion-sia-adaptador-aislado.md), [ADR-008](adr/ADR-008-verificacion-asincrona-con-reintentos.md) |

## 5. Vistas (4+1)

Modelo 4+1: cuatro vistas documentadas en cinco partes (presentación, catálogo, justificación, comportamiento y vistas relacionadas) más los escenarios que las validan. Los diagramas están en [diagramas/](diagramas/).

| Vista | Documento | Diagrama | Notación |
|-------|-----------|----------|----------|
| Contexto (marco) | [contexto.md](contexto.md) | [contexto.puml](diagramas/contexto.puml) | C4 nivel 1 |
| Lógica | [vistas/01-logica.md](vistas/01-logica.md) | [01-logica.puml](diagramas/01-logica.puml) | UML (modelo de dominio) |
| Procesos | [vistas/02-procesos.md](vistas/02-procesos.md) | [02-procesos.puml](diagramas/02-procesos.puml) | C4 nivel 2 |
| Desarrollo | [vistas/03-desarrollo.md](vistas/03-desarrollo.md) | [03-desarrollo.puml](diagramas/03-desarrollo.puml) | C4 nivel 3, capas y usos |
| Física | [vistas/04-fisica.md](vistas/04-fisica.md) | [04-fisica.puml](diagramas/04-fisica.puml) | C4 despliegue |
| Escenarios (+1) | [escenarios.md](escenarios.md) | [secuencias/](diagramas/secuencias/) | UML (secuencia arquitectónica) |

Trazabilidad: [matriz-cobertura.md](matriz-cobertura.md). Tabla de escenarios: [drivers.md §6](drivers.md#6-escenarios).

## 6. Conceptos transversales

Preocupaciones arquitectónicas que cruzan varios módulos y cómo se resuelven:

| Concepto | Cómo se resuelve | Dónde se ve |
|----------|-------------------|-------------|
| Autenticación interna | Delegada al SSO institucional; el sistema no guarda contraseñas | [ADR-004](adr/ADR-004-autenticacion-sso-institucional.md), Adaptador SSO en [03-desarrollo.md](vistas/03-desarrollo.md) |
| Autorización por roles | Roles y permisos en la base de datos; filtro de alcance del tutor | [ADR-005](adr/ADR-005-autorizacion-por-roles-y-bitacora.md), Módulo Identidad y accesos |
| Acceso externo sin cuenta | Enlace de un solo uso con vencimiento a 30 días; formulario liviano | [ADR-006](adr/ADR-006-acceso-externo-enlace-un-solo-uso.md), Formulario de acceso externo |
| Integración con el SIA | Adaptador aislado; puerto ConsultaAcademica; tiempo de espera de 10 s | [ADR-007](adr/ADR-007-integracion-sia-adaptador-aislado.md), Adaptador SIA |
| Tolerancia a fallos del SIA | Verificación asíncrona; cola en base de datos; reintentos cada 15 min | [ADR-008](adr/ADR-008-verificacion-asincrona-con-reintentos.md), Planificador de tareas |
| Versionado de reglas | Reglas inmutables por programa; la práctica referencia la versión vigente | [ADR-009](adr/ADR-009-reglas-versionadas-por-programa.md), Módulo Reglas |
| Inmutabilidad del acta | PDF con huella de integridad; corrección crea acta nueva y anula la anterior | [ADR-010](adr/ADR-010-acta-final-plantilla-oficial-inmutable.md), Módulo Actas |
| Notificaciones | Correo institucional (SMTP); registro de cada envío, incluidos los fallidos | [ADR-013](adr/ADR-013-notificaciones-por-correo-institucional.md), Módulo Notificaciones |
| Trazabilidad y bitácora | Registro de accesos de solo inserción (quién, qué, cuándo, desde dónde) | [ADR-005](adr/ADR-005-autorizacion-por-roles-y-bitacora.md), RegistroAcceso |
| Retención documental | Actas y evidencias sin borrado físico antes del plazo; retención parametrizable | [ADR-011](adr/ADR-011-retencion-documental-y-datos-personales.md), Almacenamiento de archivos |

## 7. Decisiones de diseño

### Índice de ADR

| ADR | Decisión | Estado | Drivers |
|-----|----------|--------|---------|
| [ADR-001](adr/ADR-001-monolito-modular.md) | Aplicación única y modular (monolito modular) | Aceptado | PA-05, EAC-01, RT-01, RT-04, RN-05 |
| [ADR-002](adr/ADR-002-persistencia-relacional.md) | Base de datos relacional única | Aceptado | PA-04, RT-04, RN-05, RT-03 |
| [ADR-003](adr/ADR-003-despliegue-infraestructura-institucional.md) | Despliegue en infraestructura institucional | Aceptado | RT-01, RT-04, RN-05 |
| [ADR-004](adr/ADR-004-autenticacion-sso-institucional.md) | Autenticación interna con SSO institucional | Aceptado | RT-02, PA-02 |
| [ADR-005](adr/ADR-005-autorizacion-por-roles-y-bitacora.md) | Autorización por roles y bitácora de accesos | Aceptado | RN-01, PA-04, EAC-02 |
| [ADR-006](adr/ADR-006-acceso-externo-enlace-un-solo-uso.md) | Acceso externo por enlace de un solo uso | Aceptado | EAC-02, RN-04, PA-02 |
| [ADR-007](adr/ADR-007-integracion-sia-adaptador-aislado.md) | Adaptador aislado hacia el SIA | Aceptado | RT-03, PA-01, EAC-03 |
| [ADR-008](adr/ADR-008-verificacion-asincrona-con-reintentos.md) | Verificación asíncrona con reintentos | Aceptado | EAC-03, PA-01, CU-03 |
| [ADR-009](adr/ADR-009-reglas-versionadas-por-programa.md) | Reglas versionadas por programa | Aceptado | EAC-01, PA-03, CU-02 |
| [ADR-010](adr/ADR-010-acta-final-plantilla-oficial-inmutable.md) | Acta final inmutable desde plantilla oficial | Aceptado | CU-06, RN-03, PA-04 |
| [ADR-011](adr/ADR-011-retencion-documental-y-datos-personales.md) | Retención documental y de datos personales | Propuesto | RN-02, RN-01, PA-04 |
| [ADR-012](adr/ADR-012-asignacion-tutores-sugerida-con-confirmacion.md) | Asignación de tutores sugerida con confirmación | Propuesto | CU-01 |
| [ADR-013](adr/ADR-013-notificaciones-por-correo-institucional.md) | Notificaciones por correo institucional | Aceptado | CU-04, CU-05, EAC-02, EAC-03 |

### Cobertura de drivers

| Driver | ADR que lo cubren |
|--------|-------------------|
| CU-01 | 012, 005, 001 |
| CU-02 | 001, 009 |
| CU-03 | 007, 008, 013 |
| CU-04 | 006, 013, 005 |
| CU-05 | 006, 013, 005 |
| CU-06 | 009, 010, 011 |
| EAC-01 | 001, 009 |
| EAC-02 | 006, 005, 013 |
| EAC-03 | 007, 008, 013 |
| RT-01 | 003, 001 |
| RT-02 | 004 |
| RT-03 | 007, 002 |
| RT-04 | 003, 002 |
| RN-01 | 005, 011 |
| RN-02 | 010, 011 |
| RN-03 | 010 |
| RN-04 | 006 |
| RN-05 | 001, 002, 003, 008, 013 |
| PA-01 | 007, 008 |
| PA-02 | 004, 006 |
| PA-03 | 009 |
| PA-04 | 002, 005, 010, 011 |
| PA-05 | 001 |

### Drivers sin ADR propio (declarados como riesgo)

- **CU-07 a CU-12** (exportar acta, registros maestros y consultas): sin impacto arquitectónico propio; se resuelven dentro de los módulos de [ADR-001](adr/ADR-001-monolito-modular.md) (CU-07 con [ADR-010](adr/ADR-010-acta-final-plantilla-oficial-inmutable.md); CU-11 y CU-12 con [ADR-007](adr/ADR-007-integracion-sia-adaptador-aislado.md)).
- **Vigencia de convenio, migración de prácticas históricas y diagnóstico para mesa de ayuda** (cuadrante de baja importancia y bajo impacto de [drivers.md §5](drivers.md#5-matriz-de-priorización)): sin ADR; **riesgo asumido**. La migración se relaciona con el riesgo RI-01 de [vision.md](vision.md#riesgos).

## 8. Requisitos de calidad

Los escenarios de atributos de calidad están en [drivers.md §2](drivers.md#2-escenarios-de-atributos-de-calidad):

| EAC | Atributo | Prioridad | ADR | Se verifica en |
|-----|----------|-----------|-----|----------------|
| [EAC-01](drivers.md#eac-01-mantenibilidad-modificabilidad) | Mantenibilidad (modificabilidad) | Alta | ADR-001, ADR-009 | [specs/002-registrar-practica/](../specs/002-registrar-practica/), ESC-02, ESC-06, ESC-07 |
| [EAC-02](drivers.md#eac-02-seguridad-acceso-externo-sin-cuenta) | Seguridad (acceso externo sin cuenta) | Alta | ADR-006, ADR-005 | ESC-04, ESC-05 |
| [EAC-03](drivers.md#eac-03-fiabilidad-tolerancia-a-fallos-del-sia) | Fiabilidad (tolerancia a fallos del SIA) | Alta | ADR-007, ADR-008 | [specs/003-realizar-postulacion/](../specs/003-realizar-postulacion/), ESC-03 |

## 9. Riesgos y deuda técnica

| ID | Riesgo o deuda | Origen | Impacto | Respuesta |
|----|----------------|--------|---------|-----------|
| R-01 | Información histórica incompleta, duplicada o desactualizada en Excel | RI-01 de [vision.md](vision.md) | Datos incorrectos al migrar al nuevo sistema | Revisar, depurar y validar los datos antes de migrarlos |
| R-02 | Resistencia de usuarios a adoptar el sistema | RI-02 de [vision.md](vision.md) | Baja adopción; retorno al proceso manual | Capacitación y documentación de uso |
| R-03 | Falta de disponibilidad de las empresas para evaluar | RI-03 de [vision.md](vision.md) | Prácticas sin evaluación ni acta final | Fechas límite, notificaciones y seguimiento (ADR-013) |
| R-04 | Acceso no autorizado o exposición de datos personales | RI-04 de [vision.md](vision.md) | Incumplimiento de Ley 1581 | Roles, bitácora (ADR-005), SSO (ADR-004) y enlace con vencimiento (ADR-006) |
| R-05 | Catálogo tecnológico institucional sin confirmar (RT-04) | RT-04, pendiente de confirmación | Retraso en implementación; elección de tecnología que luego cambie | Usar candidatos (PostgreSQL, Python); confirmar antes del sprint 1 |
| R-06 | Protocolo del SSO sin confirmar | RT-02, pendiente de confirmación | Bloqueo de autenticación durante integración | Adaptador SSO con interfaz estable (ADR-004); confirmar protocolo (OIDC, SAML o CAS) |
| R-07 | Servicios del SIA sin especificar | RT-03, pendiente de confirmación | Adaptador SIA no compilable hasta confirmar endpoints | Confirmar lista de servicios y protocolo con el Administrador del SIA |
| R-08 | ADR-011 y ADR-012 en estado «Propuesto» | Decisiones pendientes de aprobación | Los plazos de retención o criterios de asignación pueden cambiar | Revisar al confirmar; las vistas ya los reflejan |
| DT-01 | Secciones 4, 6, 9 y 10 de este documento estaban pendientes | Versión parcial del documento de arquitectura | Riesgo de drift entre documentación y código | Este documento las completa en la versión 1.0 |

## 10. Glosario

Los términos del dominio, con su definición y su nombre en el código. Los nombres de clases, métodos y variables del proyecto deben usar estos términos.

| Término | Definición | Nombre en el código |
|---------|------------|---------------------|
| Programa | Programa académico de la Facultad (p. ej. Ingeniería de Sistemas) | `Programa` |
| Regla de programa | Versión inmutable de las reglas de práctica de un programa: horas mínimas, capacidad máxima por tutor, vigencia | `ReglaPrograma` |
| Estudiante | Quien realiza la práctica; sus datos académicos se consultan al SIA | `Estudiante` |
| Tutor | Docente que acompaña y da seguimiento a los estudiantes asignados | `Tutor` |
| Empresa | Organización donde se realiza la práctica | `Empresa` |
| Supervisor | Persona de la empresa que valida horas y evalúa al estudiante; no tiene cuenta | `Supervisor` |
| Coordinador de prácticas | Responsable administrativo que registra prácticas, asigna tutores y genera actas | — (rol, no entidad) |
| Administrador | Gestiona usuarios, roles y datos maestros | — (rol, no entidad) |
| Postulación | Solicitud del estudiante para hacer práctica; pasa por estados de verificación | `Postulacion` |
| Práctica | La práctica empresarial en sí; se rige por la versión de regla vigente al registrarse | `Practica` |
| Asignación de tutor | Vínculo de un tutor con una práctica; el sistema sugiere y el coordinador confirma | `AsignacionTutor` |
| Registro de horas | Horas realizadas y su validación por parte del supervisor y el tutor | `RegistroHoras` |
| Evaluación | Evaluación del estudiante hecha por la empresa; una por práctica, no se modifica | `Evaluacion` |
| Acta final | Documento oficial de cierre con huella de integridad; inmutable | `ActaFinal` |
| Enlace de acceso | Autorización de un solo uso para el supervisor; vence a los 30 días | `EnlaceAcceso` |
| Registro de acceso | Constancia de un acceso a datos personales; solo se agrega, nunca se modifica | `RegistroAcceso` |
| Estado de postulación | pendiente de verificación · verificada · rechazada · revisión manual | `EstadoPostulacion` |
| Estado de práctica | registrada · en curso · finalizada · cerrada (con acta vigente) | `EstadoPractica` |
| Estado de acta | vigente · anulada | `EstadoActa` |
| Estado de enlace | vigente · usado · vencido · revocado | `EstadoEnlace` |
| Consulta académica | Puerto para verificar datos académicos del estudiante en el SIA | `ConsultaAcademica` |
| Repositorio | Puerto de persistencia; cada entidad tiene el suyo | `<Entidad>Repository` |
| Almacén de archivos | Puerto para guardar y recuperar archivos (actas, evidencias) | `AlmacenArchivos` |
| Proveedor de identidad | Puerto para autenticar usuarios internos vía SSO | `ProveedorIdentidad` |
| Envío de correo | Puerto para enviar notificaciones por correo institucional | `EnvioCorreo` |
