from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Tutor:
    documento: str
    nombre: str
    correo: str
    programa: str
    activo: bool = True
