from collections.abc import Callable, Sequence
from typing import Any

from src.modulos.tutores_asignacion.aplicacion.consultar_datos_tutor import ConsultarDatosTutor
from src.modulos.tutores_asignacion.aplicacion.dto_consulta_tutor import (
    DatosTutorDTO,
    ResumenTutorDTO,
)
from src.modulos.tutores_asignacion.aplicacion.listar_tutores_programa import ListarTutoresPrograma


class ControladorConsultaTutor:
    """Controlador de entrada para el caso de uso CU-11: Consultar datos tutor."""

    ROL_COORDINADOR = "Coordinador de prácticas"

    def __init__(
        self,
        consultar_datos_tutor: ConsultarDatosTutor,
        listar_tutores_programa: ListarTutoresPrograma,
        registrar_acceso: Callable[..., None] | Any | None = None,
    ) -> None:
        self._consultar_datos_tutor = consultar_datos_tutor
        self._listar_tutores_programa = listar_tutores_programa
        self._registrar_acceso_callback = registrar_acceso

    def consultar_tutor(
        self,
        tutor_documento: str,
        usuario_id: str,
        rol: str,
        ip: str = "127.0.0.1",
        agente_usuario: str = "Interfaz web interna",
        version_regla: str | None = None,
    ) -> DatosTutorDTO:
        if rol != self.ROL_COORDINADOR:
            self._registrar(
                sujeto=usuario_id,
                accion="CU-11: consultar datos tutor",
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=False,
                detalle=f"Acceso denegado: el rol {rol!r} no tiene permisos para consultar datos de tutor.",
            )
            raise PermissionError("Solo el Coordinador de prácticas puede consultar los datos del tutor.")

        try:
            resultado = self._consultar_datos_tutor.ejecutar(
                tutor_documento=tutor_documento,
                version_regla=version_regla,
            )
            self._registrar(
                sujeto=usuario_id,
                accion="CU-11: consultar datos tutor",
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=True,
                detalle=f"Consulta exitosa de los datos del tutor {tutor_documento}.",
            )
            return resultado
        except LookupError as error:
            self._registrar(
                sujeto=usuario_id,
                accion="CU-11: consultar datos tutor",
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=False,
                detalle=str(error),
            )
            raise

    def listar_tutores_programa(
        self,
        programa: str,
        usuario_id: str,
        rol: str,
        ip: str = "127.0.0.1",
        agente_usuario: str = "Interfaz web interna",
        version_regla: str | None = None,
    ) -> Sequence[ResumenTutorDTO]:
        if rol != self.ROL_COORDINADOR:
            self._registrar(
                sujeto=usuario_id,
                accion="CU-11: listar tutores programa",
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=False,
                detalle=f"Acceso denegado: el rol {rol!r} no tiene permisos para consultar el listado de tutores.",
            )
            raise PermissionError("Solo el Coordinador de prácticas puede consultar el listado de tutores.")

        resultado = self._listar_tutores_programa.ejecutar(
            programa=programa,
            version_regla=version_regla,
        )
        self._registrar(
            sujeto=usuario_id,
            accion="CU-11: listar tutores programa",
            ip=ip,
            agente_usuario=agente_usuario,
            exitoso=True,
            detalle=f"Listado exitoso de {len(resultado)} tutores para el programa {programa}.",
        )
        return resultado

    def _registrar(
        self,
        sujeto: str,
        accion: str,
        ip: str,
        agente_usuario: str,
        exitoso: bool,
        detalle: str,
    ) -> None:
        if not self._registrar_acceso_callback:
            return

        if hasattr(self._registrar_acceso_callback, "registrar"):
            from src.modulos.identidad_accesos.dominio.registro_acceso import RegistroAcceso
            self._registrar_acceso_callback.registrar(
                RegistroAcceso(
                    sujeto=sujeto,
                    accion=accion,
                    ip=ip,
                    agente_usuario=agente_usuario,
                    exitoso=exitoso,
                    detalle=detalle,
                )
            )
            return

        try:
            self._registrar_acceso_callback(
                sujeto=sujeto,
                accion=accion,
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=exitoso,
                detalle=detalle,
            )
        except TypeError:
            try:
                self._registrar_acceso_callback(sujeto, accion, ip, agente_usuario, exitoso, detalle)
            except TypeError:
                self._registrar_acceso_callback(sujeto, accion)
