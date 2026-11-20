from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True)
class RegistrarEvaluacionDTO:
    token: str
    practica_id: UUID
    fecha: date
    calificacion: float
    observaciones: str


@dataclass(frozen=True)
class EvaluacionDTO:
    id: UUID
    practica_id: UUID
    fecha: date
    calificacion: float
    observaciones: str


@dataclass(frozen=True)
class ResultadoEvaluacionDTO:
    exitoso: bool
    mensaje: str
    evaluacion_id: UUID | None = None
