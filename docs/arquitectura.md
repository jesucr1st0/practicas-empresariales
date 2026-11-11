# Documento de arquitectura: Sistema de Gestión de Prácticas Empresariales

> Versión parcial. Las secciones 1, 2, 3, 5, 7 y 8 están completas tras el taller de vistas; las demás se desarrollan en las siguientes unidades.

## 1. Introducción y objetivos

Sistema para centralizar la gestión de las prácticas empresariales de la Facultad de Ingenierías. El problema y la oportunidad están en [vision.md §1](vision.md#1-problema-u-oportunidad) y los objetivos de negocio (OB-01 a OB-05) en [vision.md §2](vision.md#2-objetivos-de-negocio). Los stakeholders están en [vision.md §4](vision.md#4-stakeholders).

## 2. Restricciones

Las restricciones vigentes (RT-01 a RT-04 y RN-01 a RN-05) están en [drivers.md §3](drivers.md#3-restricciones). Cada una se atiende en los ADR indicados en la sección 7.

## 3. Contexto del sistema

El sistema como caja negra, con sus cinco actores y tres sistemas externos (SIA, SSO institucional y correo institucional), está en [contexto.md](contexto.md), con su diagrama C4 nivel 1 en [diagramas/contexto.puml](diagramas/contexto.puml).

## 4. Estrategia de solución

*Pendiente.* Las decisiones de alto nivel se resumirán desde los ADR de la sección 7.

## 5. Vistas

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

*Pendiente.*

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
| [EAC-01](drivers.md#eac-01-mantenibilidad-modificabilidad) | 001, 009 |
| [EAC-02](drivers.md#eac-02-seguridad-acceso-externo-sin-cuenta) | 006, 005, 013 |
| [EAC-03](drivers.md#eac-03-fiabilidad-tolerancia-a-fallos-del-sia) | 007, 008, 013 |
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

- [EAC-01: Mantenibilidad (modificabilidad)](drivers.md#eac-01-mantenibilidad-modificabilidad)
- [EAC-02: Seguridad (acceso externo sin cuenta)](drivers.md#eac-02-seguridad-acceso-externo-sin-cuenta)
- [EAC-03: Fiabilidad (tolerancia a fallos del SIA)](drivers.md#eac-03-fiabilidad-tolerancia-a-fallos-del-sia)

## 9. Riesgos y deuda técnica

*Pendiente.*
