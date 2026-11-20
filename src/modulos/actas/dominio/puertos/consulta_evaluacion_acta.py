from abc import ABC, abstractmethod
from uuid import UUID


class ConsultaEvaluacionActa(ABC):
    @abstractmethod
    def obtener_calificacion_evaluacion(self, practica_id: UUID) -> float | None:
        pass
