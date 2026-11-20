from uuid import UUID

from src.modulos.horas.aplicacion.dto import RegistroHorasDTO
from src.modulos.horas.dominio.puertos.registro_horas_repository import RegistroHorasRepository


class ConsultarHorasSupervisor:
    def __init__(self, repositorio_horas: RegistroHorasRepository):
        self._repositorio_horas = repositorio_horas

    def ejecutar(self, practica_id: UUID) -> list[RegistroHorasDTO]:
        registros = self._repositorio_horas.listar_por_practica(practica_id)
        return [
            RegistroHorasDTO(
                id=r.id,
                practica_id=r.practica_id,
                estudiante_documento=r.estudiante_documento,
                fecha=r.fecha,
                cantidad_horas=r.cantidad_horas,
                evidencia=r.evidencia,
                estado_validacion=r.estado_validacion.value,
            )
            for r in registros
        ]
