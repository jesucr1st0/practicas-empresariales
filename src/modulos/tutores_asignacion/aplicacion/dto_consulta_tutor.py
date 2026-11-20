from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True, slots=True)
class PracticaAsignadaDTO:
    practica_id: UUID
    fecha_asignacion: date
    origen: str
    vigente: bool


@dataclass(frozen=True, slots=True)
class DatosTutorDTO:
    documento: str
    nombre: str
    correo: str
    programa: str
    activo: bool
    departamento: str
    categoria: str
    dedicacion: str
    disponible_sia: bool
    mensaje_sia: str
    carga_actual: int
    capacidad_maxima: int
    cupos_disponibles: int
    sobrecupo: bool
    practicas_asignadas: tuple[PracticaAsignadaDTO, ...]


@dataclass(frozen=True, slots=True)
class ResumenTutorDTO:
    documento: str
    nombre: str
    correo: str
    programa: str
    activo: bool
    carga_actual: int
    capacidad_maxima: int
    cupos_disponibles: int
    sobrecupo: bool
