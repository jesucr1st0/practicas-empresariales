from enum import Enum


class EstadoActa(str, Enum):
    VIGENTE = "vigente"
    ANULADA = "anulada"
