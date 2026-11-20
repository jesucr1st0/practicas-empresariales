from collections.abc import Sequence

from src.modulos.tutores_asignacion.aplicacion.dto_consulta_tutor import ResumenTutorDTO
from src.modulos.tutores_asignacion.dominio.puertos.asignacion_repository import AsignacionRepository
from src.modulos.tutores_asignacion.dominio.puertos.consulta_regla_tutor import ConsultaReglaTutor


class ListarTutoresPrograma:
    """Caso de uso para consultar el listado consolidado de tutores por programa (CU-11, ADR-012)."""

    def __init__(
        self,
        asignaciones: AsignacionRepository,
        reglas: ConsultaReglaTutor,
    ) -> None:
        self._asignaciones = asignaciones
        self._reglas = reglas

    def ejecutar(
        self,
        programa: str,
        version_regla: str | None = None,
    ) -> Sequence[ResumenTutorDTO]:
        tutores = self._asignaciones.listar_tutores_activos(programa)

        if version_regla:
            capacidad_maxima = self._reglas.obtener_capacidad_maxima_por_tutor(version_regla)
        else:
            try:
                capacidad_maxima = self._reglas.obtener_capacidad_maxima_programa(programa)
            except Exception:
                capacidad_maxima = 10

        resumenes = []
        for tutor in tutores:
            carga = self._asignaciones.contar_asignaciones_vigentes_por_tutor(tutor.documento)
            cupos = max(0, capacidad_maxima - carga)
            sobrecupo = carga >= capacidad_maxima
            resumenes.append(
                ResumenTutorDTO(
                    documento=tutor.documento,
                    nombre=tutor.nombre,
                    correo=tutor.correo,
                    programa=tutor.programa,
                    activo=tutor.activo,
                    carga_actual=carga,
                    capacidad_maxima=capacidad_maxima,
                    cupos_disponibles=cupos,
                    sobrecupo=sobrecupo,
                )
            )

        return tuple(resumenes)
