from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class PostulacionDTO:
    estudiante_documento: str
    programa: str
    correo_estudiante: str = ""


@dataclass(frozen=True)
class ResultadoPostulacionDTO:
    id: UUID
    estudiante_documento: str
    programa: str
    estado: str
    fecha_creacion: datetime
    mensaje: str
    motivo_rechazo: str | None = None
