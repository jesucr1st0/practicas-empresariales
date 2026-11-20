from uuid import UUID

from src.modulos.actas.dominio.puertos.consulta_evaluacion_acta import (
    ConsultaEvaluacionActa,
)


class AdaptadorConsultaEvaluacionMemoria(ConsultaEvaluacionActa):
    def __init__(self, evaluaciones: dict[UUID, float] | None = None):
        self._evaluaciones: dict[UUID, float] = evaluaciones or {}

    def registrar_evaluacion(self, practica_id: UUID, calificacion: float) -> None:
        self._evaluaciones[practica_id] = calificacion

    def obtener_calificacion_evaluacion(self, practica_id: UUID) -> float | None:
        return self._evaluaciones.get(practica_id)
