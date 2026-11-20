# language: es
# Traza: CU-03, EAC-03, ADR-007, ADR-008, ADR-013

Característica: Realizar postulación
  Como estudiante autenticado
  quiero postularme a una práctica empresarial
  para que el sistema verifique mis datos académicos y registre mi solicitud.

  Antecedentes:
    Dado que el estudiante ha iniciado sesión con el SSO institucional

  Escenario: Postulación exitosa
    Dado un estudiante con documento "1001234567" del programa "Ingeniería de Sistemas"
    Y el estudiante tiene paz y salvo académico en el SIA
    Y no tiene una postulación activa
    Cuando el estudiante solicita postularse a una práctica empresarial
    Entonces el sistema crea una Postulacion en estado "pendiente de verificación"
    Y el sistema consulta los datos académicos al SIA con un tiempo de espera de 10 segundos
    Y el SIA confirma que el estudiante cumple los requisitos
    Y la Postulacion pasa a estado "verificada"
    Y el sistema envía un correo institucional al estudiante confirmando la postulación
    Y el sistema notifica al Coordinador de prácticas

  Escenario: Estudiante sin requisitos académicos
    Dado un estudiante con documento "1009876543" del programa "Ingeniería Civil"
    Y el estudiante tiene una deuda pendiente con la biblioteca en el SIA
    Cuando el estudiante solicita postularse a una práctica empresarial
    Entonces el sistema crea una Postulacion en estado "pendiente de verificación"
    Y el sistema consulta los datos académicos al SIA
    Y el SIA indica que el estudiante no cumple los requisitos
    Y la Postulacion pasa a estado "rechazada"
    Y el sistema envía un correo al estudiante indicando el motivo del rechazo

  Escenario: SIA no responde en 10 segundos (EAC-03)
    Dado un estudiante con documento "1001234567" del programa "Ingeniería de Sistemas"
    Y el SIA no está disponible o responde lento
    Cuando el estudiante solicita postularse a una práctica empresarial
    Entonces el sistema crea una Postulacion en estado "pendiente de verificación"
    Y el sistema intenta consultar al SIA con un tiempo de espera de 10 segundos
    Y el SIA no responde dentro de los 10 segundos
    Y la Postulacion permanece en estado "pendiente de verificación"
    Y el sistema avisa al estudiante en máximo 1 minuto que la verificación está pendiente
    Y el sistema programa reintentos de verificación cada 15 minutos durante 24 horas
    Y no se pierde ninguna postulación

  Escenario: SIA no responde en 24 horas
    Dado una Postulacion en estado "pendiente de verificación" con 24 horas de reintentos fallidos
    Cuando se agotan los reintentos sin respuesta del SIA
    Entonces la Postulacion pasa a estado "revisión manual"
    Y el sistema envía un correo al Coordinador de prácticas para revisión manual
    Y no se pierde la postulación

  Escenario: Respuesta del SIA dentro de los reintentos
    Dado una Postulacion en estado "pendiente de verificación" con reintentos programados
    Y el SIA vuelve a estar disponible después de 2 horas
    Cuando el planificador ejecuta el siguiente reintento
    Entonces el sistema consulta al SIA y obtiene respuesta en menos de 5 segundos (p95)
    Y la Postulacion pasa a estado "verificada" o "rechazada" según los datos del SIA
    Y el sistema envía un correo al estudiante con el resultado

  Escenario: Postulación duplicada
    Dado un estudiante con documento "1001234567"
    Y el estudiante ya tiene una Postulacion en estado "pendiente de verificación" o "verificada"
    Cuando el estudiante intenta postularse nuevamente
    Entonces el sistema rechaza la solicitud
    Y le indica al estudiante que ya tiene una postulación activa
