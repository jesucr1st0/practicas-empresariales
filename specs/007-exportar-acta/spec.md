# language: es
# Traza: CU-07, CU-06, PA-04, ADR-010, ADR-005, ADR-004, ADR-011, RN-01, RN-02

Característica: Exportar acta final
  Como Coordinador de prácticas o Estudiante
  quiero descargar el acta final ya generada de una práctica
  para disponer del documento oficial original y verificar que no ha sido alterado.

  Antecedentes:
    Dado una práctica "P-100" del estudiante con documento "1001234567"
    Y la práctica "P-100" tiene un ActaFinal en estado "vigente" generada en CU-06 con huella SHA-256 registrada

  Escenario: Exportación del acta vigente por el Coordinador (flujo básico, ADR-010)
    Dado un usuario autenticado con SSO con documento "C-001" y rol "Coordinador"
    Cuando el Coordinador solicita exportar el acta final de la práctica "P-100" desde la IP "10.0.0.15" con agente "Firefox"
    Entonces el sistema recupera el mismo documento almacenado al generar el acta en CU-06
    Y comprueba que la huella SHA-256 del archivo coincide con la huella registrada
    Y retorna el archivo "acta_final_<id de P-100>.pdf" para su descarga
    Y la exportación queda registrada en la bitácora como exitosa con quién "C-001", qué "exportar_acta", cuándo, IP "10.0.0.15" y agente "Firefox"

  Escenario: Exportación del acta por el estudiante titular de la práctica (ADR-005)
    Dado un usuario autenticado con SSO con documento "1001234567" y rol "Estudiante"
    Cuando el estudiante solicita exportar el acta final de la práctica "P-100"
    Entonces el sistema verifica que la práctica "P-100" pertenece al estudiante "1001234567"
    Y retorna el archivo del acta final con su huella de integridad
    Y la exportación queda registrada en la bitácora como exitosa

  Escenario: Estudiante intenta exportar el acta de una práctica ajena (ADR-005, RN-01)
    Dado un usuario autenticado con SSO con documento "1009999999" y rol "Estudiante"
    Cuando el estudiante solicita exportar el acta final de la práctica "P-100"
    Entonces el sistema deniega la exportación indicando que la práctica no está en su alcance
    Y no entrega ningún archivo
    Y el intento queda registrado en la bitácora como fallido

  Escenario: Rol no autorizado para exportar actas (ADR-005)
    Dado un usuario autenticado con SSO con documento "T-001" y rol "Tutor"
    Cuando el usuario solicita exportar el acta final de la práctica "P-100"
    Entonces el sistema deniega la exportación indicando que el rol "Tutor" no tiene permiso para exportar actas
    Y no entrega ningún archivo
    Y el intento queda registrado en la bitácora como fallido

  Escenario: Exportación después de una corrección del acta (ADR-010)
    Dado que la práctica "P-100" tiene un acta "anulada" y una nueva acta "vigente" generada por corrección
    Y un usuario autenticado con SSO con documento "C-001" y rol "Coordinador"
    Cuando el Coordinador solicita exportar el acta final de la práctica "P-100"
    Entonces el sistema retorna únicamente el documento del acta "vigente"
    Y la huella entregada es la del acta "vigente", no la del acta "anulada"

  Escenario: Práctica sin acta final vigente
    Dado una práctica "P-200" que aún no tiene acta final generada
    Y un usuario autenticado con SSO con documento "C-001" y rol "Coordinador"
    Cuando el Coordinador solicita exportar el acta final de la práctica "P-200"
    Entonces el sistema rechaza la exportación indicando que no existe un acta final vigente para la práctica
    Y el intento queda registrado en la bitácora como fallido

  Escenario: Archivo del acta alterado en el almacén (PA-04, ADR-010, ADR-011)
    Dado que el archivo almacenado del acta vigente de "P-100" fue modificado después de su generación
    Y un usuario autenticado con SSO con documento "C-001" y rol "Coordinador"
    Cuando el Coordinador solicita exportar el acta final de la práctica "P-100"
    Entonces el sistema detecta que la huella SHA-256 del archivo no coincide con la registrada
    Y no entrega el archivo alterado
    Y el intento queda registrado en la bitácora como fallido con el motivo de integridad
