from abc import ABC, abstractmethod
from uuid import UUID

from src.modulos.actas.dominio.acta_final import ActaFinal


class ActaFinalRepository(ABC):
    @abstractmethod
    def guardar(self, acta: ActaFinal) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, id: UUID) -> ActaFinal | None:
        pass

    @abstractmethod
    def buscar_vigente_por_practica(self, practica_id: UUID) -> ActaFinal | None:
        pass

    @abstractmethod
    def listar_por_practica(self, practica_id: UUID) -> list[ActaFinal]:
        pass
