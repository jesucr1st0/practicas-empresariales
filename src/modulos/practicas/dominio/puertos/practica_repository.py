from typing import Protocol
from uuid import UUID

from src.modulos.practicas.dominio.practica import Practica


class PracticaRepository(Protocol):
    def guardar(self, practica: Practica) -> None:
        ...

    def obtener_por_id(self, practica_id: UUID) -> Practica | None:
        ...

    def obtener_activa_por_estudiante(self, estudiante_documento: str) -> Practica | None:
        ...

    def obtener_por_estudiante(self, estudiante_documento: str) -> list[Practica]:
        ...

    def listar_por_tutor(self, tutor_documento: str) -> list[Practica]:
        ...

    def listar_todas(self) -> list[Practica]:
        ...
