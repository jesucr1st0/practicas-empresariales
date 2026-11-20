from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class GenerarActaDTO:
    practica_id: UUID


@dataclass(frozen=True)
class ActaFinalDTO:
    id: UUID
    practica_id: UUID
    fecha_emision: datetime
    huella_integridad: str
    estado: str
    version_regla: str
    horas_validadas: int
    calificacion_evaluacion: float
    ruta_archivo: str
    plantilla_version: str


@dataclass(frozen=True)
class ResultadoExportacionDTO:
    contenido: bytes
    huella_integridad: str
    nombre_archivo: str
