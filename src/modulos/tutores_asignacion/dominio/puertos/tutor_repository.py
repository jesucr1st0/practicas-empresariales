from typing import Protocol

from src.modulos.tutores_asignacion.dominio.tutor import Tutor


class TutorRepository(Protocol):
    def guardar(self, tutor: Tutor) -> None: ...

    def obtener_por_documento(self, documento: str) -> Tutor | None: ...
