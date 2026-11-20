from src.modulos.practicas.dominio.datos_academicos_estudiante import DatosAcademicosEstudiante
from src.modulos.practicas.dominio.puertos.consulta_academica_estudiante import (
    ConsultaAcademicaEstudiante,
    SIAError,
    SIATimeoutError,
)


class AdaptadorSIAEstudianteMemoria(ConsultaAcademicaEstudiante):
    """Adaptador simulado en memoria para consultar datos académicos de estudiantes en el SIA (ADR-007)."""

    def __init__(self) -> None:
        self._estudiantes: dict[str, DatosAcademicosEstudiante] = {}
        self._simular_timeout: bool = False
        self._simular_error: bool = False

    def configurar_estudiante(
        self,
        documento: str,
        creditos_aprobados: int,
        promedio_acumulado: float,
        semestre_actual: int,
        matricula_activa: bool = True,
        disponible_sia: bool = True,
        mensaje_estado: str = "",
    ) -> None:
        self._estudiantes[documento] = DatosAcademicosEstudiante(
            creditos_aprobados=creditos_aprobados,
            promedio_acumulado=promedio_acumulado,
            semestre_actual=semestre_actual,
            matricula_activa=matricula_activa,
            disponible_sia=disponible_sia,
            mensaje_estado=mensaje_estado,
        )

    def simular_timeout(self, activo: bool = True) -> None:
        self._simular_timeout = activo

    def simular_error(self, activo: bool = True) -> None:
        self._simular_error = activo

    def consultar_academica(
        self,
        estudiante_documento: str,
        timeout_segundos: float = 10.0,
    ) -> DatosAcademicosEstudiante:
        if self._simular_timeout:
            raise SIATimeoutError(
                f"El servicio del SIA no respondió dentro de los {timeout_segundos} segundos (timeout)."
            )

        if self._simular_error:
            raise SIAError("El servicio de consulta académica del SIA no se encuentra disponible.")

        if estudiante_documento in self._estudiantes:
            return self._estudiantes[estudiante_documento]

        return DatosAcademicosEstudiante(
            creditos_aprobados=120,
            promedio_acumulado=4.0,
            semestre_actual=8,
            matricula_activa=True,
            disponible_sia=True,
            mensaje_estado="Datos académicos sincronizados desde el SIA.",
        )
