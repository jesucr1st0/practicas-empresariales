from src.modulos.identidad_accesos.aplicacion.autorizador_accesos import (
    AutorizadorAccesos,
)
from src.modulos.identidad_accesos.dominio.rol import Rol
from src.modulos.identidad_accesos.dominio.usuario_autenticado import (
    UsuarioAutenticado,
)
from src.modulos.tutores_asignacion.aplicacion.registrar_tutor import RegistrarTutor
from src.modulos.tutores_asignacion.aplicacion.registrar_tutor_dto import (
    RegistrarTutorDTO,
)
from src.modulos.tutores_asignacion.aplicacion.resultado_tutor_dto import (
    ResultadoTutorDTO,
)


class ControladorTutor:
    """Interfaz web interna para CU-09: aplica rol y bitácora (ADR-005)."""

    ACCION = "registrar_tutor"
    ROLES_PERMITIDOS = (Rol.ADMINISTRADOR,)

    def __init__(
        self,
        caso_uso_registrar: RegistrarTutor,
        autorizador: AutorizadorAccesos,
    ) -> None:
        self._caso_uso_registrar = caso_uso_registrar
        self._autorizador = autorizador

    def registrar_tutor(
        self,
        usuario: UsuarioAutenticado,
        documento: str,
        nombre: str,
        correo: str,
        programa: str,
        ip: str,
        agente_usuario: str,
    ) -> ResultadoTutorDTO:
        self._autorizador.verificar_rol(
            usuario, self.ROLES_PERMITIDOS, self.ACCION, ip, agente_usuario
        )

        dto = RegistrarTutorDTO(
            documento=documento, nombre=nombre, correo=correo, programa=programa
        )
        try:
            resultado = self._caso_uso_registrar.ejecutar(dto)
        except ValueError as error:
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
            f"Tutor {resultado.documento} registrado",
        )
        return resultado
