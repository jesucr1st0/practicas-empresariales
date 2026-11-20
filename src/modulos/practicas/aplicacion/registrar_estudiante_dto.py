from dataclasses import dataclass


@dataclass(frozen=True)
class RegistrarEstudianteDTO:
    documento: str
    nombre: str
    programa: str
    correo: str
