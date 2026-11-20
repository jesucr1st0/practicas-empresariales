from uuid import UUID

from src.modulos.actas.dominio.puertos.consulta_practica_acta import (
    ConsultaPracticaActa,
    DatosPracticaActa,
)


class AdaptadorConsultaPracticaMemoria(ConsultaPracticaActa):
    def __init__(self, practicas: dict[UUID, DatosPracticaActa] | None = None):
        self._practicas: dict[UUID, DatosPracticaActa] = practicas or {}

    def agregar_practica(self, datos: DatosPracticaActa) -> None:
        self._practicas[datos.practica_id] = datos

    def consultar_practica(self, practica_id: UUID) -> DatosPracticaActa | None:
        return self._practicas.get(practica_id)
