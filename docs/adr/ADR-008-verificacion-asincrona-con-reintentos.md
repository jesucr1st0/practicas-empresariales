# ADR-008: Verificar las postulaciones de forma asíncrona con estado "pendiente" y reintentos

## Estado
Aceptado — 2026-11-01

## Contexto
**EAC-03**: si el SIA está caído o lento al postularse, el sistema debe guardar la postulación como "pendiente", avisar en ≤ 1 min tras 10 s sin respuesta, reintentar cada 15 min durante 24 h y **no perder ninguna postulación**. **PA-01** pide tolerancia a fallos del SIA; **CU-03** es el caso de uso afectado. **RN-05** y **RT-04** limitan la infraestructura adicional.

## Alternativas consideradas
- **A) Verificación sincrónica con tiempo de espera y error al estudiante.** Simple, pero si el SIA falla la postulación se pierde: incumple "0 postulaciones perdidas" de **EAC-03**.
- **B) Cola de mensajes con un broker externo.** Cumple el escenario, pero agrega un componente que operar y que puede no estar en el catálogo (**RT-04**) ni encajar con **RN-05**.
- **C) Guardar la postulación primero con estado "pendiente de verificación", intentar la verificación (máximo 10 s) y, si falla, reintentarla con una tarea programada dentro de la misma aplicación, con la base de datos como cola.** Cumple todas las medidas sin infraestructura adicional.

## Decisión
Se elige **C** porque garantiza 0 postulaciones perdidas (**EAC-03**) sin añadir componentes fuera del catálogo (**RT-04**, **RN-05**). Tras 24 h de reintentos sin éxito, la postulación pasa a revisión manual del coordinador; nunca se descarta. El aviso al estudiante se envía según [ADR-013](ADR-013-notificaciones-por-correo-institucional.md).

## Consecuencias
- **Positivas:** ninguna postulación se pierde; sin broker que operar; la verificación se retoma sola cuando el SIA se recupera.
- **Negativas y costos aceptados:** el estudiante ve estados intermedios ("pendiente") que debe comunicarse con claridad; la base de datos como cola limita el caudal (suficiente para ~250 prácticas activas); los reintentos exigen operaciones idempotentes.
- **Riesgos asumidos:** acumulación de postulaciones pendientes si el SIA permanece caído varios días. *Mitigación:* alerta al coordinador de postulaciones pendientes por más de 24 h.

## Vistas que modifica
- [Lógica](../vistas/01-logica.md): estados pendiente de verificación y revisión manual de Postulacion.
- [Procesos](../vistas/02-procesos.md): base de datos como cola y tarea programada dentro de la aplicación.
- [Desarrollo](../vistas/03-desarrollo.md): Planificador de tareas y Módulo Postulaciones.

Escenarios que lo evidencian: ESC-03 (ver [escenarios.md](../escenarios.md)).
