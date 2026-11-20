from abc import ABC, abstractmethod
from uuid import UUID


class ConsultaHorasActa(ABC):
    @abstractmethod
    def obtener_horas_validadas(self, practica_id: UUID) -> int:
        pass
