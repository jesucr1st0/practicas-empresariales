from abc import ABC, abstractmethod

from src.modulos.identidad_accesos.dominio.enlace_acceso import EnlaceAcceso


class EnlaceAccesoRepository(ABC):
    @abstractmethod
    def guardar(self, enlace: EnlaceAcceso) -> None:
        pass

    @abstractmethod
    def buscar_por_hash(self, token_hash: str) -> EnlaceAcceso | None:
        pass
