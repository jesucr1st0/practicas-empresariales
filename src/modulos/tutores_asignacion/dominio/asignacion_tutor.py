from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.modulos.tutores_asignacion.dominio.origen_asignacion import OrigenAsignacion


@dataclass(slots=True)
class AsignacionTutor:
    practica_id: UUID
    tutor_documento: str
    id: UUID = field(default_factory=uuid4)
    fecha: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    vigente: bool = True
    origen: OrigenAsignacion = OrigenAsignacion.MANUAL
    observaciones: str | None = None

    def desactivar(self) -> None:
        self.vigente = False
