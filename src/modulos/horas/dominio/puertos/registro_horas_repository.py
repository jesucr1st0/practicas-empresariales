from abc import ABC, abstractmethod
from uuid import UUID

from src.modulos.horas.dominio.registro_horas import RegistroHoras


class RegistroHorasRepository(ABC):
    @abstractmethod
    def guardar(self, registro: RegistroHoras) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, id: UUID) -> RegistroHoras | None:
        pass

    @abstractmethod
    def listar_por_practica(self, practica_id: UUID) -> list[RegistroHoras]:
        pass
