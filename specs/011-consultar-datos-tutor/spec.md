# language: es
# Traza: CU-11, RT-02, RT-03, RN-01, ADR-001, ADR-004, ADR-005, ADR-007, ADR-009, ADR-012, OB-03, PA-01, PA-02, EAC-03

Característica: Consultar datos del tutor académico
  Como Coordinador de prácticas
  quiero consultar la información detallada de los tutores académicos (datos personales, programa, datos institucionales del SIA, carga actual de prácticas y capacidad máxima)
  para supervisar la distribución docente, verificar la disponibilidad y realizar seguimiento al acompañamiento de los practicantes en el tablero de estado.

  Antecedentes:
    Dado que los usuarios internos inician sesión con el SSO institucional (RT-02, ADR-004)
    Y todo acceso a datos personales queda registrado en la bitácora de auditoría (ADR-005, RN-01)

  Escenario: Consulta exitosa de datos de tutor por el Coordinador de prácticas (flujo básico)
    Dado un tutor registrado en el sistema con documento "T-101", nombre "Profesor Juan Pérez", correo "juan.perez@universidad.edu.co" en el programa "Ingeniería de Sistemas"
    Y el servicio del SIA responde dentro del límite de 10 segundos con los datos institucionales: departamento "Sistemas e Informática", categoría "Asociado" y dedicación "Tiempo Completo" (RT-03, ADR-007)
    Y el tutor tiene 3 prácticas vigentes asignadas de una capacidad máxima de 10 estudiantes según la versión de regla vigente del programa (ADR-009, ADR-012)
    Cuando el Coordinador de prácticas consulta los datos del tutor "T-101" desde la IP "192.168.1.50" con agente "Mozilla/5.0"
    Entonces el sistema retorna los datos completos del tutor incluyendo su información institucional del SIA, carga actual (3/10) y el detalle de las 3 prácticas vigentes asignadas
    Y el acceso exitoso queda registrado en la bitácora con sujeto "coordinador-01", acción "CU-11: consultar datos tutor", IP "192.168.1.50" y resultado exitoso (ADR-005, RN-01)

  Escenario: Consulta de tutor inexistente
    Dado que el Coordinador de prácticas consulta la información de un tutor con documento "T-999" que no existe en el sistema
    Cuando se ejecuta la consulta desde la IP "192.168.1.50"
    Entonces el sistema informa que el tutor no fue encontrado
    Y el intento de consulta queda registrado en la bitácora indicando tutor no encontrado

  Escenario: Usuario no autorizado intenta consultar datos de tutor (ADR-005, RN-01)
    Dado un usuario autenticado con el rol "Estudiante"
    Cuando intenta consultar los datos del tutor "T-101"
    Entonces el sistema deniega el acceso indicando que solo el Coordinador de prácticas puede consultar los datos del tutor
    Y el acceso no autorizado queda registrado en la bitácora como denegado

  Escenario: SIA no responde o se encuentra caído (tolerancia a fallos, RT-03, EAC-03, PA-01)
    Dado un tutor registrado con documento "T-101" en el programa "Ingeniería de Sistemas"
    Y el servicio del SIA no responde dentro del tiempo límite de 10 segundos o reporta una falla de comunicación
    Cuando el Coordinador de prácticas consulta los datos del tutor "T-101"
    Entonces el sistema retorna los datos locales y la carga de prácticas del tutor disponibles en el sistema
    Y reporta que los datos institucionales del SIA no se encuentran disponibles temporalmente
    Y no se realiza ninguna conexión directa a la base de datos del SIA (RT-03, EAC-03)
    Y la consulta se completa satisfactoriamente para el usuario

  Escenario: Listar tutores por programa para el tablero de estado (CU-11, ADR-012)
    Dado el programa "Ingeniería de Sistemas" con tutores activos "T-101" con carga de 3 estudiantes y "T-102" con carga de 7 estudiantes
    Y la versión de regla vigente del programa define una capacidad máxima de 10 estudiantes por tutor
    Cuando el Coordinador de prácticas consulta el listado de tutores del programa para el tablero de estado
    Entonces el sistema retorna los tutores con su carga actual, capacidad máxima y disponibilidad
    Y el acceso al listado queda registrado en la bitácora
