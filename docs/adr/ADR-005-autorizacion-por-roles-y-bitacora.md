# ADR-005: Autorización basada en roles con bitácora de accesos

## Estado
Aceptado — 2026-11-01

## Contexto
**RN-01** (Ley 1581 de 2012) exige control por roles y registro de accesos a datos personales. **EAC-02** exige que el 100 % de los accesos por enlace quede registrado. **PA-04** pide trazabilidad y **PA-02** distingue usuarios internos y externos. Un tutor solo debe ver a sus estudiantes (**CU-01**).

## Alternativas consideradas
- **A) Permisos codificados en cada pantalla o servicio.** Ventaja: rápido de construir. Desventaja: difícil de auditar y de cambiar; incumple el espíritu de **RN-01**.
- **B) Control de acceso por roles (Estudiante, Tutor, Coordinador, Administrador, Supervisor externo) con permisos en la base de datos y bitácora de accesos de solo inserción.** Ventajas: auditable y modificable sin tocar la lógica.
- **C) Control por atributos (ABAC).** Ventaja: máxima expresividad. Desventaja: complejidad desproporcionada para cinco roles (**PA-05**).

## Decisión
Se elige **B** porque responde directamente a **RN-01** y a la medida de 100 % de accesos registrados de **EAC-02**. El rol se complementa con una regla de alcance (el tutor solo accede a sus estudiantes asignados). La bitácora registra quién, qué, cuándo y desde dónde, incluidos los accesos por enlace.

## Consecuencias
- **Positivas:** accesos auditables para la Ley 1581; permisos cambiables sin redesplegar.
- **Negativas y costos aceptados:** cada acceso escribe en la bitácora (volumen creciente); el alcance por estudiante añade una regla más que un rol puro.
- **Riesgos asumidos:** la bitácora contiene datos personales (por ejemplo direcciones IP). *Mitigación:* aplicarle la política de retención de [ADR-011](ADR-011-retencion-documental-y-datos-personales.md).

## Vistas que modifica
- [Lógica](../vistas/01-logica.md): RegistroAcceso (bitácora de solo inserción).
- [Procesos](../vistas/02-procesos.md): roles y bitácora en la Base de datos relacional.
- [Desarrollo](../vistas/03-desarrollo.md): Módulo Identidad y accesos y regla de alcance del tutor.

Escenarios que lo evidencian: ESC-01, ESC-04, ESC-05 (ver [escenarios.md](../escenarios.md)).
