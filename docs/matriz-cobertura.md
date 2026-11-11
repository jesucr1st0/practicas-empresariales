# Matriz de cobertura: drivers y ADR por vista

Ninguna fila vacía: todo driver y todo ADR se ven en al menos una vista y en al menos un escenario. Los IDs de drivers son los vigentes de [drivers.md](drivers.md). Contexto es el marco de las vistas, no una vista de 4+1.

## Drivers por vista

| Driver o ADR | Contexto (marco) | Lógica | Procesos | Desarrollo | Física | Escenarios |
|---|:-:|:-:|:-:|:-:|:-:|---|
| CU-01 Asignar tutor | ✓ | ✓ | ✓ | ✓ |  | ESC-01 |
| CU-02 Registrar práctica | ✓ | ✓ | ✓ | ✓ |  | ESC-02 |
| CU-03 Realizar postulación | ✓ | ✓ | ✓ | ✓ |  | ESC-03 |
| CU-04 Seguimiento de horas | ✓ | ✓ | ✓ | ✓ |  | ESC-04 |
| CU-05 Evaluar al estudiante | ✓ | ✓ | ✓ | ✓ |  | ESC-05 |
| CU-06 Generar acta final | ✓ | ✓ | ✓ | ✓ | ✓ | ESC-06 |
| CU-07 a CU-12 (exportar acta, datos maestros, consultas) | ✓ |  |  | ✓ |  | ESC-06 (CU-07) |
| EAC-01 Modificabilidad: 480 a 540 horas, 1 solo módulo |  | ✓ | ✓ | ✓ | ✓ | ESC-02, ESC-06, ESC-07 |
| EAC-02 Seguridad: acceso externo sin cuenta | ✓ | ✓ | ✓ | ✓ | ✓ | ESC-04, ESC-05 |
| EAC-03 Fiabilidad: tolerancia a fallos del SIA | ✓ | ✓ | ✓ | ✓ | ✓ | ESC-03 |
| RT-01 Infraestructura de la Universidad |  |  |  |  | ✓ | ESC-04 |
| RT-02 SSO institucional | ✓ |  | ✓ | ✓ | ✓ | ESC-01 |
| RT-03 SIA solo por sus servicios | ✓ |  | ✓ | ✓ | ✓ | ESC-03 |
| RT-04 Tecnologías del catálogo |  |  | ✓ |  | ✓ | (por confirmar) |
| RN-01 Ley 1581: roles y registro de accesos |  | ✓ |  | ✓ | ✓ | ESC-04, ESC-05 |
| RN-02 Ley 594: retención de actas y evidencias |  | ✓ | ✓ |  | ✓ | ESC-06 |
| RN-03 Plantilla de acta oficial |  | ✓ |  | ✓ |  | ESC-06 |
| RN-04 Supervisor sin cuenta ni contraseña | ✓ | ✓ |  | ✓ |  | ESC-04, ESC-05 |
| RN-05 Sin licencias de pago recurrente |  |  | ✓ |  | ✓ | ESC-03 |
| PA-01 Integración con el SIA y tolerancia a fallos | ✓ |  | ✓ | ✓ |  | ESC-03 |
| PA-02 Doble acceso: SSO y enlace | ✓ |  | ✓ | ✓ |  | ESC-01, ESC-04 |
| PA-03 Reglas variables por programa |  | ✓ |  | ✓ |  | ESC-02, ESC-07 |
| PA-04 Integridad, trazabilidad y retención |  | ✓ | ✓ |  | ✓ | ESC-06 |
| PA-05 Solución proporcionada a la carga |  |  | ✓ | ✓ | ✓ | ESC-07 |

## ADR por vista

Cada ADR enlaza en su sección «Vistas que modifica» las vistas donde se ve ([adr/](adr/)).

| Driver o ADR | Contexto (marco) | Lógica | Procesos | Desarrollo | Física | Escenarios |
|---|:-:|:-:|:-:|:-:|:-:|---|
| ADR-001 Monolito modular |  |  | ✓ | ✓ | ✓ | ESC-07 |
| ADR-002 Base de datos relacional |  |  | ✓ | ✓ | ✓ | ESC-01, ESC-02, ESC-06 |
| ADR-003 Despliegue institucional |  |  | ✓ |  | ✓ | ESC-04 |
| ADR-004 Autenticación con SSO | ✓ |  | ✓ | ✓ | ✓ | ESC-01 |
| ADR-005 Roles y bitácora de accesos |  | ✓ | ✓ | ✓ |  | ESC-01, ESC-04, ESC-05 |
| ADR-006 Acceso externo por enlace | ✓ | ✓ | ✓ | ✓ | ✓ | ESC-04, ESC-05 |
| ADR-007 Adaptador aislado al SIA | ✓ |  | ✓ | ✓ | ✓ | ESC-03 |
| ADR-008 Verificación asíncrona con reintentos |  | ✓ | ✓ | ✓ |  | ESC-03 |
| ADR-009 Reglas versionadas |  | ✓ |  | ✓ |  | ESC-02, ESC-06, ESC-07 |
| ADR-010 Acta inmutable |  | ✓ | ✓ | ✓ | ✓ | ESC-06 |
| ADR-011 Retención documental |  | ✓ | ✓ | ✓ | ✓ | ESC-06 |
| ADR-012 Asignación sugerida |  | ✓ |  | ✓ |  | ESC-01 |
| ADR-013 Notificaciones por correo | ✓ |  | ✓ | ✓ | ✓ | ESC-03, ESC-04, ESC-05 |

## Dónde se ve cada ADR

| ADR | Estado | Dónde se ve |
|-----|--------|-------------|
| ADR-001 | Aceptado | Procesos: un solo contenedor, la Aplicación de prácticas; Desarrollo: módulos con límites explícitos y regla de dependencia; Física: un único artefacto en un solo Servidor de aplicaciones |
| ADR-002 | Aceptado | Procesos: contenedor Base de datos relacional (SQL); Desarrollo: Adaptador de persistencia; Física: Servidor de base de datos |
| ADR-003 | Aceptado | Procesos: todos los contenedores son propios, sin servicios de nube; Física: Centro de datos de la Universidad (RT-01) |
| ADR-004 | Aceptado | Contexto: SSO institucional como sistema externo; Procesos: conector hacia el SSO; Desarrollo: Adaptador SSO y puerto ProveedorIdentidad; Física: SSO entre los servicios institucionales existentes |
| ADR-005 | Aceptado | Lógica: RegistroAcceso (bitácora de solo inserción); Procesos: roles y bitácora en la Base de datos relacional; Desarrollo: Módulo Identidad y accesos y regla de alcance del tutor |
| ADR-006 | Aceptado | Contexto: Supervisor de empresa como persona externa sin cuenta; Lógica: EnlaceAcceso y Supervisor; Procesos: entrada HTTPS por enlace a la misma aplicación; Desarrollo: Formulario de acceso externo; Física: Celular del supervisor accede por Internet |
| ADR-007 | Aceptado | Contexto: SIA como sistema externo consultado por servicios; Procesos: conector con espera de 10 s hacia el SIA; Desarrollo: Adaptador SIA y puerto ConsultaAcademica; Física: conexión desde el Servidor de aplicaciones a los servicios del SIA |
| ADR-008 | Aceptado | Lógica: estados pendiente de verificación y revisión manual de Postulacion; Procesos: base de datos como cola y tarea programada dentro de la aplicación; Desarrollo: Planificador de tareas y Módulo Postulaciones |
| ADR-009 | Aceptado | Lógica: ReglaPrograma versionada y referencia fija de Practica; Desarrollo: Módulo Reglas |
| ADR-010 | Aceptado | Lógica: ActaFinal inmutable con huella y estado; Procesos: PDF en el Almacenamiento de archivos y metadatos en la base de datos; Desarrollo: Módulo Actas; Física: nodo de Almacenamiento de archivos |
| ADR-011 | Propuesto | Lógica: retención sobre ActaFinal y RegistroAcceso; Procesos: contenedor Almacenamiento de archivos; Desarrollo: Adaptador de archivos y puerto AlmacenArchivos; Física: Almacenamiento de archivos institucional |
| ADR-012 | Propuesto | Lógica: AsignacionTutor con historial y origen sugerida o manual; Desarrollo: Módulo Tutores y asignación |
| ADR-013 | Aceptado | Contexto: Servidor de correo institucional como sistema externo; Procesos: conector SMTP; Desarrollo: Módulo Notificaciones y Adaptador de correo; Física: correo entre los servicios institucionales existentes |

## Verificación

- **Drivers:** las 24 filas tienen al menos una vista; CU-07 a CU-12 se declaran sin escenario propio (ver [arquitectura.md §7](arquitectura.md#drivers-sin-adr-propio-declarados-como-riesgo)).
- **ADR:** los 13 ADR aparecen en al menos una vista; ADR-011 y ADR-012 están «Propuestos» y su reflejo en las vistas puede cambiar al confirmarse.
- **Cajas sin driver:** los elementos de cada catálogo se justifican en la sección 3 de su vista; las entidades de datos maestros (Programa, Empresa) responden a CU-02, CU-08, CU-09 y CU-10.
- **Escenarios:** CU-01 a CU-06 y EAC-01 a EAC-03 aparecen en al menos un escenario ([drivers.md §6](drivers.md#6-escenarios)).
