# Vista lógica: modelo de dominio

Muestra los conceptos del negocio y cómo se relacionan, **no las clases del código**. C4 no tiene diagrama para esta vista: se usa UML.

**Stakeholders y preocupaciones que atiende:** Coordinador de prácticas, estudiantes, tutores y representante de las empresas (¿qué maneja el sistema y qué reglas lo gobiernan?); Responsable de seguridad (¿qué se registra de cada acceso?). Preocupación arquitectónica: requisitos funcionales (CU-01 a CU-06).

## 1. Presentación principal

Diagrama: [01-logica.puml](../diagramas/01-logica.puml) (UML, solo atributos clave, sin tipos, visibilidad, métodos ni elementos técnicos).

Cómo se lee: cada línea es una relación del negocio con su multiplicidad. Las multiplicidades guardan reglas: `Practica 1 — 0..1 Evaluacion` (una evaluación por práctica), `Practica 1 — 0..* ActaFinal` con **una sola vigente**, `AsignacionTutor` con **una sola vigente** y el resto como historial.

## 2. Catálogo de elementos

| Entidad | Qué representa | Atributos clave | Regla del negocio |
|---------|----------------|-----------------|-------------------|
| Programa | Programa académico de la Facultad | nombre | Cada programa tiene sus propias reglas (PA-03) |
| ReglaPrograma | Una **versión** de las reglas de práctica de un programa | versión, vigencia desde, horas mínimas, capacidad máxima por tutor | Inmutable: un cambio crea una versión nueva, nunca edita la anterior (ADR-009) |
| Estudiante | Quien realiza la práctica | documento, nombre | Sus datos académicos se consultan al SIA, no se replican (ADR-007) |
| Tutor | Docente que acompaña a los estudiantes | documento, nombre | Solo ve a los estudiantes que tiene asignados (ADR-005) |
| Empresa | Organización donde se realiza la práctica | NIT, razón social | Tiene al menos un supervisor |
| Supervisor | Persona de la empresa que valida y evalúa | nombre, correo | No tiene cuenta ni contraseña; actúa solo con un enlace (RN-04) |
| Postulacion | Solicitud del estudiante para hacer práctica | fecha, estado | Nunca se pierde ni se descarta; tras 24 h sin verificar pasa a revisión manual (ADR-008) |
| Practica | La práctica empresarial en sí | periodo, fecha de inicio, fecha de fin, estado | Se rige por la versión de regla vigente al registrarse y esa referencia no cambia (EAC-01) |
| AsignacionTutor | Vínculo de un tutor con una práctica | fecha, vigente, origen (sugerida o manual) | El sistema sugiere y el coordinador confirma; todo queda en el historial (ADR-012) |
| RegistroHoras | Horas realizadas y su validación | fecha, cantidad, evidencia, estado de validación | Las valida el supervisor; el tutor da seguimiento (OB-04) |
| Evaluacion | Evaluación del estudiante hecha por la empresa | fecha, resultado, observaciones | Una por práctica; no se modifica una vez enviada |
| ActaFinal | Documento oficial de cierre | fecha de emisión, huella de integridad, estado | Plantilla oficial (RN-03); inmutable; una corrección genera un acta nueva y anula la anterior (ADR-010) |
| EnlaceAcceso | Autorización de un solo uso para el supervisor | acciones permitidas, vencimiento, estado | Ligado a una práctica y a un supervisor; vence a los 30 días; se invalida al enviar la evaluación (ADR-006) |
| RegistroAcceso | Constancia de un acceso a datos personales | quién, qué, cuándo, desde dónde | Solo se agrega, nunca se modifica ni se borra antes de su plazo (RN-01, ADR-005) |

Estados usados: Postulacion (pendiente de verificación, verificada, rechazada, revisión manual); Practica (registrada, en curso, finalizada, cerrada); ActaFinal (vigente, anulada); EnlaceAcceso (vigente, usado, vencido, revocado).

Los **roles** (Estudiante, Tutor, Coordinador, Administrador, Supervisor externo) y sus permisos se administran como datos en la base de datos (ADR-005); no se modelan como entidades de negocio para mantener pocas clases.

## 3. Justificación

- **CU-01 a CU-06:** de ellos salen Postulacion, Practica, AsignacionTutor, RegistroHoras, Evaluacion y ActaFinal.
- **EAC-01 / PA-03 / ADR-009:** `ReglaPrograma` como dato versionado y la referencia fija de `Practica` hacen posible subir de 480 a 540 horas sin alterar prácticas en curso.
- **EAC-02 / RN-04 / ADR-006:** `EnlaceAcceso` y `Supervisor` modelan el acceso sin cuenta; `RegistroAcceso` sostiene el 100 % de accesos registrados.
- **EAC-03 / ADR-008:** los estados de `Postulacion` incluyen «pendiente de verificación» y «revisión manual», de modo que ninguna postulación se pierde sin explicación.
- **PA-04 / RN-02 / ADR-010:** `ActaFinal` inmutable, con huella y estado vigente o anulada, da el documento estable y trazable.
- **RN-01 / ADR-005:** `RegistroAcceso` responde a la Ley 1581 (quién, qué, cuándo, desde dónde).
- **CU-01 / ADR-012:** `AsignacionTutor` conserva el historial y distingue lo sugerido de lo confirmado.

## 4. Comportamiento

Los escenarios cambian el estado de las entidades:

- [ESC-03](../diagramas/secuencias/cu03-realizar-postulacion.puml): Postulacion pasa de pendiente de verificación a verificada, rechazada o revisión manual.
- [ESC-02](../diagramas/secuencias/cu02-registrar-practica.puml): se crea Practica con su ReglaPrograma.
- [ESC-04](../diagramas/secuencias/cu04-seguimiento-horas.puml) y [ESC-05](../diagramas/secuencias/cu05-evaluar-estudiante.puml): RegistroHoras pasa a validado; EnlaceAcceso pasa a usado; se crea Evaluacion.
- [ESC-06](../diagramas/secuencias/cu06-generar-acta.puml): se crea ActaFinal vigente y, si hay corrección, la anterior pasa a anulada.
- [ESC-07](../diagramas/secuencias/eac01-cambio-horas-minimas.puml): se agrega una ReglaPrograma sin tocar las existentes.

## 5. Vistas relacionadas

- **Desarrollo:** estas entidades viven en `dominio/` y los módulos las usan ([03-desarrollo.md](03-desarrollo.md)).
- **Procesos:** las entidades se guardan en la Base de datos relacional y los PDF de ActaFinal en el Almacenamiento de archivos ([02-procesos.md](02-procesos.md)).
- **Contexto:** los actores que manipulan estos conceptos ([contexto.md](../contexto.md)).
