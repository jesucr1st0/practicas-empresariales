from abc import ABC, abstractmethod


class AlmacenArchivos(ABC):
    @abstractmethod
    def guardar_archivo(self, ruta: str, contenido: bytes) -> str:
        """Almacena un archivo de manera inmutable (ADR-010, ADR-011)."""
        pass

    @abstractmethod
    def obtener_archivo(self, ruta: str) -> bytes:
        """Recupera los bytes del archivo original."""
        pass
