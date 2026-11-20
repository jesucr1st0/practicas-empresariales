# language: es
# Traza: CU-10, CU-02, RN-01, ADR-001, ADR-004, ADR-005, OB-01

Característica: Registrar empresa y sus supervisores
  Como Coordinador de prácticas
  quiero registrar una empresa participante y los datos de su supervisor
  para formalizar la vinculación de organizaciones autorizadas para recibir estudiantes en práctica empresarial.

  Antecedentes:
    Dado que los usuarios internos inician sesión con el SSO institucional (RT-02, ADR-004)
    Y todo registro y acceso a datos personales queda registrado en la bitácora de auditoría (ADR-005, RN-01)

  Escenario: Registro exitoso de empresa con supervisor inicial (flujo básico)
    Dado que el usuario autenticado tiene el rol "Coordinador de prácticas"
    Cuando el Coordinador registra una empresa con NIT "900123456-1", razón social "Tech Solutions S.A.S.", sector "Tecnología", ciudad "Manizales" y el supervisor inicial con nombre "Carlos Pérez", correo "carlos.perez@techsolutions.com" y teléfono "3001234567" desde la IP "192.168.1.50"
    Entonces el sistema registra la Empresa en estado activa
    Y crea y asocia el Supervisor a la Empresa
    Y el registro queda asentado en la bitácora con sujeto "coordinador-01", acción "CU-10: registrar empresa" y resultado exitoso (ADR-005, RN-01)

  Escenario: Intento de registro con NIT duplicado
    Dado que en el sistema ya existe una empresa registrada con NIT "900123456-1"
    Cuando el Coordinador intenta registrar otra empresa con el mismo NIT "900123456-1"
    Entonces el sistema rechaza la operación indicando que ya existe una empresa registrada con ese NIT
    Y no crea una nueva empresa ni duplica registros
    Y el intento fallido queda registrado en la bitácora de auditoría

  Escenario: Intento de registrar empresa sin supervisor inicial
    Dado que el modelo del negocio exige que toda Empresa cuente con al menos un supervisor
    Cuando el Coordinador intenta registrar una empresa con NIT "900987654-3" y razón social "Innovar Ltda." pero sin proporcionar los datos de un supervisor
    Entonces el sistema rechaza la solicitud indicando que debe incluirse al menos un supervisor para la empresa
    Y no se almacena la empresa en el sistema

  Escenario: Usuario no autorizado intenta registrar una empresa (ADR-005, RN-01)
    Dado un usuario autenticado con el rol "Estudiante"
    Cuando intenta registrar una empresa en el sistema desde la IP "192.168.1.88"
    Entonces el sistema deniega la operación por permisos insuficientes
    Y el intento no autorizado queda registrado en la bitácora de accesos como denegado

  Escenario: Consulta de empresa registrada por NIT
    Dado que la empresa "Tech Solutions S.A.S." con NIT "900123456-1" y supervisor "Carlos Pérez" está registrada
    Cuando el Coordinador consulta la empresa por su NIT "900123456-1"
    Entonces el sistema retorna los datos de la empresa y la lista de sus supervisores asociados
    Y el acceso a la consulta queda registrado en la bitácora de auditoría
