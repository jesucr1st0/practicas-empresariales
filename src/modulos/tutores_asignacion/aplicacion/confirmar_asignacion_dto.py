from dataclasses import dataclass
from uuid import UUID

from src.modulos.tutores_asignacion.dominio.origen_asignacion import OrigenAsignacion


@dataclass(frozen=True, slots=True)
class ConfirmarAsignacionDTO:
    practica_id: UUID
    tutor_documento: str
    origen: OrigenAsignacion
    confirmar_sobrecupo: bool = False
    observaciones: str | None = None
