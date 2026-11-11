# Contexto del sistema

Marco de las cuatro vistas de 4+1 (no es una vista). Responde: **¿qué hay afuera del sistema y cómo se comunica con él?**
Parte de [vision.md](vision.md) y [drivers.md](drivers.md); decisiones en [arquitectura.md §7](arquitectura.md#7-decisiones-de-diseño).

**Stakeholders que atiende:** Decano o representante de la Facultad y Coordinador de prácticas (¿con qué sistemas se integra y quién lo usa?), Responsable de seguridad informática (¿quién accede y por qué canal?), Administrador del SIA (¿qué datos se consultan y por qué canal?).

## 1. Presentación principal

Diagrama: [contexto.puml](diagramas/contexto.puml) (C4 nivel 1). El sistema es una **caja negra**: aquí no aparece ningún contenedor, módulo ni tecnología interna.

Leyenda: azul = persona interna; gris oscuro = persona externa (sin cuenta); gris = sistema externo. Cada flecha lleva un verbo y, si aplica, el protocolo.

## 2. Catálogo de elementos

| Elemento | Tipo | Rol o responsabilidad | Interacción con el sistema |
|----------|------|-----------------------|----------------------------|
| Estudiante | Persona interna | Se postula, consulta el estado de su práctica y registra horas | Interfaz web (HTTPS), con SSO |
| Tutor académico | Persona interna | Da seguimiento y valida horas de **sus** estudiantes asignados | Interfaz web (HTTPS), con SSO |
| Coordinador de prácticas | Persona interna | Registra prácticas y empresas, asigna tutores, genera y exporta actas | Interfaz web (HTTPS), con SSO |
| Administrador | Persona interna | Gestiona usuarios, roles y datos maestros (estudiantes, tutores) | Interfaz web (HTTPS), con SSO |
| Supervisor de empresa | Persona externa | Valida horas y evalúa al estudiante **sin cuenta ni contraseña** (RN-04) | Enlace de un solo uso (HTTPS, celular 4G) |
| Sistema de Gestión de Prácticas Empresariales | Sistema en alcance | Centraliza postulación, asignación de tutores, horas, evaluación y acta final | Con todos los demás elementos |
| SIA | Sistema externo | Fuente de datos académicos de estudiantes y tutores; administrado por el Área de sistemas | Solo por sus servicios de consulta; **0 conexiones a su base de datos** (RT-03) |
| SSO institucional | Sistema externo | Autentica a los usuarios internos; el sistema no guarda sus contraseñas (RT-02) | Protocolo por confirmar: OIDC, SAML o CAS |
| Servidor de correo institucional | Sistema externo | Entrega avisos, recordatorios y enlaces a estudiantes, tutores y supervisores | SMTP |

**Lo que deliberadamente no aparece** (vision.md §3, «No incluye»): plataformas de firma electrónica, pasarelas de pago, sistemas de contratación o nómina, bolsas de vacantes. El acta se protege con huella de integridad, no con firma digital (ADR-010).

## 3. Justificación

- **CU-01 a CU-06 (primarios)** definen los cinco actores y las integraciones críticas: SIA (CU-03), correo (CU-04, CU-05) y supervisor externo (CU-04, CU-05).
- **RT-02 / ADR-004:** la autenticación interna se delega al SSO; por eso es un sistema externo y no un componente propio.
- **RT-03 / ADR-007 / PA-01:** el SIA se consulta solo por sus servicios. Para el Administrador del SIA: se consultan datos académicos del estudiante (CU-03, CU-12) y datos del tutor (CU-11); la lista exacta de servicios y el protocolo siguen **por confirmar**.
- **RN-04 / PA-02 / ADR-006:** el supervisor no tiene cuenta, por eso es una persona externa con un acceso distinto al del SSO.
- **ADR-013 / RN-05:** el correo institucional es el único canal de notificación; no hay servicios externos de pago.
- **RN-01 / RT-01:** el sistema y sus datos permanecen en la infraestructura de la Universidad (se verifica en la [vista física](vistas/04-fisica.md)).

## 4. Comportamiento

Aquí empiezan los escenarios del +1 (tabla en [drivers.md §6](drivers.md#6-escenarios)):

| Escenario | Sistemas y actores externos que toca |
|-----------|--------------------------------------|
| [ESC-01 Asignar tutor](diagramas/secuencias/cu01-asignar-tutor.puml) | Coordinador, SSO |
| [ESC-02 Registrar práctica](diagramas/secuencias/cu02-registrar-practica.puml) | Coordinador |
| [ESC-03 Realizar postulación](diagramas/secuencias/cu03-realizar-postulacion.puml) | Estudiante, SIA, correo, Coordinador |
| [ESC-04 Seguimiento de horas](diagramas/secuencias/cu04-seguimiento-horas.puml) | Estudiante, Tutor, Supervisor, correo |
| [ESC-05 Evaluar al estudiante](diagramas/secuencias/cu05-evaluar-estudiante.puml) | Supervisor, correo |
| [ESC-06 Generar acta final](diagramas/secuencias/cu06-generar-acta.puml) | Coordinador |
| [ESC-07 Cambio de horas mínimas](diagramas/secuencias/eac01-cambio-horas-minimas.puml) | Desarrollador, Coordinador |

## 5. Vistas relacionadas

- **Procesos:** qué contenedor habla con cada sistema externo ([02-procesos.md](vistas/02-procesos.md)).
- **Física:** por qué red sale cada conexión ([04-fisica.md](vistas/04-fisica.md)).
- **Lógica:** qué conceptos del negocio manejan los actores ([01-logica.md](vistas/01-logica.md)).

## Anexo: nombres canónicos (idénticos en todas las vistas y escenarios)

| Categoría | Nombres |
|-----------|---------|
| Personas | Estudiante · Tutor académico · Coordinador de prácticas · Administrador · Supervisor de empresa |
| Sistemas externos | SIA · SSO institucional · Servidor de correo institucional |
| Contenedores | Aplicación de prácticas · Base de datos relacional · Almacenamiento de archivos |
| Adaptadores de entrada | Interfaz web interna · Formulario de acceso externo · Planificador de tareas |
| Módulos | Módulo Identidad y accesos · Módulo Reglas · Módulo Postulaciones · Módulo Prácticas · Módulo Tutores y asignación · Módulo Horas · Módulo Evaluaciones · Módulo Actas · Módulo Notificaciones |
| Adaptadores de salida | Adaptador SIA · Adaptador de persistencia · Adaptador de archivos · Adaptador SSO · Adaptador de correo |
| Puertos | ConsultaAcademica · repositorios · AlmacenArchivos · ProveedorIdentidad · EnvioCorreo |
| Entidades del dominio | Programa · ReglaPrograma · Estudiante · Tutor · Empresa · Supervisor · Postulacion · Practica · AsignacionTutor · RegistroHoras · Evaluacion · ActaFinal · EnlaceAcceso · RegistroAcceso |
| Estados de Postulacion | pendiente de verificación · verificada · rechazada · revisión manual |
| Estados de Practica | registrada · en curso · finalizada · cerrada (con acta vigente) |
