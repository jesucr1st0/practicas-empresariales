from src.modulos.tutores_asignacion.dominio.datos_academicos_tutor import DatosAcademicosTutor
from src.modulos.tutores_asignacion.dominio.puertos.consulta_academica_tutor import (
    ConsultaAcademicaTutor,
    SIAError,
    SIATimeoutError,
)


class AdaptadorSIATutorMemoria(ConsultaAcademicaTutor):
    """Adaptador en memoria simulado para consultar datos académicos de tutores en el SIA (ADR-007)."""

    def __init__(self) -> None:
        self._docentes: dict[str, DatosAcademicosTutor] = {}
        self._simular_timeout: bool = False
        self._simular_error: bool = False

    def configurar_docente(
        self,
        documento: str,
        departamento: str,
        categoria: str,
        dedicacion: str,
        disponible_sia: bool = True,
        mensaje_estado: str = "",
    ) -> None:
        self._docentes[documento] = DatosAcademicosTutor(
            departamento=departamento,
            categoria=categoria,
            dedicacion=dedicacion,
            disponible_sia=disponible_sia,
            mensaje_estado=mensaje_estado,
        )

    def simular_timeout(self, activo: bool = True) -> None:
        self._simular_timeout = activo

    def simular_error(self, activo: bool = True) -> None:
        self._simular_error = activo

    def consultar_docente(
        self,
        tutor_documento: str,
        timeout_segundos: float = 10.0,
    ) -> DatosAcademicosTutor:
        if self._simular_timeout:
            raise SIATimeoutError(
                f"El servicio del SIA no respondió dentro de los {timeout_segundos} segundos (timeout)."
            )

        if self._simular_error:
            raise SIAError("El servicio de consulta docente del SIA no se encuentra disponible.")

        if tutor_documento in self._docentes:
            return self._docentes[tutor_documento]

        # Si no está preconfigurado pero el SIA está operativo, retornar datos por defecto
        return DatosAcademicosTutor(
            departamento="Departamento Académico General",
            categoria="Docente",
            dedicacion="Tiempo Completo",
            disponible_sia=True,
            mensaje_estado="Datos docentes sincronizados desde el SIA.",
        )
