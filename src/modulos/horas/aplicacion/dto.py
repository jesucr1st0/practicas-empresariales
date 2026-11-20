from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True)
class RegistrarHorasDTO:
    practica_id: UUID
    estudiante_documento: str
    fecha: date
    cantidad_horas: int
    evidencia: str


@dataclass(frozen=True)
class RegistroHorasDTO:
    id: UUID
    practica_id: UUID
    estudiante_documento: str
    fecha: date
    cantidad_horas: int
    evidencia: str
    estado_validacion: str


@dataclass(frozen=True)
class ResumenHorasTutorDTO:
    practica_id: UUID
    total_horas: int
    horas_validadas: int
    horas_pendientes: int
    registros: list[RegistroHorasDTO]


@dataclass(frozen=True)
class ValidarHorasDTO:
    token: str
    practica_id: UUID
    ip: str
    agente_usuario: str


@dataclass(frozen=True)
class ResultadoValidacionDTO:
    exitoso: bool
    mensaje: str
    horas_validadas: int
