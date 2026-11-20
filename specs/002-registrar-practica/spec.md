# language: es
# Traza: CU-02, EAC-01, ADR-001, ADR-009

Característica: Registrar práctica empresarial
  Como Coordinador de prácticas o Estudiante
  quiero registrar una nueva práctica empresarial vinculando estudiante, empresa, supervisor y fechas
  para formalizar la práctica y fijar de manera inmutable la versión de regla del programa que gobernará su desarrollo.

  Antecedentes:
    Dado que el sistema tiene programas académicos y sus versiones de reglas registradas

  Escenario: Registro exitoso fijando la regla vigente del programa (flujo básico)
    Dado el programa "Ingeniería de Sistemas" con una regla "v1" vigente que exige 480 horas mínimas
    Y un estudiante con documento "1002345678" sin práctica activa
    Cuando el Coordinador registra una práctica para el estudiante con fecha de inicio "2026-08-01", fin "2026-12-15", empresa "TechCorp" y supervisor "Carlos Perez"
    Entonces el sistema resuelve y asigna la versión de regla "v1" con 480 horas mínimas a la práctica
    Y la Práctica queda guardada en estado "registrada"
    Y la referencia a la regla "v1" queda fijada de forma permanente en la práctica

  Escenario: Registro a partir de una postulación verificada
    Dado un estudiante que cuenta con una Postulación previa en estado "verificada"
    Cuando se registra la práctica asociando el identificador de dicha postulación
    Entonces el sistema valida que la postulación está en estado "verificada"
    Y crea la Práctica en estado "registrada" asociando el identificador de la postulación
    Y fija la versión de regla vigente correspondiente al programa

  Escenario: Intento de registro con postulación no verificada
    Dado un estudiante con una Postulación en estado "pendiente de verificación" o "rechazada"
    Cuando se intenta registrar una práctica vinculando dicha postulación
    Entonces el sistema rechaza la operación
    Y emite un mensaje indicando que la postulación debe estar verificada previamente
    Y no se crea ninguna práctica en el sistema

  Escenario: Programa sin versión de regla vigente configurada
    Dado un programa "Ingeniería Biomédica" que no tiene ninguna versión de regla registrada para la fecha
    Cuando se intenta registrar una práctica para un estudiante de dicho programa
    Entonces el sistema detiene el registro
    Y notifica un error de configuración indicando que no existe versión de regla vigente para el programa
    Y no se crea ninguna práctica

  Escenario: Inmutabilidad de la regla en prácticas registradas ante cambios futuros (EAC-01 / ADR-009)
    Dado una práctica registrada previamente para "Ingeniería de Sistemas" asociada a la regla "v1" (480 horas)
    Cuando el Consejo aprueba y se registra una nueva versión de regla "v2" con 540 horas mínimas con vigencia posterior
    Entonces la práctica previamente registrada conserva inmutable su referencia a la regla "v1" con 480 horas mínimas
    Y una nueva práctica registrada bajo la nueva fecha adopta la regla "v2" con 540 horas mínimas
    Y 0 prácticas en curso son alteradas por la nueva regla
