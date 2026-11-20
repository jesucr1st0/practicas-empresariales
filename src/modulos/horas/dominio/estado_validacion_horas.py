from enum import Enum


class EstadoValidacionHoras(str, Enum):
    PENDIENTE = "pendiente"
    VALIDADO_SUPERVISOR = "validado"
    RECHAZADO = "rechazado"
