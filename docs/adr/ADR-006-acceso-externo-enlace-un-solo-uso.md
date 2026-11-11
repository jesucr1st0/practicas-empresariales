# ADR-006: Acceso de supervisores externos mediante enlace de un solo uso con vencimiento

## Estado
Aceptado — 2026-11-01

## Contexto
**RN-04** prohíbe exigir cuenta o contraseña a los supervisores de empresa. **EAC-02** exige que el supervisor valide horas y evalúe al estudiante desde un celular con 4G: 90 % en ≤ 5 min, 0 contraseñas, carga ≤ 3 s (p95), expiración a los 30 días y 100 % de accesos registrados. Responde a **PA-02** y soporta **CU-04** y **CU-05** (riesgo **RI-03**, **RI-04**).

## Alternativas consideradas
- **A) Cuenta con usuario y contraseña.** Incumple **RN-04** y la medida de "0 contraseñas" de **EAC-02**.
- **B) Código de un solo uso enviado al correo en cada ingreso.** Más seguro, pero añade un paso y depende del correo en el momento; arriesga la medida de ≤ 5 min.
- **C) Enlace con token aleatorio opaco (≥ 128 bits), guardado como hash en la base de datos, ligado a una práctica y a las acciones permitidas, que se invalida al enviar la evaluación o a los 30 días.** Cumple todas las medidas de **EAC-02**.
- **D) Token firmado autocontenido (JWT).** No requiere consulta, pero no es revocable sin lista adicional y no permite invalidar tras el primer uso.

## Decisión
Se elige **C** porque es la única que cumple **RN-04** y las medidas de **EAC-02** (sin contraseña, ligera para 4G, con expiración y registro de cada acceso en la bitácora de [ADR-005](ADR-005-autorizacion-por-roles-y-bitacora.md)). El formulario se mantiene liviano para cumplir los 3 s en 4G.

## Consecuencias
- **Positivas:** cero contraseñas; enlace revocable e invalidado tras su uso; accesos trazables.
- **Negativas y costos aceptados:** quien posea el enlace puede actuar (por ejemplo, si se reenvía); si el correo del supervisor está comprometido, el enlace también; hay que reemitir enlaces vencidos.
- **Riesgos asumidos:** suplantación por enlace reenviado o filtrado. *Mitigación:* alcance mínimo por enlace, registro de IP y agente, invalidación al primer envío y reemisión controlada por el coordinador.

## Vistas que modifica
- [Contexto](../contexto.md): Supervisor de empresa como persona externa sin cuenta.
- [Lógica](../vistas/01-logica.md): EnlaceAcceso y Supervisor.
- [Procesos](../vistas/02-procesos.md): entrada HTTPS por enlace a la misma aplicación.
- [Desarrollo](../vistas/03-desarrollo.md): Formulario de acceso externo.
- [Física](../vistas/04-fisica.md): Celular del supervisor accede por Internet.

Escenarios que lo evidencian: ESC-04, ESC-05 (ver [escenarios.md](../escenarios.md)).
