from uuid import UUID

from src.modulos.practicas.dominio.estado_practica import EstadoPractica
from src.modulos.practicas.dominio.practica import Practica
from src.modulos.practicas.dominio.puertos.practica_repository import PracticaRepository


class AdaptadorPracticaMemoria(PracticaRepository):
    def __init__(self) -> None:
        self._practicas: dict[UUID, Practica] = {}

    def guardar(self, practica: Practica) -> None:
        self._practicas[practica.id] = practica

    def obtener_por_id(self, practica_id: UUID) -> Practica | None:
        return self._practicas.get(practica_id)

    def obtener_activa_por_estudiante(self, estudiante_documento: str) -> Practica | None:
        for p in self._practicas.values():
            if p.estudiante_documento == estudiante_documento and p.estado in (
                EstadoPractica.REGISTRADA,
                EstadoPractica.EN_CURSO,
            ):
                return p
        return None

    def obtener_por_estudiante(self, estudiante_documento: str) -> list[Practica]:
        return [
            p for p in self._practicas.values()
            if p.estudiante_documento == estudiante_documento
        ]

    def listar_por_tutor(self, tutor_documento: str) -> list[Practica]:
        return [
            p for p in self._practicas.values()
            if p.tutor_documento == tutor_documento
        ]

    def listar_todas(self) -> list[Practica]:
        return list(self._practicas.values())
