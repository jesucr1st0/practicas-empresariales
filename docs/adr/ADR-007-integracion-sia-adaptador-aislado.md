# ADR-007: Acceder al SIA a través de un adaptador aislado (puerto y adaptador)

## Estado
Aceptado — 2026-11-01

## Contexto
**RT-03** obliga a consultar los datos académicos solo por los servicios del SIA, sin conexión directa a su base de datos. **PA-01** pide decidir cómo se integra el sistema y cómo tolera sus fallas; **EAC-03** exige 0 conexiones directas a la base del SIA y verificación ≤ 5 s (p95). **CU-03** (postulación) y las consultas de datos de estudiantes y tutores (CU-11, CU-12) dependen de él.

## Alternativas consideradas
- **A) Conexión directa a la base de datos del SIA.** Descartada: prohibida por **RT-03**.
- **B) Llamar a los servicios del SIA desde cada módulo que los necesite.** Ventaja: sin capa adicional. Desventaja: el manejo de fallas y los cambios del SIA se dispersan por todo el sistema.
- **C) Adaptador aislado: los módulos dependen de una interfaz de consulta académica y solo el adaptador conoce los servicios del SIA.** Ventajas: un único punto para tiempos de espera, errores y cambios; se puede probar con un SIA simulado.
- **D) Copia local de los datos del SIA sincronizada periódicamente.** Ventaja: tolera caídas. Desventaja: datos desactualizados y duplicación de datos personales (**RN-01**); **RT-03** limita el acceso a servicios de consulta.

## Decisión
Se elige **C** porque **RT-03** y **EAC-03** exigen un único punto controlado de acceso con manejo de fallas, y porque aísla al resto del sistema de cambios del SIA (módulo de integración definido en [ADR-001](ADR-001-monolito-modular.md)).

## Consecuencias
- **Positivas:** fallas y cambios del SIA contenidos en un módulo; pruebas con un SIA simulado; cumplimiento verificable de "0 conexiones directas".
- **Negativas y costos aceptados:** una capa adicional que mantener; cada consulta depende de la latencia del SIA (p95 ≤ 5 s); no hay copia local, por lo que sin SIA no hay verificación inmediata (ver [ADR-008](ADR-008-verificacion-asincrona-con-reintentos.md)).
- **Riesgos asumidos:** servicios del SIA mal documentados o modificados sin aviso. *Mitigación:* pruebas de contrato contra el SIA y coordinación con su administrador.

## Vistas que modifica
- [Contexto](../contexto.md): SIA como sistema externo consultado por servicios.
- [Procesos](../vistas/02-procesos.md): conector con espera de 10 s hacia el SIA.
- [Desarrollo](../vistas/03-desarrollo.md): Adaptador SIA y puerto ConsultaAcademica.
- [Física](../vistas/04-fisica.md): conexión desde el Servidor de aplicaciones a los servicios del SIA.

Escenarios que lo evidencian: ESC-03 (ver [escenarios.md](../escenarios.md)).
