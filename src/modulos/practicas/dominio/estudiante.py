from dataclasses import dataclass


@dataclass(frozen=True)
class Estudiante:
    """Datos maestros del estudiante.

    No guarda contraseña (ADR-004: inicia sesión con SSO) ni datos académicos
    (ADR-007: se consultan al SIA, no se replican).
    """

    documento: str
    nombre: str
    programa: str
    correo: str

    def __post_init__(self) -> None:
        for campo in ("documento", "nombre", "programa", "correo"):
            if not getattr(self, campo).strip():
                raise ValueError(f"El {campo} del estudiante es obligatorio")
