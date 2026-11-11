# ADR-002: Usar una base de datos relacional única para la persistencia

## Estado
Aceptado — 2026-11-01 *(el motor concreto debe confirmarse contra el catálogo institucional)*

## Contexto
El sistema debe garantizar integridad y trazabilidad de prácticas, horas, evaluaciones y actas (**PA-04**), versionar reglas por programa (**EAC-01**) y registrar accesos (**RN-01**). Solo pueden usarse tecnologías del catálogo (**RT-04**) y sin licencias de pago recurrente (**RN-05**). **RT-03** prohíbe usar la base de datos del SIA como almacén.

## Alternativas consideradas
- **A) Base de datos relacional de código abierto** (por ejemplo PostgreSQL o MySQL). Ventajas: transacciones, integridad referencial, consultas para el tablero de estado, sin licencia. Desventaja: esquema rígido; los cambios requieren migraciones.
- **B) Base de datos documental (NoSQL).** Ventaja: esquema flexible. Desventajas: integridad referencial débil entre práctica, tutor, horas y acta; menos adecuada para consultas de seguimiento; posible ausencia en el catálogo (**RT-04**).
- **C) Reutilizar la base de datos del SIA.** Descartada: incumple **RT-03**.

## Decisión
Se elige **A** porque la integridad transaccional y la trazabilidad (**PA-04**) pesan más que la flexibilidad de esquema, y porque cumple **RN-05**. El motor se selecciona entre los del catálogo institucional (**RT-04**); el candidato inicial es PostgreSQL.

## Consecuencias
- **Positivas:** integridad entre entidades; historial y auditoría consultables con SQL; costo de licencia nulo.
- **Negativas y costos aceptados:** cada cambio de modelo exige migraciones controladas; las copias de seguridad dependen del Área de sistemas.
- **Riesgos asumidos:** que el motor elegido no esté en el catálogo. *Mitigación:* validarlo con el Área de sistemas antes de construir; si cambia, se registra un ADR que reemplace a este.

## Vistas que modifica
- [Procesos](../vistas/02-procesos.md): contenedor Base de datos relacional (SQL).
- [Desarrollo](../vistas/03-desarrollo.md): Adaptador de persistencia.
- [Física](../vistas/04-fisica.md): Servidor de base de datos.

Escenarios que lo evidencian: ESC-01, ESC-02, ESC-06 (ver [escenarios.md](../escenarios.md)).
