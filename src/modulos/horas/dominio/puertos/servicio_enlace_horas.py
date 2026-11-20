from abc import ABC, abstractmethod
from uuid import UUID


class ServicioEnlaceHoras(ABC):
    @abstractmethod
    def emitir_enlace(self, practica_id: UUID, email_supervisor: str) -> str:
        """Emite un enlace seguro para el supervisor y retorna el token o URL completa."""
        pass
