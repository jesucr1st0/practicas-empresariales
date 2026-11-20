from uuid import UUID

from src.modulos.tutores_asignacion.aplicacion.confirmar_asignacion_dto import ConfirmarAsignacionDTO
from src.modulos.tutores_asignacion.aplicacion.resultado_asignacion_dto import ResultadoAsignacionDTO
from src.modulos.tutores_asignacion.dominio.asignacion_tutor import AsignacionTutor
from src.modulos.tutores_asignacion.dominio.puertos.asignacion_repository import AsignacionRepository
from src.modulos.tutores_asignacion.dominio.puertos.consulta_practica_asignacion import (
    ConsultaPracticaAsignacion,
)
from src.modulos.tutores_asignacion.dominio.puertos.consulta_regla_tutor import ConsultaReglaTutor


class ConfirmarAsignacion:
    def __init__(
        self,
        asignaciones: AsignacionRepository,
        practicas: ConsultaPracticaAsignacion,
        reglas: ConsultaReglaTutor,
    ) -> None:
        self._asignaciones = asignaciones
        self._practicas = practicas
        self._reglas = reglas

    def ejecutar(self, solicitud: ConfirmarAsignacionDTO) -> ResultadoAsignacionDTO:
        programa = self._practicas.obtener_programa(solicitud.practica_id)
        version_regla = self._practicas.obtener_version_regla(solicitud.practica_id)
        capacidad = self._reglas.obtener_capacidad_maxima_por_tutor(version_regla)
        if capacidad <= 0:
            raise ValueError("La capacidad máxima por tutor debe ser mayor que cero.")

        tutor = next(
            (
                candidato
                for candidato in self._asignaciones.listar_tutores_activos(programa)
                if candidato.documento == solicitud.tutor_documento
            ),
            None,
        )
        if tutor is None:
            raise LookupError(
                f"No se encontró un tutor activo con documento {solicitud.tutor_documento!r} "
                f"para el programa {programa!r}."
            )

        asignacion_previa = self._asignaciones.obtener_vigente_por_practica(solicitud.practica_id)
        carga = self._asignaciones.contar_asignaciones_vigentes_por_tutor(tutor.documento)
        if (
            asignacion_previa is not None
            and asignacion_previa.tutor_documento == tutor.documento
        ):
            carga -= 1

        sobrecupo = carga >= capacidad
        mensaje = (
            f"El tutor ha alcanzado el límite de capacidad ({carga}/{capacidad})."
            if sobrecupo
            else None
        )
        if sobrecupo and not solicitud.confirmar_sobrecupo:
            return ResultadoAsignacionDTO(None, True, mensaje)

        observaciones = solicitud.observaciones
        if sobrecupo:
            nota_sobrecupo = f"Sobrecupo confirmado por el Coordinador: {carga}/{capacidad}."
            observaciones = (
                f"{observaciones}; {nota_sobrecupo}" if observaciones else nota_sobrecupo
            )

        if asignacion_previa is not None:
            asignacion_previa.desactivar()
            self._asignaciones.guardar(asignacion_previa)

        asignacion = AsignacionTutor(
            practica_id=solicitud.practica_id,
            tutor_documento=tutor.documento,
            origen=solicitud.origen,
            observaciones=observaciones,
        )
        self._asignaciones.guardar(asignacion)
        self._practicas.actualizar_tutor_vigente(solicitud.practica_id, tutor.documento)
        return ResultadoAsignacionDTO(asignacion, sobrecupo, mensaje)
