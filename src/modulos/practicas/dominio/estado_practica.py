from enum import Enum


class EstadoPractica(str, Enum):
    REGISTRADA = "registrada"
    EN_CURSO = "en curso"
    FINALIZADA = "finalizada"
    CERRADA = "cerrada"
