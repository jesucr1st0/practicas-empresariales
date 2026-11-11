# ADR-010: Generar el acta final desde la plantilla oficial y conservarla inmutable con huella de integridad

## Estado
Aceptado — 2026-11-01

## Contexto
**CU-06** genera el acta final con la plantilla oficial del Consejo de Facultad (**RN-03**); el acta debe conservarse según la Ley 594 (**RN-02**) y ser íntegra y trazable (**PA-04**). **OB-05** pide generarla dentro de los 5 días hábiles siguientes a la finalización. La firma electrónica externa está fuera del alcance (vision.md §3, "No incluye").

## Alternativas consideradas
- **A) Generar el acta bajo demanda cada vez desde los datos actuales.** Ventaja: nada que almacenar. Desventaja: si los datos cambian, el acta cambia; no hay documento oficial estable (**PA-04**).
- **B) Generar el acta una vez desde la plantilla oficial, almacenar el PDF como inmutable con huella SHA-256 y registrar los datos de origen (versión de regla, horas, evaluación).** Integridad verificable y trazabilidad.
- **C) Firma electrónica con un servicio externo.** Descartada: fuera del alcance de la visión y con posible costo recurrente (**RN-05**).

## Decisión
Se elige **B** porque **PA-04** y **RN-02** exigen un documento estable y verificable, y **RN-03** fija la plantilla. Una corrección genera un acta nueva que reemplaza a la anterior y la marca como anulada; nunca se edita. **CU-07** (exportar) descarga ese mismo PDF.

## Consecuencias
- **Positivas:** acta íntegra y verificable; trazabilidad hasta la versión de regla y las evidencias.
- **Negativas y costos aceptados:** una corrección requiere un acta nueva; la plantilla oficial debe versionarse; la huella SHA-256 garantiza integridad pero **no equivale a firma digital**.
- **Riesgos asumidos:** que el Consejo exija después firma digital con validez legal. *Mitigación:* registrar un ADR nuevo que reemplace a este.

## Vistas que modifica
- [Lógica](../vistas/01-logica.md): ActaFinal inmutable con huella y estado.
- [Procesos](../vistas/02-procesos.md): PDF en el Almacenamiento de archivos y metadatos en la base de datos.
- [Desarrollo](../vistas/03-desarrollo.md): Módulo Actas.
- [Física](../vistas/04-fisica.md): nodo de Almacenamiento de archivos.

Escenarios que lo evidencian: ESC-06 (ver [escenarios.md](../escenarios.md)).
