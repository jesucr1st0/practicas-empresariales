from datetime import date
from uuid import UUID, uuid4


class Evaluacion:
    def __init__(
        self,
        practica_id: UUID,
        fecha: date,
        calificacion: float,
        observaciones: str,
        id: UUID | None = None,
    ):
        if not (0.0 <= calificacion <= 5.0):
            raise ValueError("La calificación debe estar entre 0.0 y 5.0")
        self.id = id or uuid4()
        self.practica_id = practica_id
        self.fecha = fecha
        self.calificacion = calificacion
        self.observaciones = observaciones
