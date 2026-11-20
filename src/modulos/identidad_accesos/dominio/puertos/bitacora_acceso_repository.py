from abc import ABC, abstractmethod

from src.modulos.identidad_accesos.dominio.registro_acceso import RegistroAcceso


class BitacoraAccesoRepository(ABC):
    @abstractmethod
    def registrar(self, registro: RegistroAcceso) -> None:
        """Bitácora de solo inserción (ADR-005, RN-01)."""
        pass

    @abstractmethod
    def listar(self) -> list[RegistroAcceso]:
        pass
