# language: es
# Traza: CU-05, EAC-02, ADR-005, ADR-006, ADR-013, RN-04, OB-05

Característica: Evaluar al estudiante por la empresa
  Como supervisor de empresa
  quiero acceder mediante un enlace de un solo uso sin contraseña y registrar la evaluación del estudiante
  para certificar su desempeño en la práctica empresarial garantizando la integridad e invalidación del enlace.

  Escenario: Evaluación exitosa por el supervisor sin cuenta ni contraseña (flujo básico, EAC-02, RN-04)
    Dado un supervisor de empresa con un enlace de acceso vigente para la práctica "P-100" con acción "evaluar"
    Y la práctica "P-100" se encuentra en curso o finalizada y aún no cuenta con evaluación registrada
    Cuando el supervisor abre el enlace desde un celular con IP "190.85.12.34" y agente "Mobile Safari"
    Entonces el sistema registra el acceso en la bitácora (quién, qué, cuándo, IP y agente)
    Y permite al supervisor diligenciar la evaluación sin solicitar credenciales ni contraseñas
    Cuando el supervisor envía la evaluación con calificación 4.5 y observaciones "Excelente desempeño técnico y puntualidad"
    Entonces el sistema registra la Evaluacion para la práctica "P-100"
    Y actualiza el estado en la práctica indicando evaluación recibida
    Y el enlace de acceso pasa inmediatamente a estado "usado" quedando invalidado para usos posteriores
    Y el supervisor recibe confirmación de registro exitoso

  Escenario: Envío de recordatorio periódico de evaluación pendiente (ADR-013)
    Dado una práctica "P-100" con enlace vigente cuya evaluación está pendiente
    Cuando el planificador de tareas ejecuta la verificación de recordatorios
    Entonces el sistema envía un correo institucional de recordatorio al supervisor con el enlace de acceso
    Y el envío queda registrado en la bitácora de notificaciones

  Escenario: Intento de reenvío con enlace ya usado (ADR-006, EAC-02)
    Dado un enlace de acceso que ya fue utilizado para registrar la evaluación de la práctica "P-100"
    Cuando el supervisor o un tercero intenta acceder nuevamente con dicho enlace desde la IP "190.85.12.34"
    Entonces el sistema registra el intento no autorizado en la bitácora
    Y deniega el acceso mostrando el mensaje "enlace no disponible; pida al coordinador que lo reemita"
    Y no permite enviar una nueva evaluación

  Escenario: Acceso con enlace vencido por tiempo superior a 30 días (ADR-006)
    Dado un enlace emitido hace más de 30 días para la práctica "P-100"
    Cuando el supervisor intenta abrir el enlace
    Entonces el sistema registra el acceso denegado en la bitácora
    Y muestra el mensaje "enlace no disponible; pida al coordinador que lo reemita"
    Y no permite registrar la evaluación

  Escenario: Intento de registrar una segunda evaluación en una práctica que ya tiene evaluación
    Dado que la práctica "P-100" ya tiene una Evaluacion registrada
    Cuando se intenta registrar una nueva evaluación para la misma práctica
    Entonces el sistema rechaza la solicitud porque solo se permite una evaluación por práctica
