from typing import Protocol
from uuid import UUID


class ServicioConsultaPostulacion(Protocol):
    def postulacion_esta_verificada(self, postulacion_id: UUID) -> bool:
        ...
