from uuid import UUID

from src.modulos.tutores_asignacion.aplicacion.sugerencia_tutor_dto import SugerenciaTutorDTO
from src.modulos.tutores_asignacion.dominio.puertos.asignacion_repository import AsignacionRepository
from src.modulos.tutores_asignacion.dominio.puertos.consulta_practica_asignacion import (
    ConsultaPracticaAsignacion,
)
from src.modulos.tutores_asignacion.dominio.puertos.consulta_regla_tutor import ConsultaReglaTutor


class SugerirTutor:
    def __init__(
        self,
        asignaciones: AsignacionRepository,
        practicas: ConsultaPracticaAsignacion,
        reglas: ConsultaReglaTutor,
    ) -> None:
        self._asignaciones = asignaciones
        self._practicas = practicas
        self._reglas = reglas

    def ejecutar(self, practica_id: UUID) -> SugerenciaTutorDTO:
        programa = self._practicas.obtener_programa(practica_id)
        version_regla = self._practicas.obtener_version_regla(practica_id)
        capacidad = self._reglas.obtener_capacidad_maxima_por_tutor(version_regla)
        if capacidad <= 0:
            raise ValueError("La capacidad máxima por tutor debe ser mayor que cero.")

        tutores = self._asignaciones.listar_tutores_activos(programa)
        if not tutores:
            raise LookupError(f"No hay tutores activos para el programa {programa!r}.")

        tutor = min(
            tutores,
            key=lambda candidato: self._asignaciones.contar_asignaciones_vigentes_por_tutor(
                candidato.documento
            ),
        )
        carga = self._asignaciones.contar_asignaciones_vigentes_por_tutor(tutor.documento)
        return SugerenciaTutorDTO(
            practica_id=practica_id,
            tutor_documento=tutor.documento,
            tutor_nombre=tutor.nombre,
            carga_actual=carga,
            capacidad_maxima=capacidad,
            advertencia_sobrecupo=carga >= capacidad,
        )
