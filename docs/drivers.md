# Drivers arquitectónicos: Sistema de Gestión de Prácticas Empresariales

Parte de [vision.md](vision.md). Los ADR de [adr/](adr/) citan estos IDs.

## 1. Casos de uso y casos de uso primarios

| ID | Caso de uso | Actor | ¿Primario? | Justificación |
|----|-------------|-------|------------|---------------|
| **CU-01** | Asignar tutor | Coordinador | Sí | Sustenta OB-03; condiciona el alcance de lo que ve cada tutor. |
| **CU-02** | Registrar práctica | Coordinador / Estudiante | Sí | Núcleo del sistema; fija las reglas del programa que aplican a la práctica (EAC-01). |
| **CU-03** | Realizar postulación | Estudiante | Sí | Depende del SIA para verificar datos académicos (RT-03, EAC-03). |
| **CU-04** | Realizar seguimiento en horas | Estudiante / Tutor / Supervisor | Sí | Sustenta OB-04; el supervisor valida sin cuenta (EAC-02). |
| **CU-05** | Evaluar empresa (evaluación del estudiante por la empresa) | Supervisor de empresa | Sí | Sustenta OB-05; acceso externo por enlace (RN-04). |
| **CU-06** | Generar acta final | Coordinador | Sí | Documento oficial con trazabilidad y retención (RN-02, RN-03). |
| CU-07 | Exportar acta final | Coordinador / Estudiante | No | Descarga del documento ya generado en CU-06. |
| CU-08 | Registrar estudiante | Administrador | No | Datos maestros; sin impacto arquitectónico propio. |
| CU-09 | Registrar tutor | Administrador | No | Datos maestros. |
| CU-10 | Registrar empresa | Coordinador | No | Datos maestros. |
| CU-11 | Consultar datos tutor | Coordinador | No | Consulta simple. |
| CU-12 | Consultar datos estudiante | Coordinador / Tutor | No | Consulta simple (datos académicos vía SIA). |

## 2. Escenarios de atributos de calidad

### EAC-01: Mantenibilidad (modificabilidad)

| Parte | Pregunta | Contenido |
|-------|----------|-----------|
| **1. Fuente del estímulo** | ¿Quién o qué lo provoca? | El director de programa |
| **2. Estímulo** | ¿Qué ocurre? | El Consejo aprueba subir las horas mínimas de práctica de 480 a 540 para un programa |
| **3. Artefacto** | ¿Sobre qué parte? | El módulo de reglas del programa |
| **4. Entorno** | ¿En qué condiciones? | Producción, con prácticas en curso, un mes antes del nuevo periodo |
| **5. Respuesta** | ¿Qué debe hacer el sistema? | El desarrollador aplica el cambio; las prácticas en curso conservan la regla anterior y las nuevas usan la regla nueva |
| **6. Medida de respuesta** | ¿Cómo se verifica? | **Cambio hecho en ≤ 8 horas-persona; 1 solo módulo modificado; 100 % de pruebas de regresión aprobadas; 0 prácticas en curso alteradas; servicio detenido ≤ 5 min** |

**Escenario redactado.** Cuando el Consejo aprueba subir de 480 a 540 las horas mínimas de un programa, un mes antes del nuevo periodo y con prácticas en curso en producción, el desarrollador modifica únicamente el módulo de reglas; las prácticas en curso conservan la regla anterior y las nuevas usan la nueva. El cambio toma máximo 8 horas-persona, pasa el 100 % de las pruebas de regresión, no altera ninguna práctica en curso y detiene el servicio máximo 5 minutos.

**Traza:** OB-02, OB-05 *(inferida)*, CU-02, CU-06, PA-03

### EAC-02: Seguridad (acceso externo sin cuenta)

| Parte | Pregunta | Contenido |
|-------|----------|-----------|
| **1. Fuente del estímulo** | ¿Quién o qué lo provoca? | Supervisor de empresa |
| **2. Estímulo** | ¿Qué ocurre? | Recibe el enlace para evaluar al estudiante y validar sus horas |
| **3. Artefacto** | ¿Sobre qué parte? | El formulario web |
| **4. Entorno** | ¿En qué condiciones? | Celular con conexión 4G |
| **5. Respuesta** | ¿Qué debe hacer el sistema? | Valida las horas y registra la evaluación sin crear cuenta |
| **6. Medida de respuesta** | ¿Cómo se verifica? | **El 90 % termina en ≤ 5 min; 0 contraseñas; carga ≤ 3 s (percentil 95); el enlace expira a los 30 días; 100 % de los accesos registrados** |

**Escenario redactado.** Cuando un supervisor abre desde su celular (4G) el enlace recibido para evaluar a un estudiante y validar sus horas, el formulario web carga en máximo 3 s (p95) y le permite completar ambas acciones sin cuenta ni contraseña; el 90 % termina en 5 minutos o menos, el enlace expira a los 30 días y el 100 % de los accesos queda registrado.

**Traza:** OB-04, OB-05, RI-03, RI-04, CU-04, CU-05, RN-04

### EAC-03: Fiabilidad (tolerancia a fallos del SIA)

| Parte | Pregunta | Contenido |
|-------|----------|-----------|
| **1. Fuente del estímulo** | ¿Quién o qué lo provoca? | Estudiante |
| **2. Estímulo** | ¿Qué ocurre? | Se postula con el SIA caído |
| **3. Artefacto** | ¿Sobre qué parte? | El servicio de verificación |
| **4. Entorno** | ¿En qué condiciones? | Operación normal con el SIA lento |
| **5. Respuesta** | ¿Qué debe hacer el sistema? | Guarda la postulación como "pendiente", avisa al estudiante y reintenta |
| **6. Medida de respuesta** | ¿Cómo se verifica? | **Con el SIA operativo, verificación ≤ 5 s (p95); sin respuesta a los 10 s, aviso en ≤ 1 min; reintento cada 15 min durante 24 h; 0 postulaciones perdidas; 0 conexiones directas a la base del SIA** |

**Escenario redactado.** Cuando un estudiante se postula y el SIA no responde en 10 segundos, el sistema guarda la postulación como "pendiente", avisa al estudiante en máximo 1 minuto y reintenta la verificación cada 15 minutos durante 24 horas, sin perder ninguna postulación y sin acceder nunca a la base de datos del SIA.

**Traza:** OB-02, RI-01, RT-03, CU-03, PA-01

## 3. Restricciones

> Estas restricciones **refinan y reemplazan** las de [vision.md](vision.md#5-restricciones) (v1.0). Los IDs vigentes son los de esta tabla.

| ID | Restricción | Tipo | Origen | Impacto arquitectónico esperado |
|----|-------------|------|--------|---------------------------------|
| **RT-01** | Desplegar el sistema en la infraestructura de la Universidad | Técnica | Área de sistemas | Despliegue en infraestructura institucional; sin nube pública |
| **RT-02** | Los usuarios internos inician sesión con el inicio de sesión único institucional | Seguridad | Administrador del SIA | Autenticación delegada; el sistema no gestiona contraseñas internas |
| **RT-03** | Consultar los datos académicos solo por los servicios del SIA, sin conexión directa a su base de datos | Integración | Administrador del SIA | Capa de integración aislada (puerto y adaptador) con manejo de fallas (EAC-03) |
| **RT-04** | Usar solo tecnologías del catálogo institucional | Técnica | Área de sistemas | Limita la selección de motor de BD, lenguaje y herramientas |
| **RN-01** | Cumplir la Ley 1581 de 2012 (protección de datos personales) | Legal | Ley 1581/2012 | Roles y registro de accesos |
| **RN-02** | Cumplir la Ley 594 de 2000 (Ley General de Archivos) | Legal | Ley 594/2000 | Retención de actas y evidencias |
| **RN-03** | Usar la plantilla de acta oficial | Negocio | Consejo de Facultad | Plantilla de acta oficial como entrada de CU-06 |
| **RN-04** | No exigir cuenta ni contraseña a los supervisores de empresa | Negocio | Director de programa | Acceso por enlace sin cuenta (EAC-02) |
| **RN-05** | No usar licencias de pago recurrente | Económica | Decanatura | Software libre / incluido en el catálogo; sin servicios externos de pago |

## 4. Preocupaciones arquitectónicas

| ID | Preocupación | Qué hay que decidir | Por qué importa en este sistema |
|----|--------------|---------------------|---------------------------------|
| **PA-01** | Integración con el SIA y tolerancia a sus fallos | Cómo se accede al SIA y qué pasa cuando falla | Las postulaciones dependen de datos del SIA, que puede estar lento o caído |
| **PA-02** | Doble acceso: inicio de sesión único (internos) y enlace seguro (externos) | Cómo se autentica cada tipo de usuario | Los supervisores no tienen cuenta (RN-04) pero validan horas y evalúan |
| **PA-03** | Reglas variables por programa y periodo sin alterar prácticas en curso | Cómo se representan y versionan las reglas | Cada programa cambia sus reglas y hay prácticas vigentes (EAC-01) |
| **PA-04** | Integridad, trazabilidad y retención de actas y datos personales | Cómo se garantiza que el acta no cambie y cuánto se conserva | Documento oficial sujeto a Ley 594 y Ley 1581 |
| **PA-05** | Solución proporcionada a la carga (~250 prácticas activas) | Estilo arquitectónico y número de unidades de despliegue | Equipo pequeño y carga moderada: evitar sobreingeniería |

## 5. Matriz de priorización

Eje de importancia para el negocio y eje de impacto arquitectónico.

### Alta importancia, alto impacto arquitectónico: atender primero

Integración con el SIA (PA-01, EAC-03, RT-03) · acceso externo (PA-02, EAC-02, RN-04) · reglas variables (PA-03, EAC-01) · trazabilidad del acta (PA-04, CU-06, RN-02, RN-03)

### Alta importancia, bajo impacto arquitectónico: hacer ya

Registro de horas (CU-04) · asignación de tutor (CU-01) · tablero de estado (CU-11, CU-12) · recordatorios

### Baja importancia, alto impacto arquitectónico: planificar

Inicio de sesión único (RT-02) · despliegue y catálogo institucional (RT-01, RT-04) · retención documental (RN-02)

### Baja importancia, bajo impacto arquitectónico: hacer si sobra tiempo

Vigencia de convenio · migración de prácticas históricas · diagnóstico para mesa de ayuda

## 6. Escenarios

Inventario del +1: qué escenarios se diagraman y por qué existe cada uno. Los escenarios **recorren** las cuatro vistas ya documentadas en [vistas/](vistas/); el recorrido está en [escenarios.md](escenarios.md).

| ID | Escenario | Origen | Por qué es escenario | Archivo en secuencias/ |
|----|-----------|--------|----------------------|------------------------|
| ESC-01 | Asignar tutor | CU-01 | Caso de uso primario. Muestra que el sistema sugiere y el coordinador confirma (ADR-012) y fija el alcance de lo que ve cada tutor | [cu01-asignar-tutor.puml](diagramas/secuencias/cu01-asignar-tutor.puml) |
| ESC-02 | Registrar práctica | CU-02 | Caso de uso primario. La práctica fija la versión de regla vigente (ADR-009); evidencia EAC-01 | [cu02-registrar-practica.puml](diagramas/secuencias/cu02-registrar-practica.puml) |
| ESC-03 | Realizar postulación | CU-03 | Caso de uso primario. Cubre **EAC-03**: SIA caído o lento, estado «pendiente», reintentos y 0 postulaciones perdidas | [cu03-realizar-postulacion.puml](diagramas/secuencias/cu03-realizar-postulacion.puml) |
| ESC-04 | Seguimiento de horas | CU-04 | Caso de uso primario. Cubre **EAC-02**: supervisor sin cuenta, enlace de un solo uso, 100 % de accesos registrados | [cu04-seguimiento-horas.puml](diagramas/secuencias/cu04-seguimiento-horas.puml) |
| ESC-05 | Evaluar al estudiante | CU-05 | Caso de uso primario. Cubre **EAC-02**: evaluación desde el celular y enlace invalidado tras el primer envío | [cu05-evaluar-estudiante.puml](diagramas/secuencias/cu05-evaluar-estudiante.puml) |
| ESC-06 | Generar acta final | CU-06 | Caso de uso primario. Acta inmutable con huella y trazabilidad hasta la versión de regla (ADR-010); evidencia EAC-01 | [cu06-generar-acta.puml](diagramas/secuencias/cu06-generar-acta.puml) |
| ESC-07 | Cambio de horas mínimas de 480 a 540 | EAC-01 | **EAC-01** no queda dentro de los casos primarios: su estímulo (el Consejo cambia la regla con prácticas en curso) no es un caso de uso. Muestra 1 solo módulo, 0 prácticas alteradas y ≤ 5 min de servicio detenido | [eac01-cambio-horas-minimas.puml](diagramas/secuencias/eac01-cambio-horas-minimas.puml) |

**Verificación:** cada caso de uso primario (CU-01 a CU-06) tiene su escenario; EAC-01 aparece en ESC-02, ESC-06 y ESC-07, EAC-02 en ESC-04 y ESC-05, EAC-03 en ESC-03. Ningún escenario carece de un caso primario o un EAC como origen. CU-07 a CU-12 no tienen escenario propio (sin impacto arquitectónico, ver [arquitectura.md §7](arquitectura.md#drivers-sin-adr-propio-declarados-como-riesgo)). No se incluyen escenarios transversales opcionales: la autenticación SSO se ve en ESC-01 y la trazabilidad por bitácora en ESC-04 y ESC-05.
