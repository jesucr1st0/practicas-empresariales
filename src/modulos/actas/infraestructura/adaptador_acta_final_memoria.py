from uuid import UUID

from src.modulos.actas.dominio.acta_final import ActaFinal
from src.modulos.actas.dominio.estado_acta import EstadoActa
from src.modulos.actas.dominio.puertos.acta_final_repository import (
    ActaFinalRepository,
)


class AdaptadorActaFinalMemoria(ActaFinalRepository):
    def __init__(self, actas_iniciales: list[ActaFinal] | None = None):
        self._actas: dict[UUID, ActaFinal] = {}
        if actas_iniciales:
            for a in actas_iniciales:
                self._actas[a.id] = a

    def guardar(self, acta: ActaFinal) -> None:
        self._actas[acta.id] = acta

    def buscar_por_id(self, id: UUID) -> ActaFinal | None:
        return self._actas.get(id)

    def buscar_vigente_por_practica(self, practica_id: UUID) -> ActaFinal | None:
        for a in self._actas.values():
            if a.practica_id == practica_id and a.estado == EstadoActa.VIGENTE:
                return a
        return None

    def listar_por_practica(self, practica_id: UUID) -> list[ActaFinal]:
        return [a for a in self._actas.values() if a.practica_id == practica_id]
