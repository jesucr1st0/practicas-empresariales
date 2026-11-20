from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResultadoTutorDTO:
    documento: str
    nombre: str
    correo: str
    programa: str
    activo: bool
