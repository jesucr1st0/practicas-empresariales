from collections.abc import Iterable

from src.modulos.identidad_accesos.dominio.puertos.bitacora_acceso_repository import (
    BitacoraAccesoRepository,
)
from src.modulos.identidad_accesos.dominio.registro_acceso import RegistroAcceso
from src.modulos.identidad_accesos.dominio.rol import Rol
from src.modulos.identidad_accesos.dominio.usuario_autenticado import (
    UsuarioAutenticado,
)


class AutorizadorAccesos:
    """Autorización por roles y registro en la bitácora de solo inserción (ADR-005, RN-01)."""

    def __init__(self, bitacora: BitacoraAccesoRepository):
        self._bitacora = bitacora

    def verificar_rol(
        self,
        usuario: UsuarioAutenticado,
        roles_permitidos: Iterable[Rol],
        accion: str,
        ip: str,
        agente_usuario: str,
    ) -> None:
        if usuario.rol not in set(roles_permitidos):
            motivo = (
                f"Acceso denegado: el rol '{usuario.rol.value}' no tiene permiso para '{accion}'"
            )
            self.registrar(usuario, accion, ip, agente_usuario, False, motivo)
            raise PermissionError(motivo)

    def registrar(
        self,
        usuario: UsuarioAutenticado,
        accion: str,
        ip: str,
        agente_usuario: str,
        exitoso: bool,
        detalle: str,
    ) -> None:
        self._bitacora.registrar(
            RegistroAcceso(
                sujeto=usuario.documento,
                accion=accion,
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=exitoso,
                detalle=detalle,
            )
        )
