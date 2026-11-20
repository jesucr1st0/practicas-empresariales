from enum import Enum


class Rol(str, Enum):
    """Roles del sistema (ADR-005)."""

    ESTUDIANTE = "Estudiante"
    TUTOR = "Tutor"
    COORDINADOR = "Coordinador"
    ADMINISTRADOR = "Administrador"
    SUPERVISOR_EXTERNO = "Supervisor externo"
