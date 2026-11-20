from enum import Enum


class EstadoPostulacion(str, Enum):
    PENDIENTE_VERIFICACION = "pendiente de verificación"
    VERIFICADA = "verificada"
    RECHAZADA = "rechazada"
    REVISION_MANUAL = "revisión manual"
