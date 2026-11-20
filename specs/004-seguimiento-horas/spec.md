# language: es
# Traza: CU-04, EAC-02, ADR-005, ADR-006, ADR-013, RN-04, OB-04

Característica: Realizar seguimiento en horas
  Como estudiante, tutor académico o supervisor de empresa
  quiero registrar, consultar y validar las horas de práctica empresarial
  para dar seguimiento al avance y certificar el cumplimiento de las horas requeridas.

  Escenario: Registro de horas por el estudiante (flujo básico)
    Dado un estudiante autenticado con SSO con una práctica en curso
    Cuando el estudiante registra 40 horas realizadas con fecha "2026-11-20" y evidencia "informe_semanal_1.pdf"
    Entonces el sistema crea un RegistroHoras con 40 horas en estado "pendiente"
    Y el registro queda asociado a la práctica del estudiante
    Y el sistema confirma al estudiante que las horas fueron registradas exitosamente

  Escenario: Consulta y seguimiento de horas por el tutor asignado (ADR-005)
    Dado un tutor académico autenticado con documento "T-001" asignado a la práctica "P-100"
    Y la práctica "P-100" tiene registros de horas pendientes y validados
    Cuando el tutor consulta el seguimiento de horas de la práctica "P-100"
    Entonces el sistema retorna el listado de registros de horas y el total acumulado de horas de la práctica

  Escenario: Tutor intenta consultar horas de una práctica no asignada (ADR-005)
    Dado un tutor académico autenticado con documento "T-002" que no está asignado a la práctica "P-100"
    Cuando el tutor intenta consultar las horas de la práctica "P-100"
    Entonces el sistema deniega el acceso indicando que la práctica no está en su alcance asignado
    Y el intento no autorizado queda registrado en la bitácora

  Escenario: Emisión y envío de enlace de validación al supervisor (ADR-006, ADR-013)
    Dado una práctica "P-100" con horas pendientes de validación y un supervisor con correo "supervisor@empresa.com"
    Cuando se solicita la validación del supervisor para la práctica "P-100"
    Entonces el sistema genera un EnlaceAcceso con un token criptográfico seguro de al menos 128 bits
    Y almacena únicamente el hash del token en la base de datos con vigencia de 30 días
    Y el sistema envía un correo institucional a "supervisor@empresa.com" con el enlace de acceso
    Y el envío del correo queda registrado en el historial de notificaciones

  Escenario: Validación de horas por el supervisor sin cuenta ni contraseña (EAC-02, RN-04, ADR-006)
    Dado un enlace de acceso vigente para la práctica "P-100" emitido para el supervisor
    Cuando el supervisor abre el enlace desde un navegador externo o celular con IP "190.85.12.34" y agente "Mobile Safari"
    Entonces el sistema registra el acceso en la bitácora (quién, qué, cuándo, IP y agente)
    Y concede acceso exclusivamente a los registros de horas de la práctica "P-100" sin solicitar contraseña
    Cuando el supervisor aprueba la validación de las horas pendientes
    Entonces los registros de horas pasan a estado "validados"
    Y el supervisor recibe la confirmación de validación exitosa

  Escenario: Acceso con enlace vencido, usado o revocado (EAC-02, ADR-006)
    Dado un enlace de acceso asociado a la práctica "P-100" que se encuentra vencido, usado o revocado
    Cuando un usuario intenta acceder utilizando dicho token con IP "190.85.12.34" y agente "Mobile Safari"
    Entonces el sistema registra el intento de acceso en la bitácora con resultado denegado
    Y deniega el acceso con el mensaje "enlace no disponible; pida al coordinador que lo reemita"
    Y no permite consultar ni validar las horas de la práctica
