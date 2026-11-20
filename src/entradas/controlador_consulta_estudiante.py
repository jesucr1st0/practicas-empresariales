from collections.abc import Callable
from typing import Any

from src.modulos.practicas.aplicacion.consultar_datos_estudiante import ConsultarDatosEstudiante
from src.modulos.practicas.aplicacion.dto_consulta_estudiante import DatosEstudianteDTO


class ControladorConsultaEstudiante:
    """Controlador de entrada para CU-12: Consultar datos estudiante con regla de alcance y bitácora."""

    ROLES_AUTORIZADOS = {"Coordinador de prácticas", "Administrador", "Tutor"}

    def __init__(
        self,
        caso_uso_consultar: ConsultarDatosEstudiante,
        registrar_acceso: Callable[..., None] | Any | None = None,
    ) -> None:
        self._caso_uso_consultar = caso_uso_consultar
        self._registrar_acceso_callback = registrar_acceso

    def consultar_estudiante(
        self,
        estudiante_documento: str,
        usuario_id: str,
        rol: str,
        tutor_documento: str | None = None,
        ip: str = "127.0.0.1",
        agente_usuario: str = "Interfaz web interna",
    ) -> DatosEstudianteDTO:
        if rol not in self.ROLES_AUTORIZADOS:
            self._registrar(
                sujeto=usuario_id,
                accion="CU-12: consultar datos estudiante",
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=False,
                detalle=f"Acceso denegado: el rol {rol!r} no tiene permisos para consultar datos de estudiantes.",
            )
            raise PermissionError("Solo el Coordinador de prácticas o Tutor académico puede consultar estudiantes.")

        try:
            resultado = self._caso_uso_consultar.ejecutar(
                estudiante_documento=estudiante_documento,
                rol=rol,
                tutor_documento=tutor_documento,
            )
            self._registrar(
                sujeto=usuario_id,
                accion="CU-12: consultar datos estudiante",
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=True,
                detalle=f"Consulta exitosa del estudiante {estudiante_documento}.",
            )
            return resultado
        except (PermissionError, ValueError, LookupError) as error:
            self._registrar(
                sujeto=usuario_id,
                accion="CU-12: consultar datos estudiante",
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=False,
                detalle=str(error),
            )
            raise

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
