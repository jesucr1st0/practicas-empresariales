from src.modulos.horas.aplicacion.consultar_horas_supervisor import ConsultarHorasSupervisor
from src.modulos.horas.aplicacion.dto import RegistroHorasDTO, ResultadoValidacionDTO
from src.modulos.horas.aplicacion.validar_horas_supervisor import ValidarHorasSupervisor
from src.modulos.identidad_accesos.aplicacion.gestor_enlaces_acceso import GestorEnlacesAcceso


class ControladorAccesoExternoHoras:
    def __init__(
        self,
        gestor_enlaces: GestorEnlacesAcceso,
        caso_uso_consultar: ConsultarHorasSupervisor,
        caso_uso_validar: ValidarHorasSupervisor,
    ):
        self._gestor_enlaces = gestor_enlaces
        self._caso_uso_consultar = caso_uso_consultar
        self._caso_uso_validar = caso_uso_validar

    def consultar_horas_pendientes(
        self,
        token: str,
        ip: str,
        agente_usuario: str,
    ) -> list[RegistroHorasDTO]:
        enlace = self._gestor_enlaces.validar_token(token, ip, agente_usuario)
        return self._caso_uso_consultar.ejecutar(enlace.practica_id)

    def validar_horas(
        self,
        token: str,
        ip: str,
        agente_usuario: str,
    ) -> ResultadoValidacionDTO:
        enlace = self._gestor_enlaces.validar_token(token, ip, agente_usuario)
        return self._caso_uso_validar.ejecutar(enlace.practica_id)
