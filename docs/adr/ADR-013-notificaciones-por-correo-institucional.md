# ADR-013: Enviar las notificaciones por correo electrónico institucional

## Estado
Aceptado — 2026-11-01

## Contexto
Los supervisores reciben el enlace de **EAC-02** por un canal externo al sistema (**CU-04**, **CU-05**) y no tienen cuenta (**RN-04**); **EAC-03** exige avisar al estudiante en ≤ 1 min; el riesgo **RI-03** de la visión requiere recordatorios a las empresas. **RN-05** excluye servicios de pago recurrente y **RT-04** limita las tecnologías.

## Alternativas consideradas
- **A) Correo electrónico mediante el servidor institucional.** Llega a estudiantes, tutores y supervisores; sin costo adicional.
- **B) Servicio externo de mensajería (SMS, WhatsApp o correo transaccional de pago).** Mayor entregabilidad, pero genera costo recurrente (**RN-05**) y comparte datos personales con terceros.
- **C) Solo notificaciones dentro de la aplicación.** Descartada: los supervisores no tienen cuenta y no podrían recibir el enlace.

## Decisión
Se elige **A**, complementada con el tablero de estado dentro de la aplicación para usuarios internos. Cada envío se registra, incluidos los fallidos.

## Consecuencias
- **Positivas:** llega a usuarios sin cuenta; cumple **RN-05**; los recordatorios se programan con el mismo mecanismo de [ADR-008](ADR-008-verificacion-asincrona-con-reintentos.md).
- **Negativas y costos aceptados:** la entrega no está garantizada (spam, buzones llenos); se depende de los límites del servidor institucional.
- **Riesgos asumidos:** correos de supervisores marcados como spam. *Mitigación:* registro de envíos fallidos y opción del coordinador de reenviar el enlace.

## Vistas que modifica
- [Contexto](../contexto.md): Servidor de correo institucional como sistema externo.
- [Procesos](../vistas/02-procesos.md): conector SMTP.
- [Desarrollo](../vistas/03-desarrollo.md): Módulo Notificaciones y Adaptador de correo.
- [Física](../vistas/04-fisica.md): correo entre los servicios institucionales existentes.

Escenarios que lo evidencian: ESC-03, ESC-04, ESC-05 (ver [escenarios.md](../escenarios.md)).
