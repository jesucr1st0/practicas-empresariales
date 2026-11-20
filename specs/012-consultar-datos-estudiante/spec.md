# language: es
# Traza: CU-12, RT-02, RT-03, RN-01, ADR-001, ADR-004, ADR-005, ADR-007, EAC-03, PA-01, PA-02

Característica: Consultar datos del estudiante
  Como Coordinador de prácticas o Tutor académico
  quiero consultar los datos del estudiante, el estado de su práctica empresarial y su información académica provista por el SIA
  para dar seguimiento a su avance, verificar requisitos y monitorear el acompañamiento según las reglas de alcance institucional.

  Antecedentes:
    Dado que los usuarios internos inician sesión con el SSO institucional (RT-02, ADR-004)
    Y todo acceso a datos personales queda registrado en la bitácora de auditoría (ADR-005, RN-01)

  Escenario: Coordinador consulta datos de estudiante con práctica activa y datos del SIA (flujo básico)
    Dado un estudiante con documento "1001234567" con una práctica en curso en el programa "Ingeniería de Sistemas", empresa "TechCorp" y tutor asignado "T-101"
    Y el servicio del SIA responde dentro del límite de 10 segundos con 140 créditos aprobados, promedio 4.2, semestre 9 y matrícula activa (RT-03, ADR-007)
    Cuando el Coordinador de prácticas consulta los datos del estudiante "1001234567" desde la IP "192.168.1.50" con agente "Mozilla/5.0"
    Entonces el sistema retorna los datos de la práctica, el tutor vigente y los datos académicos sincronizados del SIA
    Y el acceso queda registrado en la bitácora con sujeto "coordinador-01", acción "CU-12: consultar datos estudiante" y resultado exitoso (ADR-005, RN-01)

  Escenario: Tutor consulta los datos de un estudiante asignado a su cargo (regla de alcance, ADR-005)
    Dado el tutor académico con documento "T-101" autenticado con el rol "Tutor"
    Y el estudiante con documento "1001234567" tiene como tutor vigente a "T-101"
    Cuando el tutor "T-101" consulta los datos del estudiante "1001234567" desde la IP "192.168.1.60"
    Entonces el sistema valida la regla de alcance y autoriza el acceso a la información
    Y retorna los datos de la práctica y la información académica del estudiante
    Y el acceso queda registrado en la bitácora como exitoso

  Escenario: Tutor intenta consultar un estudiante no asignado a su cargo (violación de regla de alcance, ADR-005)
    Dado el tutor académico con documento "T-102" autenticado con el rol "Tutor"
    Y el estudiante con documento "1001234567" tiene como tutor vigente a "T-101"
    Cuando el tutor "T-102" intenta consultar los datos del estudiante "1001234567" desde la IP "192.168.1.60"
    Entonces el sistema deniega el acceso indicando que el tutor solo puede consultar a sus estudiantes asignados
    Y el intento no autorizado queda registrado en la bitácora como denegado

  Escenario: SIA no responde dentro del tiempo límite de 10 segundos (tolerancia a fallos, RT-03, EAC-03, PA-01)
    Dado un estudiante con documento "1001234567" con práctica registrada en el sistema
    Y el servicio del SIA presenta timeout superior a 10 segundos o caída temporal
    Cuando el Coordinador de prácticas consulta los datos del estudiante
    Entonces el sistema retorna los datos de la práctica disponibles localmente
    Y reporta que los datos académicos del SIA no están disponibles temporalmente sin abortar la operación
    Y no se realiza ninguna conexión directa a la base de datos del SIA (RT-03, EAC-03)

  Escenario: Consulta de estudiante sin práctica registrada en el sistema
    Dado un estudiante con documento "1009876543" del programa "Ingeniería Industrial" que no tiene práctica registrada
    Y el servicio del SIA responde con los datos académicos del estudiante
    Cuando el Coordinador de prácticas consulta al estudiante "1009876543"
    Entonces el sistema retorna la información académica del SIA e indica que el estudiante no posee práctica activa
    Y el acceso queda registrado en la bitácora

  Escenario: Usuario no autorizado intenta consultar datos de estudiante (ADR-005, RN-01)
    Dado un usuario autenticado con el rol "Estudiante"
    Cuando intenta consultar los datos del estudiante "1001234567" desde la IP "192.168.1.99"
    Entonces el sistema deniega el acceso por falta de permisos
    Y el acceso no autorizado queda registrado en la bitácora como denegado
