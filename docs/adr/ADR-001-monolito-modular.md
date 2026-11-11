# ADR-001: Construir el sistema como una aplicación única y modular (monolito modular)

## Estado
Aceptado — 2026-11-01

## Contexto
La carga es moderada: ~250 prácticas activas, ~500 estudiantes y 50 tutores al año (**PA-05**, [vision.md](../vision.md#1-problema-u-oportunidad)). El equipo es de máximo cuatro personas. **EAC-01** exige que un cambio de reglas toque **un solo módulo**, **RT-01** y **RT-04** obligan a desplegar en infraestructura y tecnologías institucionales, y **RN-05** prohíbe costos recurrentes de licencias.

## Alternativas consideradas
- **A) Microservicios por capacidad.** Ventaja: despliegue y escalado independientes. Desventaja: exige operar ~8 servicios, orquestación y monitoreo en una infraestructura institucional limitada; desproporcionado para 250 prácticas activas y 4 desarrolladores (**PA-05**).
- **B) Monolito en capas sin límites de módulo.** Ventaja: el más simple de construir. Desventaja: la lógica de reglas se dispersa por capas y un cambio como el de **EAC-01** tocaría varios módulos.
- **C) Monolito modular.** Una sola aplicación y un solo despliegue, con módulos de límites explícitos: postulaciones, prácticas, tutores y asignación, horas, evaluaciones, actas, reglas, integración con el SIA, identidad y accesos, notificaciones.

## Decisión
Se elige **C** porque **EAC-01** pide localizar el cambio en un módulo y **PA-05** pide una solución proporcional a la carga; además simplifica el despliegue exigido por **RT-01** y **RT-04**.

## Consecuencias
- **Positivas:** un solo artefacto que operar y monitorear; cambios de reglas localizados; costo de infraestructura mínimo (**RN-05**).
- **Negativas y costos aceptados:** los módulos no escalan de forma independiente; cualquier cambio exige redesplegar toda la aplicación (el servicio detenido debe ser ≤ 5 min, **EAC-01**); requiere disciplina para respetar los límites entre módulos.
- **Riesgos asumidos:** erosión de los límites por acoplamiento a través de la base de datos compartida. *Mitigación:* revisión en Pull Request y pruebas automáticas de dependencias entre módulos. Si la carga crece de forma sostenida, se evaluará separar módulos mediante un ADR nuevo.

## Vistas que modifica
- [Procesos](../vistas/02-procesos.md): un solo contenedor, la Aplicación de prácticas.
- [Desarrollo](../vistas/03-desarrollo.md): módulos con límites explícitos y regla de dependencia.
- [Física](../vistas/04-fisica.md): un único artefacto en un solo Servidor de aplicaciones.

Escenarios que lo evidencian: ESC-07 (ver [escenarios.md](../escenarios.md)).
