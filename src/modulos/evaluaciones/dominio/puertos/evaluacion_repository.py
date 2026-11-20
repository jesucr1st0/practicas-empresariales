from abc import ABC, abstractmethod
from uuid import UUID

from src.modulos.evaluaciones.dominio.evaluacion import Evaluacion


class EvaluacionRepository(ABC):
    @abstractmethod
    def guardar(self, evaluacion: Evaluacion) -> None:
        pass

    @abstractmethod
    def buscar_por_practica(self, practica_id: UUID) -> Evaluacion | None:
        pass

    @abstractmethod
    def existe_para_practica(self, practica_id: UUID) -> bool:
        pass
