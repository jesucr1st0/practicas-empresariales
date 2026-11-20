from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Supervisor:
    """Persona de la empresa que valida horas y evalúa al estudiante (ADR-006, RN-04)."""
    empresa_nit: str
    nombre: str
    correo: str
    telefono: str = ""
    activo: bool = True
    id: UUID = field(default_factory=uuid4)
