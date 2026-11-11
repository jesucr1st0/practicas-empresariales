# Escenarios del +1: recorrido de validación

Los escenarios no agregan estructura nueva: recorren las cuatro vistas para comprobar que funcionan juntas. La tabla de escenarios está en [drivers.md §6](drivers.md#6-escenarios); cada fila tiene su diagrama de secuencia arquitectónico en [diagramas/secuencias/](diagramas/secuencias/).

Los diagramas se escribieron con el método de cinco pasos: (1) elegir un CU primario o EAC; (2) copiar los participantes de la vista de procesos y de desarrollo con su mismo nombre; (3) flujo principal sin fallas, con verbo y protocolo; (4) flujos alternos con `alt`, `opt`, `loop`, `par` o `break` y su condición de guarda; (5) verificar que se ve la decisión del ADR y que se cumple el EAC.

Nota de lectura: en las secuencias se omite el **Adaptador de persistencia** y los módulos aparecen escribiendo directo en la «Base de datos relacional» (SQL), para mantener los diagramas legibles; el recorrido completo está en la vista de desarrollo.

## Recorrido de validación

| Escenario | Contexto (actores y externos) | Lógica (entidades) | Procesos (contenedores y conectores) | Desarrollo (componentes) | Física (nodos) |
|-----------|-------------------------------|--------------------|--------------------------------------|--------------------------|----------------|
| ESC-01 Asignar tutor | Coordinador, SSO institucional | Practica, AsignacionTutor, Tutor, ReglaPrograma | Aplicación de prácticas → Base de datos (SQL); Aplicación → SSO | Interfaz web interna, Identidad y accesos, Tutores y asignación, Prácticas, Reglas, Adaptador SSO | Servidor de aplicaciones, Servidor de base de datos |
| ESC-02 Registrar práctica | Coordinador | Practica, ReglaPrograma, Postulacion, Empresa, Supervisor | Aplicación → Base de datos (SQL) | Interfaz web interna, Prácticas, Postulaciones, Reglas | Servidor de aplicaciones, Servidor de base de datos |
| ESC-03 Realizar postulación | Estudiante, SIA, Servidor de correo institucional, Coordinador | Postulacion (estados), Estudiante | Aplicación → SIA (espera 10 s); Aplicación → correo (SMTP); cola en base de datos | Interfaz web interna, Postulaciones, Adaptador SIA, Notificaciones, Adaptador de correo, Planificador de tareas | Servidor de aplicaciones → servicios institucionales (SIA, correo), Servidor de base de datos |
| ESC-04 Seguimiento de horas | Estudiante, Tutor, Supervisor, correo | RegistroHoras, EnlaceAcceso, RegistroAcceso, Supervisor | Navegador del supervisor → Aplicación (HTTPS, 4G); Aplicación → correo | Interfaz web interna, Formulario de acceso externo, Horas, Identidad y accesos, Notificaciones | Celular del supervisor (Internet), Servidor de aplicaciones, Servidor de base de datos |
| ESC-05 Evaluar al estudiante | Supervisor, correo | Evaluacion, EnlaceAcceso, RegistroAcceso, Practica | Navegador del supervisor → Aplicación (HTTPS, 4G); recordatorios por SMTP | Planificador de tareas, Formulario de acceso externo, Evaluaciones, Identidad y accesos, Prácticas, Notificaciones | Celular del supervisor, Servidor de aplicaciones, Servidor de base de datos |
| ESC-06 Generar acta final | Coordinador | ActaFinal, Practica, ReglaPrograma, RegistroHoras, Evaluacion | Aplicación → Almacenamiento de archivos; Aplicación → Base de datos (SQL) | Interfaz web interna, Actas, Prácticas, Horas, Evaluaciones, Reglas, Adaptador de archivos | Servidor de aplicaciones, Almacenamiento de archivos institucional, Servidor de base de datos |
| ESC-07 Cambio de horas mínimas | Desarrollador, Coordinador | ReglaPrograma (v1 y v2), Practica | Aplicación de prácticas (único artefacto), Base de datos | Módulo Reglas, Módulo Prácticas | Servidor de aplicaciones (redespliegue ≤ 5 min) |

**Cobertura:** cada vista es recorrida por al menos tres escenarios (Contexto 7, Lógica 7, Procesos 7, Desarrollo 7, Física 7); cada EAC aparece en al menos un escenario; todo escenario tiene un driver detrás. Ningún escenario obligó a crear una vista nueva.

## Decisiones y puntos abiertos que dejó el recorrido

1. **Alcance del tutor sin ciclos.** Para que «el tutor solo ve a sus estudiantes» (ADR-005) no obligue a Prácticas a depender de Tutores y asignación, la vista de desarrollo registra el *tutor vigente* en Prácticas, actualizado desde Tutores por medio de Prácticas (ESC-01).
2. **Momento de emisión del enlace al supervisor.** Los ADR fijan cómo es el enlace (ADR-006) pero no cuándo se emite. Los escenarios suponen que se emite al solicitar la validación de horas, y que el coordinador puede reemitirlo. **Por confirmar con el coordinador (riesgo RI-05).**
3. **Vigencia de 30 días frente a prácticas largas.** Con un enlace de 30 días e invalidación al enviar la evaluación, las validaciones de horas deben ocurrir dentro de esa ventana o requerir reemisión. Conviene decidir si se emite un enlace por ciclo de seguimiento.
4. **Sin broker.** Los ejemplos de clase usan un broker de mensajes; aquí el ADR-008 lo descarta, por lo que la «cola» es la base de datos y el reintento lo hace el Planificador de tareas dentro de la misma aplicación.
5. **Tecnologías y protocolos por confirmar (RT-04):** lenguaje y framework, motor de base de datos, protocolo del SSO, servicios del SIA y acceso al almacenamiento. Están marcados como «por confirmar» en los diagramas.
6. **Estados ADR-011 y ADR-012 «Propuesto».** Las vistas los reflejan, pero si cambian los plazos de retención o los criterios de asignación habrá que ajustar el Almacenamiento de archivos, AsignacionTutor y ESC-01.
