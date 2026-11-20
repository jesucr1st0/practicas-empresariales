from uuid import UUID

from src.modulos.evaluaciones.dominio.evaluacion import Evaluacion
from src.modulos.evaluaciones.dominio.puertos.evaluacion_repository import (
    EvaluacionRepository,
)


class AdaptadorEvaluacionMemoria(EvaluacionRepository):
    def __init__(self, evaluaciones_iniciales: list[Evaluacion] | None = None):
        self._evaluaciones: dict[UUID, Evaluacion] = {}
        if evaluaciones_iniciales:
            for e in evaluaciones_iniciales:
                self._evaluaciones[e.practica_id] = e

    def guardar(self, evaluacion: Evaluacion) -> None:
        self._evaluaciones[evaluacion.practica_id] = evaluacion

    def buscar_por_practica(self, practica_id: UUID) -> Evaluacion | None:
        return self._evaluaciones.get(practica_id)

    def existe_para_practica(self, practica_id: UUID) -> bool:
        return practica_id in self._evaluaciones
