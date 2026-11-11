# Documento de visión: Sistema de Gestión de Prácticas Empresariales

> **Enunciado.** La Facultad de Ingenierías quiere un sistema para centralizar la gestión de las prácticas empresariales de sus estudiantes: postulación, asignación de tutores, seguimiento de horas, evaluación de la empresa y generación del acta final. *(Resumen: reemplazar por el texto original del enunciado del taller.)*

**Versión:** 1.0 · **Fecha:** 2 de noviembre de 2026

## 1. Problema u oportunidad

Actualmente, la Facultad de Ingenierías gestiona las prácticas empresariales mediante herramientas no centralizadas, principalmente hojas de cálculo de Excel y correo electrónico. Esto dificulta el seguimiento de las postulaciones, la asignación de tutores, el control de las horas realizadas y la evaluación del desempeño de los estudiantes por parte de las empresas. Además, la información puede estar dispersa, duplicada o desactualizada, lo que incrementa el trabajo administrativo y dificulta conocer el estado real de cada práctica. Con aproximadamente 500 estudiantes en práctica al año y 50 tutores, se necesita una solución que centralice el proceso, facilite el seguimiento y garantice la disponibilidad y trazabilidad de la información.

## 2. Objetivos de negocio

| ID | Objetivo | Indicador de cumplimiento |
|----|----------|---------------------------|
| **OB-01** | Reducir el tiempo dedicado a la gestión administrativa de las prácticas empresariales. | Disminuir en un 50 % el tiempo promedio de gestión respecto al proceso actual, durante el primer año de implementación. |
| **OB-02** | Mejorar la trazabilidad de las prácticas desde la postulación hasta su finalización. | El 100 % de los estudiantes registrados tiene información actualizada sobre el estado de su práctica. |
| **OB-03** | Optimizar la distribución y asignación de tutores académicos. | Al menos el 95 % de los estudiantes que cumplan los requisitos cuenta con tutor antes del inicio de su práctica. |
| **OB-04** | Mejorar el control y cumplimiento de las horas de práctica. | Al menos el 95 % de los registros de horas cuenta con seguimiento y validación del responsable. |
| **OB-05** | Incrementar la oportunidad en la evaluación y cierre de las prácticas. | Al menos el 95 % de las prácticas finalizadas cuenta con evaluación de la empresa y acta final dentro de los cinco días hábiles siguientes a su finalización. |

*Nota: los porcentajes y tiempos son metas propuestas y deben validarse con la Facultad antes de su aprobación definitiva.*

## 3. Alcance

### Qué SÍ incluye

- **Postulación de estudiantes:** registro de solicitudes y consulta de su estado.
- **Asignación de tutores:** distribución de estudiantes entre los tutores académicos.
- **Seguimiento de horas:** registro, consulta y validación de las horas realizadas.
- **Evaluación empresarial:** registro de las evaluaciones de las empresas sobre los estudiantes.
- **Generación del acta final:** consolidación de la información de la práctica en el documento de cierre.
- **Gestión de usuarios y roles:** administración de accesos de estudiantes, tutores y personal administrativo.
- **Consulta de información:** estado y avance de las prácticas para usuarios autorizados.

### Qué NO incluye

- Gestión de contratos laborales y procesos de contratación empresarial.
- Administración de nómina, salarios o pagos a estudiantes.
- Búsqueda y publicación de ofertas laborales o vacantes.
- Gestión de calificaciones de asignaturas distintas a las prácticas.
- Administración financiera o contable de las empresas participantes.
- Integración con plataformas externas de firma electrónica, mientras no sea una necesidad institucional.

## 4. Stakeholders

| Nombre / rol | Tipo | Preocupaciones | Poder / interés |
|--------------|------|----------------|-----------------|
| Decano o representante de la Facultad | Negocio | Cumplimiento de objetivos institucionales, eficiencia y resultados. | Alto / Alto |
| Coordinador de prácticas empresariales | Negocio | Postulaciones, asignación de tutores y seguimiento de estudiantes. | Alto / Alto |
| Estudiantes en práctica | Negocio | Facilidad de postulación, consulta de estados y registro de horas. | Medio / Alto |
| Tutores académicos | Negocio | Seguimiento de estudiantes, validación de horas y evaluación de avances. | Medio / Alto |
| Desarrollador de software | Técnico | Mantenibilidad, modularidad, facilidad de pruebas y evolución. | Medio / Alto |
| Administrador de infraestructura y TI | Técnico | Despliegue, disponibilidad, rendimiento, copias de seguridad y monitoreo. | Alto / Medio |
| Responsable de seguridad informática | Técnico | Protección de datos personales, autenticación, autorización y control de accesos. | Alto / Alto |
| Responsable de soporte técnico | Técnico | Diagnóstico de errores, registro de incidentes y mantenimiento operativo. | Medio / Medio |
| Representante de las empresas participantes | Negocio | Facilidad para evaluar estudiantes y validar su desempeño. | Bajo / Medio |

## 5. Restricciones

> **Nota:** esta es la versión 1.0 de la visión. Tras el taller de drivers, las restricciones se refinaron y reasignaron en [drivers.md](drivers.md#3-restricciones); **los IDs de drivers.md son los vigentes**.

| ID | Tipo | Restricción | Origen |
|----|------|-------------|--------|
| RT-01 | Técnica | Mecanismos de protección para la información personal y académica de los estudiantes. | Políticas institucionales y normativa de protección de datos. |
| RT-02 | Técnica | Acceso diferenciado según roles y responsabilidades. | Necesidades de control y seguridad de la Facultad. |
| RN-01 | Negocio | Contemplar ~500 estudiantes en práctica por año. | Facultad de Ingenierías. |
| RN-02 | Negocio | Contemplar ~50 tutores académicos. | Facultad de Ingenierías. |
| RN-03 | Organizacional | Desarrollo en equipos de máximo cuatro integrantes. | Condición del docente para el taller. |

**Pendiente de confirmación:** tecnologías institucionales obligatorias, infraestructura de despliegue, presupuesto, integraciones y plazos. No son restricciones confirmadas mientras no exista decisión formal.

## 6. Supuestos y riesgos iniciales

### Supuestos

- **S-01:** La Facultad proporcionará la información de estudiantes, tutores y empresas.
- **S-02:** Cada estudiante tendrá una cuenta individual de acceso.
- **S-03:** Los tutores tienen responsabilidades de seguimiento y validación de sus estudiantes asignados.
- **S-04:** Las empresas podrán proporcionar información y evaluaciones del desempeño de los practicantes.
- **S-05:** La Facultad establecerá los requisitos y criterios para aprobar y finalizar una práctica.
- **S-06:** Existirá un responsable institucional que administre los usuarios y supervise el sistema.

### Riesgos

| ID | Riesgo inicial | Objetivo afectado | Mitigación |
|----|----------------|-------------------|------------|
| RI-01 | Información histórica incompleta, duplicada o desactualizada en Excel. | OB-02 | Revisar, depurar y validar los datos antes de migrarlos. |
| RI-02 | Resistencia de estudiantes, tutores o administrativos a usar la solución. | OB-01 | Capacitación y documentación de uso. |
| RI-03 | Falta de disponibilidad de las empresas para evaluar a los estudiantes. | OB-05 | Fechas límite, notificaciones y seguimiento. |
| RI-04 | Acceso no autorizado o exposición de información personal y académica. | OB-02 | Controles de acceso, autenticación, copias de seguridad y protección de datos. |
| RI-05 | Retrasos por falta de claridad en procedimientos institucionales. | OB-01 | Validar procesos con el coordinador de prácticas antes de implementar. |

## Conclusión

La implementación del Sistema de Gestión de Prácticas Empresariales moderniza los procesos de la Facultad, reduce la carga administrativa y mejora el seguimiento académico, centralizando la información y dando control y trazabilidad durante todas las etapas de las prácticas.
