from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class DatosPracticaActa:
    practica_id: UUID
    version_regla: str
    programa: str
    estudiante_documento: str
    estudiante_nombre: str
    empresa_nombre: str


class ConsultaPracticaActa(ABC):
    @abstractmethod
    def consultar_practica(self, practica_id: UUID) -> DatosPracticaActa | None:
        pass
