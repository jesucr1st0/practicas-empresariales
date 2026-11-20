from dataclasses import dataclass


@dataclass(frozen=True)
class ResultadoEstudianteDTO:
    documento: str
    nombre: str
    programa: str
    correo: str
