# language: es
# Traza: CU-09, CU-01, ADR-005, ADR-004, ADR-012, ADR-001, RN-01

Característica: Registrar tutor
  Como Administrador
  quiero registrar los datos maestros de un tutor académico
  para que quede disponible como tutor activo de su programa y pueda ser asignado a prácticas (CU-01).

  # [NECESITA ACLARACIÓN: drivers.md no fija los datos maestros del tutor. Se usan los atributos de la
  #  entidad Tutor ya existente en el Módulo Tutores y asignación (spec 001): documento, nombre,
  #  correo, programa y activo.]

  Escenario: Registro exitoso de un tutor (flujo básico)
    Dado un usuario autenticado con SSO con documento "A-001" y rol "Administrador"
    Y no existe un tutor registrado con documento "T-010"
    Cuando el Administrador registra al tutor con documento "T-010", nombre "María López", correo "maria.lopez@ucaldas.edu.co" y programa "Ingeniería de Sistemas" desde la IP "10.0.0.20" con agente "Chrome"
    Entonces el sistema guarda el Tutor con esos datos en estado activo
    Y el sistema confirma al Administrador el registro del tutor "T-010"
    Y el registro queda en la bitácora como exitoso con quién "A-001", qué "registrar_tutor", cuándo, IP "10.0.0.20" y agente "Chrome"

  Escenario: El registro no guarda contraseña (ADR-004)
    Dado un usuario autenticado con SSO con documento "A-001" y rol "Administrador"
    Cuando el Administrador registra al tutor con documento "T-010", nombre "María López", correo "maria.lopez@ucaldas.edu.co" y programa "Ingeniería de Sistemas"
    Entonces el Tutor guardado solo contiene documento, nombre, correo, programa y activo
    Y no se guarda ninguna contraseña, porque el tutor inicia sesión con el SSO institucional

  Escenario: Rechazo por documento ya registrado
    Dado un usuario autenticado con SSO con documento "A-001" y rol "Administrador"
    Y ya existe un tutor registrado con documento "T-010" y nombre "María López"
    Cuando el Administrador intenta registrar otro tutor con documento "T-010" y nombre "M. López"
    Entonces el sistema rechaza el registro indicando que ya existe un tutor con documento "T-010"
    Y el tutor existente conserva el nombre "María López"
    Y el intento queda registrado en la bitácora como fallido

  Escenario: Rol no autorizado para registrar tutores (ADR-005)
    Dado un usuario autenticado con SSO con documento "C-001" y rol "Coordinador"
    Cuando el usuario intenta registrar al tutor con documento "T-010"
    Entonces el sistema deniega el registro indicando que el rol "Coordinador" no tiene permiso para registrar tutores
    Y no se guarda ningún tutor
    Y el intento queda registrado en la bitácora como fallido

  Escenario: Rechazo por datos obligatorios incompletos
    Dado un usuario autenticado con SSO con documento "A-001" y rol "Administrador"
    Cuando el Administrador intenta registrar al tutor con documento "T-010", nombre "María López", correo "maria.lopez@ucaldas.edu.co" y programa "" (vacío)
    Entonces el sistema rechaza el registro indicando que el programa es obligatorio
    Y no se guarda ningún tutor
    Y el intento queda registrado en la bitácora como fallido
