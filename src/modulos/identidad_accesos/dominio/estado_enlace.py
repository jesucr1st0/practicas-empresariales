from enum import Enum


class EstadoEnlace(str, Enum):
    VIGENTE = "vigente"
    USADO = "usado"
    VENCIDO = "vencido"
    REVOCADO = "revocado"
