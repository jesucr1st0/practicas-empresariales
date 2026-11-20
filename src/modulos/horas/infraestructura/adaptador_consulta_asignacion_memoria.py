from uuid import UUID

from src.modulos.horas.dominio.puertos.consulta_asignacion_tutor import ConsultaAsignacionTutor


class AdaptadorConsultaAsignacionMemoria(ConsultaAsignacionTutor):
    def __init__(self, asignaciones_iniciales: dict[tuple[str, UUID], bool] | None = None):
        # Mapea (tutor_documento, practica_id) -> bool
        self._asignaciones: dict[tuple[str, UUID], bool] = asignaciones_iniciales or {}

    def asignar(self, tutor_documento: str, practica_id: UUID) -> None:
        self._asignaciones[(tutor_documento, practica_id)] = True

    def desasignar(self, tutor_documento: str, practica_id: UUID) -> None:
        self._asignaciones.pop((tutor_documento, practica_id), None)

    def esta_asignado(self, tutor_documento: str, practica_id: UUID) -> bool:
        return self._asignaciones.get((tutor_documento, practica_id), False)
