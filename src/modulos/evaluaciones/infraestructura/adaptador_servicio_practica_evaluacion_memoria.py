from uuid import UUID

from src.modulos.evaluaciones.dominio.puertos.servicio_actualizacion_practica_evaluacion import (
    ServicioActualizacionPracticaEvaluacion,
)


class AdaptadorServicioPracticaEvaluacionMemoria(
    ServicioActualizacionPracticaEvaluacion
):
    def __init__(self) -> None:
        self.practicas_evaluadas: set[UUID] = set()

    def registrar_evaluacion_recibida(self, practica_id: UUID) -> None:
        self.practicas_evaluadas.add(practica_id)
