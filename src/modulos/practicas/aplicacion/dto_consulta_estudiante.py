from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class DatosEstudianteDTO:
    estudiante_documento: str
    tiene_practica_activa: bool
    practica_id: UUID | None
    programa: str | None
    estado_practica: str | None
    periodo: str | None
    empresa_id: str | None
    supervisor_id: str | None
    tutor_documento: str | None
    horas_minimas_exigidas: int | None
    creditos_aprobados: int | None
    promedio_acumulado: float | None
    semestre_actual: int | None
    matricula_activa: bool | None
    disponible_sia: bool
    mensaje_sia: str


@dataclass(frozen=True, slots=True)
class ResumenEstudianteDTO:
    estudiante_documento: str
    programa: str
    practica_id: UUID
    estado_practica: str
    tutor_documento: str | None
