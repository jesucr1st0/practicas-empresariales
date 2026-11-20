from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegistrarTutorDTO:
    documento: str
    nombre: str
    correo: str
    programa: str
