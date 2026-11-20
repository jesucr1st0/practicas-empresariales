from typing import Protocol

from src.modulos.tutores_asignacion.dominio.datos_academicos_tutor import DatosAcademicosTutor


class SIATimeoutError(Exception):
    """Error cuando el servicio del SIA no responde dentro del tiempo límite de 10 segundos."""
    pass


class SIAError(Exception):
    """Error general de comunicación o caída en los servicios del SIA."""
    pass


class ConsultaAcademicaTutor(Protocol):
    """Puerto para consultar datos institucionales/docentes de tutores en el SIA (ADR-007, RT-03)."""

    def consultar_docente(
        self,
        tutor_documento: str,
        timeout_segundos: float = 10.0,
    ) -> DatosAcademicosTutor:
        ...
