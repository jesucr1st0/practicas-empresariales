from uuid import UUID

from src.modulos.actas.dominio.puertos.consulta_horas_acta import (
    ConsultaHorasActa,
)


class AdaptadorConsultaHorasMemoria(ConsultaHorasActa):
    def __init__(self, horas_por_practica: dict[UUID, int] | None = None):
        self._horas: dict[UUID, int] = horas_por_practica or {}

    def fijar_horas(self, practica_id: UUID, cantidad: int) -> None:
        self._horas[practica_id] = cantidad

    def obtener_horas_validadas(self, practica_id: UUID) -> int:
        return self._horas.get(practica_id, 0)
