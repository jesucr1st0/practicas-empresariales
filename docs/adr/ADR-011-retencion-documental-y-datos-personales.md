# ADR-011: Conservar actas y evidencias en almacenamiento institucional con retención parametrizable

## Estado
Propuesto — 2026-11-01 *(pendiente confirmar los plazos con la Tabla de Retención Documental de la Universidad)*

## Contexto
**RN-02** (Ley 594 de 2000) exige retener actas y evidencias; **RN-01** (Ley 1581 de 2012) limita el tratamiento de datos personales; **PA-04** pide retención e integridad; **RT-01** obliga a que los datos permanezcan en infraestructura institucional. Aplica a actas (**CU-06**), evidencias y a la bitácora de [ADR-005](ADR-005-autorizacion-por-roles-y-bitacora.md).

## Alternativas consideradas
- **A) Guardar los archivos como campos binarios en la base de datos.** Ventaja: un solo almacén y respaldo. Desventaja: crece la base de datos y se complica su respaldo y migración.
- **B) Almacenamiento de archivos institucional con metadatos en la base de datos, política de retención parametrizable y baja lógica.** Ventajas: cumple **RT-01**, separa archivos de datos y permite aplicar plazos por tipo de documento.
- **C) Servicio de almacenamiento en la nube externa.** Descartada: incumple **RT-01** y puede generar costo recurrente (**RN-05**).

## Decisión
Se elige **B**. No hay borrado físico antes del vencimiento del plazo de retención; el plazo por tipo de documento se toma de la Tabla de Retención Documental institucional.

## Consecuencias
- **Positivas:** cumplimiento de Ley 594; archivos desacoplados de la base de datos; plazos ajustables sin cambiar código.
- **Negativas y costos aceptados:** hay que coordinar los respaldos de archivos y de base de datos; el derecho de supresión (Ley 1581) puede chocar con la retención legal y requiere un procedimiento definido.
- **Riesgos asumidos:** plazos de retención no confirmados. *Mitigación:* por eso el ADR queda "Propuesto" hasta validarlo con el archivo institucional.

## Vistas que modifica
- [Lógica](../vistas/01-logica.md): retención sobre ActaFinal y RegistroAcceso.
- [Procesos](../vistas/02-procesos.md): contenedor Almacenamiento de archivos.
- [Desarrollo](../vistas/03-desarrollo.md): Adaptador de archivos y puerto AlmacenArchivos.
- [Física](../vistas/04-fisica.md): Almacenamiento de archivos institucional.

Escenarios que lo evidencian: ESC-06 (ver [escenarios.md](../escenarios.md)).
