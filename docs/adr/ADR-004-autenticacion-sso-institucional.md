# ADR-004: Autenticar a los usuarios internos con el inicio de sesión único institucional

## Estado
Aceptado — 2026-11-01 *(decisión impuesta por restricción)*

## Contexto
**RT-02** exige que los usuarios internos (estudiantes, tutores, coordinador, administradores) inicien sesión con el inicio de sesión único institucional. **PA-02** plantea además un segundo acceso, para externos, resuelto en [ADR-006](ADR-006-acceso-externo-enlace-un-solo-uso.md). **RI-04** (acceso no autorizado) hace crítica la gestión de credenciales.

## Alternativas consideradas
- **A) Cuentas propias con usuario y contraseña.** Ventaja: independencia del SSO. Desventajas: incumple **RT-02**, duplica identidades y obliga a custodiar contraseñas (superficie de **RI-04**).
- **B) SSO institucional.** Cumple **RT-02**; las altas y bajas se gestionan una sola vez en la institución.
- **C) Proveedor de identidad externo (p. ej. cuentas de Google).** Descartado: no es el mecanismo institucional (**RT-02**) y puede implicar dependencias de terceros (**RN-05**).

## Decisión
Se elige **B**. La decisión **viene impuesta por RT-02**. El sistema no almacena contraseñas de usuarios internos; el protocolo concreto (OIDC, SAML, CAS) y los atributos de rol entregados se confirman con el Administrador del SIA.

## Consecuencias
- **Positivas:** sin contraseñas que custodiar; desvinculación centralizada; experiencia de acceso familiar para la comunidad.
- **Negativas y costos aceptados:** si el SSO cae, nadie interno puede ingresar; no sirve para supervisores externos (requieren ADR-006); el desarrollo y las pruebas necesitan un simulador del proveedor de identidad.
- **Riesgos asumidos:** que el SSO no entregue el rol del usuario. *Mitigación:* los roles se administran dentro del sistema (ver [ADR-005](ADR-005-autorizacion-por-roles-y-bitacora.md)).

## Vistas que modifica
- [Contexto](../contexto.md): SSO institucional como sistema externo.
- [Procesos](../vistas/02-procesos.md): conector hacia el SSO.
- [Desarrollo](../vistas/03-desarrollo.md): Adaptador SSO y puerto ProveedorIdentidad.
- [Física](../vistas/04-fisica.md): SSO entre los servicios institucionales existentes.

Escenarios que lo evidencian: ESC-01 (ver [escenarios.md](../escenarios.md)).
