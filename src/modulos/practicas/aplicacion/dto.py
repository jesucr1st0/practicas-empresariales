from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True)
class RegistrarPracticaDTO:
    estudiante_documento: str
    programa: str
    empresa_id: str
    supervisor_id: str
    periodo: str
    fecha_inicio: date
    fecha_fin: date
    postulacion_id: UUID | None = None
    fecha_registro: date | None = None


@dataclass(frozen=True)
class ResultadoPracticaDTO:
    id: UUID
    estudiante_documento: str
    programa: str
    estado: str
    regla_version: str
    horas_minimas_exigidas: int
    postulacion_id: UUID | None
