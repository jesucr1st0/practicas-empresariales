from collections.abc import Callable
from typing import Any

from src.modulos.practicas.aplicacion.consultar_empresa import ConsultarEmpresa
from src.modulos.practicas.aplicacion.dto_empresa import (
    DetalleEmpresaDTO,
    RegistrarEmpresaDTO,
    ResultadoEmpresaDTO,
)
from src.modulos.practicas.aplicacion.registrar_empresa import RegistrarEmpresa


class ControladorEmpresa:
    """Controlador de entrada para CU-10: Registrar empresa."""

    ROLES_AUTORIZADOS = {"Coordinador de prácticas", "Administrador"}

    def __init__(
        self,
        caso_uso_registrar: RegistrarEmpresa,
        caso_uso_consultar: ConsultarEmpresa,
        registrar_acceso: Callable[..., None] | Any | None = None,
    ) -> None:
        self._caso_uso_registrar = caso_uso_registrar
        self._caso_uso_consultar = caso_uso_consultar
        self._registrar_acceso_callback = registrar_acceso

    def registrar_empresa(
        self,
        dto: RegistrarEmpresaDTO,
        usuario_id: str,
        rol: str,
        ip: str = "127.0.0.1",
        agente_usuario: str = "Interfaz web interna",
    ) -> ResultadoEmpresaDTO:
        if rol not in self.ROLES_AUTORIZADOS:
            self._registrar(
                sujeto=usuario_id,
                accion="CU-10: registrar empresa",
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=False,
                detalle=f"Acceso denegado: el rol {rol!r} no tiene permisos para registrar empresas.",
            )
            raise PermissionError("Solo el Coordinador de prácticas o Administrador puede registrar empresas.")

        try:
            resultado = self._caso_uso_registrar.ejecutar(dto)
            self._registrar(
                sujeto=usuario_id,
                accion="CU-10: registrar empresa",
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=True,
                detalle=f"Empresa '{dto.nit}' registrada exitosamente con {resultado.supervisores_registrados} supervisor(es).",
            )
            return resultado
        except ValueError as error:
            self._registrar(
                sujeto=usuario_id,
                accion="CU-10: registrar empresa",
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=False,
                detalle=str(error),
            )
            raise

    def consultar_por_nit(
        self,
        nit: str,
        usuario_id: str,
        rol: str,
        ip: str = "127.0.0.1",
        agente_usuario: str = "Interfaz web interna",
    ) -> DetalleEmpresaDTO:
        if rol not in self.ROLES_AUTORIZADOS:
            self._registrar(
                sujeto=usuario_id,
                accion="CU-10: consultar empresa",
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=False,
                detalle=f"Acceso denegado: el rol {rol!r} no tiene permisos para consultar empresas.",
            )
            raise PermissionError("Solo el Coordinador de prácticas o Administrador puede consultar empresas.")

        try:
            resultado = self._caso_uso_consultar.ejecutar(nit)
            self._registrar(
                sujeto=usuario_id,
                accion="CU-10: consultar empresa",
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=True,
                detalle=f"Consulta exitosa de la empresa '{nit}'.",
            )
            return resultado
        except LookupError as error:
            self._registrar(
                sujeto=usuario_id,
                accion="CU-10: consultar empresa",
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
