from typing import Protocol

from src.modulos.practicas.dominio.datos_academicos_estudiante import DatosAcademicosEstudiante


class SIATimeoutError(Exception):
    """Error cuando el servicio del SIA no responde dentro del tiempo límite de 10 segundos."""
    pass


class SIAError(Exception):
    """Error general de comunicación o caída en los servicios del SIA."""
    pass


class ConsultaAcademicaEstudiante(Protocol):
    """Puerto para consultar información académica de estudiantes en el SIA (ADR-007, RT-03)."""

    def consultar_academica(
        self,
        estudiante_documento: str,
        timeout_segundos: float = 10.0,
    ) -> DatosAcademicosEstudiante:
        ...
