from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SupervisorDTO:
    nombre: str
    correo: str
    telefono: str = ""


@dataclass(frozen=True, slots=True)
class RegistrarEmpresaDTO:
    nit: str
    razon_social: str
    sector: str = ""
    ciudad: str = ""
    supervisores: tuple[SupervisorDTO, ...] = ()


@dataclass(frozen=True, slots=True)
class ResultadoEmpresaDTO:
    empresa_id: UUID
    nit: str
    razon_social: str
    activa: bool
    supervisores_registrados: int


@dataclass(frozen=True, slots=True)
class DetalleSupervisorDTO:
    id: UUID
    nombre: str
    correo: str
    telefono: str
    activo: bool


@dataclass(frozen=True, slots=True)
class DetalleEmpresaDTO:
    id: UUID
    nit: str
    razon_social: str
    sector: str
    ciudad: str
    activa: bool
    supervisores: tuple[DetalleSupervisorDTO, ...]
