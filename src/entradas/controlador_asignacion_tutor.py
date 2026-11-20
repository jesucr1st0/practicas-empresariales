from collections.abc import Callable
from uuid import UUID

from src.modulos.tutores_asignacion.aplicacion.confirmar_asignacion import ConfirmarAsignacion
from src.modulos.tutores_asignacion.aplicacion.confirmar_asignacion_dto import ConfirmarAsignacionDTO
from src.modulos.tutores_asignacion.aplicacion.resultado_asignacion_dto import ResultadoAsignacionDTO
from src.modulos.tutores_asignacion.aplicacion.sugerir_tutor import SugerirTutor
from src.modulos.tutores_asignacion.aplicacion.sugerencia_tutor_dto import SugerenciaTutorDTO


class ControladorAsignacionTutor:
    ROL_COORDINADOR = "Coordinador de prácticas"

    def __init__(
        self,
        sugerir_tutor: SugerirTutor,
        confirmar_asignacion: ConfirmarAsignacion,
        registrar_acceso: Callable[[str, str], None],
    ) -> None:
        self._sugerir_tutor = sugerir_tutor
        self._confirmar_asignacion = confirmar_asignacion
        self._registrar_acceso = registrar_acceso

    def sugerir(
        self,
        practica_id: UUID,
        usuario_id: str,
        rol: str,
    ) -> SugerenciaTutorDTO:
        self._registrar_acceso(usuario_id, "CU-01: solicitar sugerencia de tutor")
        self._validar_rol(rol)
        return self._sugerir_tutor.ejecutar(practica_id)

    def confirmar(
        self,
        solicitud: ConfirmarAsignacionDTO,
        usuario_id: str,
        rol: str,
    ) -> ResultadoAsignacionDTO:
        self._registrar_acceso(usuario_id, "CU-01: confirmar asignación de tutor")
        self._validar_rol(rol)
        return self._confirmar_asignacion.ejecutar(solicitud)

    @classmethod
    def _validar_rol(cls, rol: str) -> None:
        if rol != cls.ROL_COORDINADOR:
            raise PermissionError("Solo el Coordinador de prácticas puede asignar tutores.")
