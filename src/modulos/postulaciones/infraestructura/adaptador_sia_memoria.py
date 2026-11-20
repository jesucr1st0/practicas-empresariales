from src.modulos.postulaciones.dominio.puertos.consulta_academica import (
    ConsultaAcademica,
    ResultadoConsultaAcademica,
    SIATimeoutError,
    SIAError,
)


class AdaptadorSIAMemoria(ConsultaAcademica):
    """Adaptador simulado para integración con el SIA (ADR-007).

    Permite configurar estudiantes que cumplen requisitos, los que tienen deudas/faltantes,
    y simular caídas/timeout del SIA para validar EAC-03.
    """

    def __init__(self) -> None:
        self._estudiantes_aptos: set[str] = set()
        self._motivos_rechazo: dict[str, str] = {}
        self._simular_timeout: bool = False
        self._simular_caida: bool = False

    def configurar_estudiante_apto(self, estudiante_documento: str) -> None:
        self._estudiantes_aptos.add(estudiante_documento)
        self._motivos_rechazo.pop(estudiante_documento, None)

    def configurar_estudiante_rechazado(self, estudiante_documento: str, motivo: str) -> None:
        self._estudiantes_aptos.discard(estudiante_documento)
        self._motivos_rechazo[estudiante_documento] = motivo

    def simular_timeout(self, activo: bool = True) -> None:
        self._simular_timeout = activo

    def simular_caida(self, activo: bool = True) -> None:
        self._simular_caida = activo

    def verificar_requisitos(
        self,
        estudiante_documento: str,
        programa: str,
        timeout_segundos: float = 10.0,
    ) -> ResultadoConsultaAcademica:
        if self._simular_timeout:
            raise SIATimeoutError(f"El SIA no respondió dentro del límite de {timeout_segundos} segundos.")

        if self._simular_caida:
            raise SIAError("El servicio del SIA no está disponible.")

        if estudiante_documento in self._estudiantes_aptos:
            return ResultadoConsultaAcademica(cumple_requisitos=True)

        motivo = self._motivos_rechazo.get(
            estudiante_documento,
            "El estudiante no cumple con los créditos mínimos requeridos o tiene deudas pendientes."
        )
        return ResultadoConsultaAcademica(cumple_requisitos=False, motivo=motivo)
