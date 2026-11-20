# language: es
# Traza: CU-01, OB-03, ADR-001, ADR-005, ADR-009, ADR-012

Característica: Asignar tutor académico a una práctica
  Como Coordinador de prácticas
  quiero que el sistema sugiera un tutor académico y me permita confirmar o ajustar la asignación
  para equilibrar la carga docente y garantizar el acompañamiento de los practicantes antes de iniciar su periodo.

  Antecedentes:
    Dado que el usuario autenticado tiene el rol "Coordinador de prácticas"
    Y el acceso queda registrado en la bitácora del sistema (ADR-005)

  Escenario: Sugerencia automática y confirmación directa (flujo básico)
    Dado una práctica registrada en estado "registrada" para el programa "Ingeniería de Sistemas"
    Y la versión vigente de la regla del programa establece una capacidad máxima de 10 estudiantes por tutor
    Y existen los tutores "Profesor A" con 4 estudiantes y "Profesor B" con 7 estudiantes asignados
    Cuando el Coordinador solicita sugerencia de asignación para la práctica
    Entonces el sistema sugiere al tutor "Profesor A" por tener menor carga en el programa
    Cuando el Coordinador confirma la sugerencia
    Entonces se registra una AsignacionTutor con origen "sugerida", estado vigente y fecha actual
    Y se actualiza el tutor vigente en la Práctica correspondiente
    Y el tutor "Profesor A" queda habilitado para consultar y dar seguimiento a dicha práctica (ADR-005)

  Escenario: Coordinador ajusta y elige otro tutor manualmente
    Dado una práctica registrada para el programa "Ingeniería de Sistemas"
    Y el sistema sugiere al "Profesor A" por tener menor carga
    Cuando el Coordinador decide no aceptar la sugerencia y selecciona al "Profesor B"
    Entonces el sistema registra la AsignacionTutor con el "Profesor B" y origen "manual"
    Y se actualiza el tutor vigente en la Práctica correspondiente
    Y la asignación sugerida previa no confirmada queda descartada

  Escenario: Advertencia por superación de capacidad máxima (ADR-012)
    Dado una práctica registrada para el programa "Ingeniería Industrial"
    Y la regla vigente establece una capacidad máxima de 8 estudiantes por tutor
    Y el "Profesor C" ya cuenta con 8 estudiantes asignados actualmente
    Cuando el Coordinador selecciona al "Profesor C" para la práctica
    Entonces el sistema muestra una advertencia indicando que el tutor ha alcanzado el límite de capacidad (8/8)
    Y permite al Coordinador confirmar la asignación forzada bajo su criterio
    Y la AsignacionTutor queda registrada como origen "manual" con la observación de sobrecupo

  Escenario: Reasignación de tutor conservando historial
    Dado una práctica que ya cuenta con una AsignacionTutor vigente con el "Profesor A"
    Cuando el Coordinador reasigna la práctica al "Profesor D" de manera manual
    Entonces la AsignacionTutor previa con el "Profesor A" pasa a estado no vigente en el historial
    Y se crea una nueva AsignacionTutor vigente con el "Profesor D"
    Y se actualiza el tutor vigente en la Práctica
    Y el "Profesor A" pierde el alcance de seguimiento sobre la práctica
    Y el "Profesor D" adquiere el alcance de seguimiento sobre la práctica
