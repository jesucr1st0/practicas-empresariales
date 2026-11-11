# Vista de desarrollo: componentes, capas y usos

La organización estática de la **Aplicación de prácticas**: módulos, capas y dependencias (C4 nivel 3 más vista de usos).

**Stakeholders y preocupaciones que atiende:** Desarrollador de software (¿un cambio de reglas toca más de un módulo? ¿qué se puede entregar por incrementos?), Responsable de seguridad (¿dónde se aplican roles y bitácora?). Equipo de máximo 4 personas.

## 1. Presentación principal

Diagrama: [03-desarrollo.puml](../diagramas/03-desarrollo.puml), con tres diagramas de la misma vista:

1. **Componentes** (C4 nivel 3): adaptadores de entrada, módulos y adaptadores de salida.
2. **Capas** (Clean Architecture): `infraestructura → aplicacion → dominio`; las flechas apuntan hacia el dominio. Si `dominio/` importa algo de `infraestructura/`, la arquitectura está rota.
3. **Usos** entre módulos, **sin ciclos**. La flecha roja marca el tipo de dependencia prohibida (Reglas no puede usar Prácticas).

## 2. Catálogo de elementos

| Componente | Tipo | Responsabilidad | Depende de |
|------------|------|-----------------|------------|
| Interfaz web interna | Adaptador de entrada | Pantallas y controladores para usuarios con SSO; aplica rol y alcance | Todos los módulos de casos de uso |
| Formulario de acceso externo | Adaptador de entrada | Formulario liviano del supervisor; solo funciona con enlace vigente | Módulo Identidad y accesos, Módulo Horas, Módulo Evaluaciones |
| Planificador de tareas | Adaptador de entrada programado | Reintentos de verificación, recordatorios y alertas (ADR-008, ADR-013) | Módulo Postulaciones, Módulo Notificaciones, Módulo Horas, Módulo Evaluaciones |
| Módulo Identidad y accesos | Módulo (caso de uso) | Roles, permisos, emisión y validación de enlaces de un solo uso, bitácora de solo inserción | Puerto ProveedorIdentidad |
| Módulo Reglas | Módulo | Versiones inmutables de reglas por programa; resuelve la versión vigente a una fecha | Ninguno (base) |
| Módulo Postulaciones | Módulo | CU-03: guarda como pendiente, verifica, reintenta | Puerto ConsultaAcademica, Módulo Notificaciones |
| Módulo Prácticas | Módulo | CU-02 y CU-12: registra prácticas, estado, tutor vigente y tablero | Módulo Reglas, Módulo Postulaciones, Puerto ConsultaAcademica |
| Módulo Tutores y asignación | Módulo | CU-01, CU-09, CU-11: sugiere y confirma asignaciones con historial | Módulo Prácticas, Módulo Reglas, Puerto ConsultaAcademica |
| Módulo Horas | Módulo | CU-04: registro y validación de horas | Módulo Prácticas, Módulo Reglas, Módulo Identidad y accesos, Módulo Notificaciones |
| Módulo Evaluaciones | Módulo | CU-05: evaluación de la empresa | Módulo Prácticas, Módulo Identidad y accesos, Módulo Notificaciones |
| Módulo Actas | Módulo | CU-06 y CU-07: genera, guarda y exporta el acta inmutable | Módulo Prácticas, Módulo Horas, Módulo Evaluaciones, Módulo Reglas, Puerto AlmacenArchivos |
| Módulo Notificaciones | Módulo | Avisos, recordatorios y registro de cada envío, incluidos los fallidos | Puerto EnvioCorreo |
| Adaptador SIA | Adaptador de salida | Implementa ConsultaAcademica; **único** punto de acceso al SIA, con tiempos de espera y manejo de errores | SIA (servicios) |
| Adaptador de persistencia | Adaptador de salida | Implementa los puertos de repositorio | Base de datos relacional (SQL) |
| Adaptador de archivos | Adaptador de salida | Implementa AlmacenArchivos | Almacenamiento de archivos |
| Adaptador SSO | Adaptador de salida | Implementa ProveedorIdentidad | SSO institucional |
| Adaptador de correo | Adaptador de salida | Implementa EnvioCorreo | Servidor de correo institucional (SMTP) |

**Decisiones de organización que conviene conocer**

- **Alcance del tutor (ADR-005):** el Módulo Tutores y asignación registra la asignación y actualiza el *tutor vigente* de la Práctica a través del Módulo Prácticas; así el filtro «solo mis estudiantes» se aplica en Prácticas sin que Prácticas dependa de Tutores (evita un ciclo).
- **Enlaces (ADR-006):** Identidad y accesos guarda solo una referencia opaca a la práctica; no depende de Prácticas.
- **Incrementos posibles** (de menor a mayor nivel de dependencia): Reglas, Identidad, Notificaciones, ConsultaAcademica → Postulaciones → Prácticas → Tutores, Horas, Evaluaciones → Actas.

**Estructura propuesta en `src/`** (la implementación depende del lenguaje, aún por confirmar):

```text
src/
├── composicion/                 # arranque: lo único que conoce todas las capas
├── modulos/
│   ├── reglas/ ─────────┐
│   ├── identidad_accesos/│      cada módulo tiene:
│   ├── notificaciones/   │        dominio/          entidades y reglas
│   ├── postulaciones/    ├──      aplicacion/       casos de uso y puertos
│   ├── practicas/        │        infraestructura/  adaptadores
│   ├── tutores_asignacion/
│   ├── horas/            │
│   ├── evaluaciones/     │
│   └── actas/ ───────────┘
├── entradas/                    # Interfaz web interna, Formulario de acceso externo, Planificador de tareas
└── pruebas/arquitectura/        # pruebas automáticas de dependencias (mitigación de ADR-001)
```

## 3. Justificación

- **ADR-001 / PA-05 / EAC-01:** monolito modular con un módulo por capacidad, abarcable por 4 personas; un cambio de reglas queda en **Módulo Reglas** (1 solo módulo).
- **Regla de dependencia (ADR-001, ADR-007):** los casos de uso definen los puertos y los adaptadores los implementan; el SIA, el correo, el SSO, la base de datos y el almacenamiento quedan aislados en un adaptador cada uno.
- **RT-03 / EAC-03 / ADR-007:** «0 conexiones directas al SIA» se verifica aquí: solo el Adaptador SIA conoce al SIA.
- **EAC-01 / ADR-009:** Prácticas, Horas, Tutores y Actas resuelven la regla a través de Reglas; ninguna la copia.
- **RN-01 / ADR-005:** autorización y bitácora viven en Identidad y accesos y se aplican en los adaptadores de entrada.
- **ADR-010 / RN-03:** la generación del acta y su plantilla oficial están confinadas en Módulo Actas.
- **Riesgo asumido (ADR-001):** erosión de límites por la base de datos compartida; se mitiga con revisión en Pull Request y pruebas automáticas de dependencias entre módulos (`pruebas/arquitectura/`).

## 4. Comportamiento

- [ESC-03](../diagramas/secuencias/cu03-realizar-postulacion.puml): Interfaz web interna → Módulo Postulaciones → Adaptador SIA; Planificador de tareas → Módulo Postulaciones.
- [ESC-04](../diagramas/secuencias/cu04-seguimiento-horas.puml) y [ESC-05](../diagramas/secuencias/cu05-evaluar-estudiante.puml): Formulario de acceso externo → Módulo Identidad y accesos → Módulo Horas o Módulo Evaluaciones.
- [ESC-06](../diagramas/secuencias/cu06-generar-acta.puml): Módulo Actas usa Prácticas, Horas, Evaluaciones y Reglas.
- [ESC-07](../diagramas/secuencias/eac01-cambio-horas-minimas.puml): el cambio toca solo Módulo Reglas.

## 5. Vistas relacionadas

- **Procesos:** es el interior del contenedor Aplicación de prácticas ([02-procesos.md](02-procesos.md)).
- **Lógica:** los módulos operan sobre las entidades de `dominio/` ([01-logica.md](01-logica.md)).
- **Física:** todo este contenedor se despliega como un único artefacto ([04-fisica.md](04-fisica.md)).
