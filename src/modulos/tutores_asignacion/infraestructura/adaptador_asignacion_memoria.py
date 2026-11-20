from collections.abc import Iterable, Sequence
from uuid import UUID

from src.modulos.tutores_asignacion.dominio.asignacion_tutor import AsignacionTutor
from src.modulos.tutores_asignacion.dominio.tutor import Tutor


class AdaptadorAsignacionMemoria:
    def __init__(self, tutores: Iterable[Tutor] = ()) -> None:
        self._tutores = list(tutores)
        self._asignaciones: dict[UUID, AsignacionTutor] = {}

    def agregar_tutor(self, tutor: Tutor) -> None:
        self._tutores.append(tutor)

    def guardar(self, asignacion: AsignacionTutor) -> None:
        self._asignaciones[asignacion.id] = asignacion

    def obtener_vigente_por_practica(self, practica_id: UUID) -> AsignacionTutor | None:
        return next(
            (
                asignacion
                for asignacion in self._asignaciones.values()
                if asignacion.practica_id == practica_id and asignacion.vigente
            ),
            None,
        )

    def obtener_historial_por_practica(self, practica_id: UUID) -> Sequence[AsignacionTutor]:
        return tuple(
            asignacion
            for asignacion in self._asignaciones.values()
            if asignacion.practica_id == practica_id
        )

    def contar_asignaciones_vigentes_por_tutor(self, tutor_documento: str) -> int:
        return sum(
            asignacion.vigente and asignacion.tutor_documento == tutor_documento
            for asignacion in self._asignaciones.values()
        )

    def listar_tutores_activos(self, programa: str) -> Sequence[Tutor]:
        return tuple(
            tutor
            for tutor in self._tutores
            if tutor.activo and tutor.programa == programa
        )

    def obtener_tutor_por_documento(self, documento: str) -> Tutor | None:
        return next(
            (tutor for tutor in self._tutores if tutor.documento == documento),
            None,
        )

    def obtener_asignaciones_vigentes_por_tutor(
        self, tutor_documento: str
    ) -> Sequence[AsignacionTutor]:
        return tuple(
            asignacion
            for asignacion in self._asignaciones.values()
            if asignacion.vigente and asignacion.tutor_documento == tutor_documento
        )
