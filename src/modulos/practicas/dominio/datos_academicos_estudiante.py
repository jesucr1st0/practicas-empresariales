from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DatosAcademicosEstudiante:
    """Información académica del estudiante provista por los servicios del SIA (ADR-007, RT-03)."""
    creditos_aprobados: int
    promedio_acumulado: float
    semestre_actual: int
    matricula_activa: bool
    disponible_sia: bool = True
    mensaje_estado: str = ""
