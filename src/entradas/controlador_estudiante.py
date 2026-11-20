from src.modulos.identidad_accesos.aplicacion.autorizador_accesos import (
    AutorizadorAccesos,
)
from src.modulos.identidad_accesos.dominio.rol import Rol
from src.modulos.identidad_accesos.dominio.usuario_autenticado import (
    UsuarioAutenticado,
)
from src.modulos.practicas.aplicacion.registrar_estudiante import RegistrarEstudiante
from src.modulos.practicas.aplicacion.registrar_estudiante_dto import (
    RegistrarEstudianteDTO,
)
from src.modulos.practicas.aplicacion.resultado_estudiante_dto import (
    ResultadoEstudianteDTO,
)


class ControladorEstudiante:
    """Interfaz web interna para CU-08: aplica rol y bitácora (ADR-005)."""

    ACCION = "registrar_estudiante"
    ROLES_PERMITIDOS = (Rol.ADMINISTRADOR,)

    def __init__(
        self,
        caso_uso_registrar: RegistrarEstudiante,
        autorizador: AutorizadorAccesos,
    ) -> None:
        self._caso_uso_registrar = caso_uso_registrar
        self._autorizador = autorizador

    def registrar_estudiante(
        self,
        usuario: UsuarioAutenticado,
        documento: str,
        nombre: str,
        programa: str,
        correo: str,
        ip: str,
        agente_usuario: str,
    ) -> ResultadoEstudianteDTO:
        self._autorizador.verificar_rol(
            usuario, self.ROLES_PERMITIDOS, self.ACCION, ip, agente_usuario
        )

        dto = RegistrarEstudianteDTO(
            documento=documento, nombre=nombre, programa=programa, correo=correo
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
            f"Estudiante {resultado.documento} registrado",
        )
        return resultado
