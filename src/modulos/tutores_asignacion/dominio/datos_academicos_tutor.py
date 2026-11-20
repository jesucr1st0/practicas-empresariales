from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DatosAcademicosTutor:
    """Información académica y docente del tutor provista por los servicios del SIA (ADR-007)."""
    departamento: str
    categoria: str
    dedicacion: str
    disponible_sia: bool = True
    mensaje_estado: str = ""
