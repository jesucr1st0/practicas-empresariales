from uuid import UUID

from src.modulos.actas.aplicacion.dto import ResultadoExportacionDTO
from src.modulos.actas.aplicacion.exportar_acta_final import ExportarActaFinal
from src.modulos.identidad_accesos.aplicacion.autorizador_accesos import (
    AutorizadorAccesos,
)
from src.modulos.identidad_accesos.dominio.rol import Rol
from src.modulos.identidad_accesos.dominio.usuario_autenticado import (
    UsuarioAutenticado,
)


class ControladorExportarActa:
    """Interfaz web interna para CU-07: aplica rol, alcance y bitácora (ADR-005)."""

    ACCION = "exportar_acta"
    ROLES_PERMITIDOS = (Rol.COORDINADOR, Rol.ESTUDIANTE)

    def __init__(
        self,
        caso_uso_exportar: ExportarActaFinal,
        autorizador: AutorizadorAccesos,
    ):
        self._caso_uso_exportar = caso_uso_exportar
        self._autorizador = autorizador

    def exportar_acta(
        self,
        usuario: UsuarioAutenticado,
        practica_id: UUID,
        ip: str,
        agente_usuario: str,
    ) -> ResultadoExportacionDTO:
        self._autorizador.verificar_rol(
            usuario, self.ROLES_PERMITIDOS, self.ACCION, ip, agente_usuario
        )

        estudiante_documento = (
            usuario.documento if usuario.rol == Rol.ESTUDIANTE else None
        )
        try:
            resultado = self._caso_uso_exportar.ejecutar(
                practica_id, estudiante_documento=estudiante_documento
            )
        except (PermissionError, ValueError, FileNotFoundError) as error:
            self._autorizador.registrar(
                usuario, self.ACCION, ip, agente_usuario, False, str(error)
            )
            raise

        self._autorizador.registrar(
            usuario,
            self.ACCION,
            ip,
            agente_usuario,
            True,
            f"Acta final exportada para la práctica {practica_id}",
        )
        return resultado
