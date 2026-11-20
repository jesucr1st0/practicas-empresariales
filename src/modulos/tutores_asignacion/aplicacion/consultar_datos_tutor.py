from src.modulos.tutores_asignacion.aplicacion.dto_consulta_tutor import (
    DatosTutorDTO,
    PracticaAsignadaDTO,
)
from src.modulos.tutores_asignacion.dominio.puertos.asignacion_repository import AsignacionRepository
from src.modulos.tutores_asignacion.dominio.puertos.consulta_academica_tutor import (
    ConsultaAcademicaTutor,
    SIAError,
    SIATimeoutError,
)
from src.modulos.tutores_asignacion.dominio.puertos.consulta_regla_tutor import ConsultaReglaTutor


class ConsultarDatosTutor:
    """Caso de uso CU-11: Consultar datos de un tutor académico."""

    def __init__(
        self,
        asignaciones: AsignacionRepository,
        reglas: ConsultaReglaTutor,
        servicio_sia: ConsultaAcademicaTutor,
    ) -> None:
        self._asignaciones = asignaciones
        self._reglas = reglas
        self._servicio_sia = servicio_sia

    def ejecutar(
        self,
        tutor_documento: str,
        version_regla: str | None = None,
    ) -> DatosTutorDTO:
        tutor = self._asignaciones.obtener_tutor_por_documento(tutor_documento)
        if tutor is None:
            raise LookupError(f"No se encontró el tutor con documento {tutor_documento!r}.")

        # Obtener asignaciones vigentes y calcular carga
        asignaciones_vigentes = self._asignaciones.obtener_asignaciones_vigentes_por_tutor(
            tutor.documento
        )
        carga_actual = len(asignaciones_vigentes)

        # Determinar capacidad máxima por regla
        if version_regla:
            capacidad_maxima = self._reglas.obtener_capacidad_maxima_por_tutor(version_regla)
        else:
            try:
                capacidad_maxima = self._reglas.obtener_capacidad_maxima_programa(tutor.programa)
            except Exception:
                capacidad_maxima = 10  # Capacidad estándar de contingencia si no hay regla específica

        # Consultar datos docentes en el SIA con tolerancia a fallos (ADR-007, EAC-03)
        try:
            datos_academicos = self._servicio_sia.consultar_docente(tutor.documento)
            departamento = datos_academicos.departamento
            categoria = datos_academicos.categoria
            dedicacion = datos_academicos.dedicacion
            disponible_sia = datos_academicos.disponible_sia
            mensaje_sia = (
                datos_academicos.mensaje_estado
                or "Datos académicos sincronizados correctamente desde el SIA."
            )
        except (SIATimeoutError, SIAError, Exception) as error:
            departamento = "No disponible"
            categoria = "No disponible"
            dedicacion = "No disponible"
            disponible_sia = False
            mensaje_sia = f"Datos institucionales del SIA no disponibles temporalmente ({error})."

        cupos_disponibles = max(0, capacidad_maxima - carga_actual)
        sobrecupo = carga_actual >= capacidad_maxima

        practicas_asignadas = tuple(
            PracticaAsignadaDTO(
                practica_id=asignacion.practica_id,
                fecha_asignacion=asignacion.fecha,
                origen=(
                    asignacion.origen.value
                    if hasattr(asignacion.origen, "value")
                    else str(asignacion.origen)
                ),
                vigente=asignacion.vigente,
            )
            for asignacion in asignaciones_vigentes
        )

        return DatosTutorDTO(
            documento=tutor.documento,
            nombre=tutor.nombre,
            correo=tutor.correo,
            programa=tutor.programa,
            activo=tutor.activo,
            departamento=departamento,
            categoria=categoria,
            dedicacion=dedicacion,
            disponible_sia=disponible_sia,
            mensaje_sia=mensaje_sia,
            carga_actual=carga_actual,
            capacidad_maxima=capacidad_maxima,
            cupos_disponibles=cupos_disponibles,
            sobrecupo=sobrecupo,
            practicas_asignadas=practicas_asignadas,
        )
