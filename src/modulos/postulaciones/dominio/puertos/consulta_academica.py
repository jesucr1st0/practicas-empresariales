from typing import Protocol
from dataclasses import dataclass


@dataclass(frozen=True)
class ResultadoConsultaAcademica:
    cumple_requisitos: bool
    motivo: str | None = None


class SIATimeoutError(Exception):
    """Error cuando el SIA no responde dentro del tiempo límite de 10 segundos."""
    pass


class SIAError(Exception):
    """Error general de comunicación con el servicio del SIA."""
    pass


class ConsultaAcademica(Protocol):
    def verificar_requisitos(
        self,
        estudiante_documento: str,
        programa: str,
        timeout_segundos: float = 10.0,
    ) -> ResultadoConsultaAcademica:
        ...
