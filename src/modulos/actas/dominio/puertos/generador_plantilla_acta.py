from abc import ABC, abstractmethod
from datetime import datetime


class GeneradorPlantillaActa(ABC):
    @abstractmethod
    def generar_documento(
        self,
        programa: str,
        estudiante_nombre: str,
        estudiante_documento: str,
        empresa_nombre: str,
        version_regla: str,
        horas_validadas: int,
        calificacion: float,
        fecha_emision: datetime,
    ) -> tuple[bytes, str]:
        """Genera el contenido binario del acta con la plantilla oficial y retorna (bytes, huella_sha256)."""
        pass
