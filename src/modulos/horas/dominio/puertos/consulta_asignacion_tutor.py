from abc import ABC, abstractmethod
from uuid import UUID


class ConsultaAsignacionTutor(ABC):
    @abstractmethod
    def esta_asignado(self, tutor_documento: str, practica_id: UUID) -> bool:
        pass
