from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SugerenciaTutorDTO:
    practica_id: UUID
    tutor_documento: str
    tutor_nombre: str
    carga_actual: int
    capacidad_maxima: int
    advertencia_sobrecupo: bool
