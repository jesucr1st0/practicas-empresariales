# language: es
# Traza: CU-08, ADR-005, ADR-004, ADR-007, ADR-001, RN-01, RT-03

Característica: Registrar estudiante
  Como Administrador
  quiero registrar los datos maestros de un estudiante
  para que pueda postularse, tener prácticas a su nombre y recibir notificaciones del sistema.

  # [NECESITA ACLARACIÓN: la vista de desarrollo no asigna CU-08 a ningún módulo. Se ubica en el
  #  Módulo Prácticas porque ese módulo ya atiende CU-12 (Consultar datos estudiante).]
  # [NECESITA ACLARACIÓN: drivers.md no fija los datos maestros del estudiante. Se toman los
  #  atributos clave de la vista lógica (documento, nombre), el programa (las prácticas y las
  #  reglas son por programa) y el correo institucional (ADR-013 notifica al estudiante por correo).]

  Escenario: Registro exitoso de un estudiante (flujo básico)
    Dado un usuario autenticado con SSO con documento "A-001" y rol "Administrador"
    Y no existe un estudiante registrado con documento "1001234567"
    Cuando el Administrador registra al estudiante con documento "1001234567", nombre "Laura Gómez", programa "Ingeniería de Sistemas" y correo "laura.gomez@ucaldas.edu.co" desde la IP "10.0.0.20" con agente "Chrome"
    Entonces el sistema guarda el Estudiante con esos datos
    Y el sistema confirma al Administrador el registro del estudiante "1001234567"
    Y el registro queda en la bitácora como exitoso con quién "A-001", qué "registrar_estudiante", cuándo, IP "10.0.0.20" y agente "Chrome"

  Escenario: El registro no guarda contraseña ni datos académicos (ADR-004, ADR-007, RT-03)
    Dado un usuario autenticado con SSO con documento "A-001" y rol "Administrador"
    Cuando el Administrador registra al estudiante con documento "1001234567", nombre "Laura Gómez", programa "Ingeniería de Sistemas" y correo "laura.gomez@ucaldas.edu.co"
    Entonces el Estudiante guardado solo contiene documento, nombre, programa y correo
    Y no se guarda ninguna contraseña, porque el estudiante inicia sesión con el SSO institucional
    Y no se copian datos académicos, porque se consultan al SIA cuando se necesitan

  Escenario: Rechazo por documento ya registrado
    Dado un usuario autenticado con SSO con documento "A-001" y rol "Administrador"
    Y ya existe un estudiante registrado con documento "1001234567"
    Cuando el Administrador intenta registrar otro estudiante con documento "1001234567" y nombre "Laura G."
    Entonces el sistema rechaza el registro indicando que ya existe un estudiante con documento "1001234567"
    Y el estudiante existente conserva el nombre "Laura Gómez"
    Y el intento queda registrado en la bitácora como fallido

  Escenario: Rol no autorizado para registrar estudiantes (ADR-005)
    Dado un usuario autenticado con SSO con documento "C-001" y rol "Coordinador"
    Cuando el usuario intenta registrar al estudiante con documento "1001234567"
    Entonces el sistema deniega el registro indicando que el rol "Coordinador" no tiene permiso para registrar estudiantes
    Y no se guarda ningún estudiante
    Y el intento queda registrado en la bitácora como fallido

  Escenario: Rechazo por datos obligatorios incompletos
    Dado un usuario autenticado con SSO con documento "A-001" y rol "Administrador"
    Cuando el Administrador intenta registrar al estudiante con documento "1001234567", nombre "" (vacío), programa "Ingeniería de Sistemas" y correo "laura.gomez@ucaldas.edu.co"
    Entonces el sistema rechaza el registro indicando que el nombre es obligatorio
    Y no se guarda ningún estudiante
    Y el intento queda registrado en la bitácora como fallido
