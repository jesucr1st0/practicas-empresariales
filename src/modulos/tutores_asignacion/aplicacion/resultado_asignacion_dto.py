from dataclasses import dataclass

from src.modulos.tutores_asignacion.dominio.asignacion_tutor import AsignacionTutor


@dataclass(frozen=True, slots=True)
class ResultadoAsignacionDTO:
    asignacion: AsignacionTutor | None
    advertencia_sobrecupo: bool
    mensaje_advertencia: str | None = None
