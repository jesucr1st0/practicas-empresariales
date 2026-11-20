from uuid import UUID

from src.modulos.evaluaciones.dominio.puertos.evaluacion_repository import (
    EvaluacionRepository,
)
from src.modulos.evaluaciones.dominio.puertos.servicio_recordatorio_evaluacion import (
    ServicioRecordatorioEvaluacion,
)


class EnviarRecordatorioEvaluacion:
    def __init__(
        self,
        repositorio: EvaluacionRepository,
        servicio_recordatorio: ServicioRecordatorioEvaluacion,
    ):
        self._repositorio = repositorio
        self._servicio_recordatorio = servicio_recordatorio

    def ejecutar(self, practica_id: UUID, email_supervisor: str, token: str) -> bool:
        if self._repositorio.existe_para_practica(practica_id):
            return False

        enlace_url = f"https://practicas.universidad.edu.co/evaluacion?token={token}"
        return self._servicio_recordatorio.enviar_recordatorio(email_supervisor, enlace_url)
