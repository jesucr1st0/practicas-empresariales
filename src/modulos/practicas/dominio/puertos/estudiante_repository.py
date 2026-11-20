from typing import Protocol

from src.modulos.practicas.dominio.estudiante import Estudiante


class EstudianteRepository(Protocol):
    def guardar(self, estudiante: Estudiante) -> None:
        ...

    def obtener_por_documento(self, documento: str) -> Estudiante | None:
        ...
