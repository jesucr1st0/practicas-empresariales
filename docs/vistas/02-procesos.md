# Vista de procesos: diagrama de contenedores

Qué se ejecuta por separado, cómo se comunica y cómo se reparte el trabajo en ejecución (C4 nivel 2).

**Stakeholders y preocupaciones que atiende:** Arquitecto del sistema (¿cómo se cumplen EAC-01, EAC-02, EAC-03?), Administrador de infraestructura y TI (¿qué se ejecuta y qué hay que operar?), Responsable de soporte (¿dónde se detuvo una operación?), Administrador del SIA (¿por qué canal se consulta?).

## 1. Presentación principal

Diagrama: [02-procesos.puml](../diagramas/02-procesos.puml) (C4 nivel 2). En este contexto un contenedor no es Docker: es cualquier cosa que se ejecuta o guarda datos por separado.

Cómo se lee: el sistema son **tres contenedores**. Toda la lógica corre en un único contenedor, la Aplicación de prácticas (ADR-001). Los reintentos y recordatorios son una tarea programada **dentro** de ese contenedor y la base de datos funciona como cola (ADR-008). **No hay broker de mensajes**: se descartó por operar un componente adicional fuera del catálogo y de RN-05.

## 2. Catálogo de elementos

| Elemento | Responsabilidad | Tecnología | Se comunica con |
|----------|-----------------|------------|-----------------|
| Aplicación de prácticas | Interfaz web, reglas del proceso, acceso por enlace del supervisor, tareas programadas (reintentos cada 15 min durante 24 h, recordatorios, alertas) | Monolito modular; lenguaje y framework **por confirmar** contra el catálogo (RT-04) | Navegadores (HTTPS), Base de datos relacional (SQL), Almacenamiento de archivos, SIA, SSO institucional, Servidor de correo (SMTP) |
| Base de datos relacional | Prácticas, horas, evaluaciones, reglas versionadas, bitácora de accesos, hash de enlaces y verificaciones pendientes | PostgreSQL (candidato, ADR-002); motor **por confirmar** (RT-04) | Aplicación de prácticas (SQL) |
| Almacenamiento de archivos | Actas finales en PDF y evidencias, con retención parametrizable y baja lógica | Almacenamiento institucional (ADR-011) | Aplicación de prácticas (lee y escribe) |
| SIA *(externo)* | Datos académicos | Servicios del SIA; protocolo **por confirmar** | Aplicación de prácticas |
| SSO institucional *(externo)* | Autenticación de usuarios internos | OIDC, SAML o CAS, **por confirmar** | Aplicación de prácticas |
| Servidor de correo institucional *(externo)* | Entrega de notificaciones | SMTP | Aplicación de prácticas |

**Conectores relevantes** (en esta vista el conector es tan importante como el componente):

- **Aplicación → SIA:** síncrono con espera máxima de 10 s; si falla, la postulación queda «pendiente» y se reintenta. Es el conector que cumple EAC-03.
- **Navegador del supervisor → Aplicación:** HTTPS por Internet, formulario liviano para cargar en ≤ 3 s (p95) en 4G (EAC-02).
- **Aplicación → Base de datos:** SQL, también como cola de verificaciones pendientes; las operaciones deben ser idempotentes.

## 3. Justificación

| Driver | Cómo lo atiende esta vista | ADR |
|--------|----------------------------|-----|
| EAC-01 | Un solo contenedor y un solo artefacto: el redespliegue detiene el servicio ≤ 5 min | ADR-001 |
| EAC-02 | Acceso externo por HTTPS al mismo contenedor, sin cuentas; accesos registrados en la base de datos | ADR-006, ADR-005 |
| EAC-03 / PA-01 | Conector síncrono con tiempo de espera hacia el SIA, tarea programada y cola en base de datos | ADR-007, ADR-008 |
| RT-02 / PA-02 | SSO para internos y enlace para externos son dos entradas al mismo contenedor | ADR-004, ADR-006 |
| RT-03 | Solo la Aplicación de prácticas habla con el SIA y solo por sus servicios | ADR-007 |
| RT-04 / RN-05 | Sin broker ni servicios externos de pago; el motor se elige del catálogo | ADR-001, ADR-002, ADR-008 |
| PA-04 / RN-02 | PDF en almacenamiento propio, metadatos y huella en la base de datos | ADR-010, ADR-011 |
| PA-05 | Tres contenedores en vez de ~8 servicios: proporcional a ~250 prácticas activas y 4 desarrolladores | ADR-001 |

## 4. Comportamiento

Todos los escenarios recorren esta vista. Los más reveladores:

- [ESC-03 Realizar postulación](../diagramas/secuencias/cu03-realizar-postulacion.puml): el conector hacia el SIA y la tarea programada (alt, loop, break, opt).
- [ESC-04](../diagramas/secuencias/cu04-seguimiento-horas.puml) y [ESC-05](../diagramas/secuencias/cu05-evaluar-estudiante.puml): el acceso del supervisor por enlace.
- [ESC-06 Generar acta](../diagramas/secuencias/cu06-generar-acta.puml): escritura en el Almacenamiento de archivos y en la base de datos.

## 5. Vistas relacionadas

- **Contexto:** de dónde vienen los actores y sistemas externos ([contexto.md](../contexto.md)).
- **Física:** en qué nodo corre cada contenedor ([04-fisica.md](04-fisica.md)).
- **Desarrollo:** cómo se organiza por dentro la Aplicación de prácticas ([03-desarrollo.md](03-desarrollo.md)).
- **Lógica:** qué entidades guarda la base de datos ([01-logica.md](01-logica.md)).
