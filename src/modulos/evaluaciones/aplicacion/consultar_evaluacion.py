from uuid import UUID

from src.modulos.evaluaciones.aplicacion.dto import EvaluacionDTO
from src.modulos.evaluaciones.dominio.puertos.evaluacion_repository import (
    EvaluacionRepository,
)


class ConsultarEvaluacion:
    def __init__(self, repositorio: EvaluacionRepository):
        self._repositorio = repositorio

    def ejecutar(self, practica_id: UUID) -> EvaluacionDTO | None:
        evaluacion = self._repositorio.buscar_por_practica(practica_id)
        if evaluacion is None:
            return None
        return EvaluacionDTO(
            id=evaluacion.id,
            practica_id=evaluacion.practica_id,
            fecha=evaluacion.fecha,
            calificacion=evaluacion.calificacion,
            observaciones=evaluacion.observaciones,
        )
