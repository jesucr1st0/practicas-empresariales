from typing import Protocol
from uuid import UUID
from src.modulos.postulaciones.dominio.postulacion import Postulacion


class PostulacionRepository(Protocol):
    def guardar(self, postulacion: Postulacion) -> None:
        ...

    def obtener_por_id(self, postulacion_id: UUID) -> Postulacion | None:
        ...

    def obtener_activa_por_estudiante(self, estudiante_documento: str) -> Postulacion | None:
        ...

    def listar_pendientes(self) -> list[Postulacion]:
        ...
