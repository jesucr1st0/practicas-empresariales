# language: es
# Traza: CU-06, CU-07, OB-05, ADR-010, ADR-011, RN-02, RN-03, EAC-01

Característica: Generar acta final
  Como Coordinador de prácticas
  quiero generar y exportar el acta final de una práctica finalizada utilizando la plantilla oficial
  para oficializar el cierre con un documento inmutable, trazable y con huella de integridad.

  Antecedentes:
    Dado que el usuario autenticado tiene el rol "Coordinador de prácticas"

  Escenario: Generación exitosa de acta final (flujo básico, ADR-010, RN-03)
    Dado una práctica finalizada "P-100" con regla aplicada "v1" que exige 480 horas mínimas
    Y la práctica tiene 480 horas validadas registradas
    Y la práctica cuenta con la evaluación de la empresa con calificación 4.5
    Cuando el Coordinador solicita generar el acta final de la práctica "P-100"
    Entonces el sistema genera el documento del acta final a partir de la plantilla oficial versionada
    Y calcula la huella de integridad SHA-256 del documento generado
    Y almacena el documento en el almacén de archivos de manera inmutable
    Y crea un registro de ActaFinal en estado "vigente" con la huella, versión de regla "v1", 480 horas y calificación 4.5
    Y el Coordinador recibe la confirmación con los datos del acta emitida

  Escenario: Rechazo por horas validadas insuficientes
    Dado una práctica "P-100" con regla aplicada que exige 480 horas mínimas
    Y la práctica tiene únicamente 360 horas validadas
    Y la práctica cuenta con evaluación de la empresa
    Cuando el Coordinador solicita generar el acta final de la práctica "P-100"
    Entonces el sistema rechaza la generación del acta indicando que las horas validadas (360) son menores a las mínimas requeridas (480)
    Y no se crea ningún registro de acta ni archivo documental

  Escenario: Rechazo por evaluación de empresa pendiente
    Dado una práctica "P-100" con 480 horas validadas que superan el mínimo
    Pero la práctica aún no cuenta con evaluación registrada por parte de la empresa
    Cuando el Coordinador solicita generar el acta final de la práctica "P-100"
    Entonces el sistema rechaza la generación indicando que la evaluación de la empresa está pendiente
    Y no se crea ningún registro de acta

  Escenario: Corrección de acta final generando una nueva y anulando la anterior (ADR-010)
    Dado que la práctica "P-100" ya tiene un ActaFinal previa en estado "vigente"
    Cuando el Coordinador solicita generar una nueva acta por corrección de datos
    Entonces el sistema genera un nuevo documento de acta final con una nueva huella SHA-256
    Y el acta previa pasa automáticamente a estado "anulada" en el historial sin ser editada ni eliminada
    Y la nueva acta queda registrada en estado "vigente"
    Y el sistema conserva ambas actas en el repositorio y en el almacén de archivos

  Escenario: Exportar y verificar integridad del acta final (CU-07)
    Dado que existe un ActaFinal en estado "vigente" para la práctica "P-100"
    Cuando el usuario solicita exportar o descargar el acta final
    Entonces el sistema recupera el documento original almacenado
    Y comprueba que la huella SHA-256 del archivo coincide exactamente con la huella registrada
    Y retorna el archivo para su descarga
