# Vista física: diagrama de despliegue

Dónde se ejecuta cada contenedor y por qué red viaja cada conexión.

**Stakeholders y preocupaciones que atiende:** Administrador de infraestructura y TI (¿qué se instala, en qué servidores, cómo se respalda y monitorea?), Responsable de seguridad (¿los datos personales permanecen en la institución?), Decanatura (¿hay costo recurrente?).

## 1. Presentación principal

Diagrama: [04-fisica.puml](../diagramas/04-fisica.puml) (C4 despliegue).

Cómo se lee: todo lo que construye el equipo corre dentro del **Centro de datos de la Universidad**. Los usuarios entran por HTTPS; el supervisor lo hace desde Internet con su celular. La base de datos y el almacenamiento solo se acceden desde la red interna. **RT-01 se verifica aquí:** no hay nube pública.

## 2. Catálogo de elementos

| Nodo | Contenedores que aloja | Características | Conexiones |
|------|------------------------|-----------------|------------|
| Servidor de aplicaciones | Aplicación de prácticas | Un único artefacto reproducible; capacidad fija, sin elasticidad; un redespliegue detiene el servicio ≤ 5 min (EAC-01). SO y entorno de ejecución **por confirmar** (RT-04) | Navegadores (HTTPS), base de datos (SQL), almacenamiento, SIA, SSO, correo (SMTP) |
| Servidor de base de datos | Base de datos relacional | Solo accesible desde la red interna; copias de seguridad a cargo del Área de sistemas | Aplicación de prácticas (SQL) |
| Almacenamiento de archivos institucional | Almacenamiento de archivos | Dentro del centro de datos; retención parametrizable y sin borrado físico antes del plazo (ADR-011); respaldo coordinado con el de la base de datos | Aplicación de prácticas (lee y escribe) |
| Servicios institucionales existentes | SIA, SSO institucional, Servidor de correo institucional | Administrados por el Área de sistemas y el Administrador del SIA; **no los despliega este proyecto** | Aplicación de prácticas |
| Equipo del usuario interno | Navegador | Cualquier navegador moderno | Aplicación de prácticas (HTTPS) |
| Celular del supervisor | Navegador móvil | Conexión 4G; formulario ≤ 3 s (p95) | Aplicación de prácticas (HTTPS, Internet) |

Todos los nodos del proyecto están en el centro de datos de la Universidad. La ubicación exacta de los servicios institucionales existentes está **por confirmar**.

## 3. Justificación

- **RT-01 / ADR-003:** servidor de aplicaciones, base de datos y almacenamiento están en infraestructura propia; no hay nube pública ni esquema híbrido.
- **RN-01 / PA-04:** los datos personales, las actas y la bitácora no salen de la institución; el único tráfico saliente es el correo institucional.
- **RN-05 / ADR-001:** un solo servidor de aplicaciones, sin broker ni servicios externos de pago.
- **RT-04 / ADR-002:** el sistema operativo, el entorno de ejecución y el motor de base de datos se eligen del catálogo; hasta confirmarlo se mantienen como candidatos.
- **EAC-01:** al ser un único artefacto, el servicio detenido durante un cambio de reglas es el de un redespliegue (≤ 5 min).
- **EAC-02:** la ruta del formulario de acceso externo debe ser alcanzable desde Internet por HTTPS; el resto de rutas puede restringirse a la red institucional o a VPN.
- **ADR-011:** el almacenamiento de archivos es un nodo propio, separado de la base de datos.

**Puntos por confirmar con el Área de sistemas** (vision.md §5, «pendiente de confirmación»): catálogo de tecnologías, quién publica el acceso por Internet (proxy inverso o zona desmilitarizada), frecuencia de respaldos, monitoreo y si habrá un entorno de pruebas con simulador del SSO y del SIA.

## 4. Comportamiento

- [ESC-04](../diagramas/secuencias/cu04-seguimiento-horas.puml) y [ESC-05](../diagramas/secuencias/cu05-evaluar-estudiante.puml): el supervisor atraviesa Internet hasta el Servidor de aplicaciones; el resto del recorrido ocurre en la red interna.
- [ESC-03](../diagramas/secuencias/cu03-realizar-postulacion.puml): la espera de 10 s se da en la conexión entre el Servidor de aplicaciones y el SIA.
- [ESC-06](../diagramas/secuencias/cu06-generar-acta.puml): el PDF se escribe en el nodo de Almacenamiento de archivos y la huella en el de base de datos.
- [ESC-07](../diagramas/secuencias/eac01-cambio-horas-minimas.puml): el redespliegue afecta a un solo nodo.

## 5. Vistas relacionadas

- **Procesos:** cada contenedor de esa vista aparece en un nodo de esta ([02-procesos.md](02-procesos.md)).
- **Contexto:** cada sistema externo aparece con su protocolo ([contexto.md](../contexto.md)).
- **Desarrollo:** el artefacto que se despliega es la Aplicación de prácticas completa ([03-desarrollo.md](03-desarrollo.md)).
