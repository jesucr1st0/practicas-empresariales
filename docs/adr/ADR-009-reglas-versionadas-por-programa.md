# ADR-009: Representar las reglas de práctica como versiones inmutables con vigencia por programa

## Estado
Aceptado — 2026-11-01

## Contexto
**PA-03** exige reglas variables por programa y periodo sin alterar las prácticas en curso. **EAC-01**: subir las horas mínimas de 480 a 540 debe hacerse en ≤ 8 horas-persona, en un solo módulo, con 0 prácticas en curso alteradas y ≤ 5 min de servicio detenido. Las reglas afectan **CU-02** (registrar práctica) y **CU-06** (acta final).

## Alternativas consideradas
- **A) Reglas en el código con condicionales por programa y periodo.** Ventaja: sin modelo adicional. Desventaja: cada cambio exige modificar y desplegar código y se dispersa en varios lugares (incumple "1 solo módulo").
- **B) Tabla de configuración editable (se sobrescribe el valor).** Ventaja: cambio sin código. Desventaja: modifica retroactivamente las prácticas en curso: incumple "0 prácticas alteradas".
- **C) Reglas versionadas e inmutables, con fecha de vigencia por programa; cada práctica referencia la versión vigente al registrarse.** Cumple todas las medidas de **EAC-01**.

## Decisión
Se elige **C** porque es la única que permite que las prácticas en curso conserven la regla anterior y las nuevas usen la nueva (**EAC-01**, **PA-03**). Los valores parametrizables (como horas mínimas) son datos; una regla estructuralmente nueva requiere código, siempre dentro del módulo de reglas ([ADR-001](ADR-001-monolito-modular.md)).

## Consecuencias
- **Positivas:** cambio de valores sin tocar prácticas en curso; historial completo de reglas aplicadas a cada práctica (apoya **PA-04**).
- **Negativas y costos aceptados:** toda consulta debe resolver la versión de la regla de la práctica; más casos de prueba de regresión (varias versiones conviven); el modelo de datos es más complejo.
- **Riesgos asumidos:** que el Consejo decida aplicar una regla nueva a prácticas ya en curso. *Mitigación:* procedimiento explícito de migración controlada, nunca automática.

## Vistas que modifica
- [Lógica](../vistas/01-logica.md): ReglaPrograma versionada y referencia fija de Practica.
- [Desarrollo](../vistas/03-desarrollo.md): Módulo Reglas.

Escenarios que lo evidencian: ESC-02, ESC-06, ESC-07 (ver [escenarios.md](../escenarios.md)).
