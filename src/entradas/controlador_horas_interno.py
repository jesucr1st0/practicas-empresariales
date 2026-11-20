from uuid import UUID

from src.modulos.horas.aplicacion.consultar_horas_tutor import ConsultarHorasTutor
from src.modulos.horas.aplicacion.dto import (
    RegistrarHorasDTO,
    RegistroHorasDTO,
    ResumenHorasTutorDTO,
)
from src.modulos.horas.aplicacion.registrar_horas import RegistrarHoras


class ControladorHorasInterno:
    def __init__(
        self,
        caso_uso_registrar: RegistrarHoras,
        caso_uso_consultar_tutor: ConsultarHorasTutor,
    ):
        self._caso_uso_registrar = caso_uso_registrar
        self._caso_uso_consultar_tutor = caso_uso_consultar_tutor

    def registrar_horas(self, dto: RegistrarHorasDTO) -> RegistroHorasDTO:
        return self._caso_uso_registrar.ejecutar(dto)

    def consultar_horas_tutor(
        self,
        tutor_documento: str,
        practica_id: UUID,
        ip: str = "127.0.0.1",
        agente_usuario: str = "Interfaz web interna",
    ) -> ResumenHorasTutorDTO:
        return self._caso_uso_consultar_tutor.ejecutar(
            tutor_documento=tutor_documento,
            practica_id=practica_id,
            ip=ip,
            agente_usuario=agente_usuario,
        )
