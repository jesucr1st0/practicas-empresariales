from src.modulos.practicas.dominio.estudiante import Estudiante
from src.modulos.practicas.dominio.puertos.estudiante_repository import (
    EstudianteRepository,
)


class AdaptadorEstudianteMemoria(EstudianteRepository):
    def __init__(self) -> None:
        self._estudiantes: dict[str, Estudiante] = {}

    def guardar(self, estudiante: Estudiante) -> None:
        self._estudiantes[estudiante.documento] = estudiante

    def obtener_por_documento(self, documento: str) -> Estudiante | None:
        return self._estudiantes.get(documento)
