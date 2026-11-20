from uuid import UUID

from src.modulos.horas.aplicacion.dto import ResultadoValidacionDTO
from src.modulos.horas.dominio.estado_validacion_horas import EstadoValidacionHoras
from src.modulos.horas.dominio.puertos.registro_horas_repository import RegistroHorasRepository


class ValidarHorasSupervisor:
    def __init__(self, repositorio_horas: RegistroHorasRepository):
        self._repositorio_horas = repositorio_horas

    def ejecutar(self, practica_id: UUID) -> ResultadoValidacionDTO:
        registros = self._repositorio_horas.listar_por_practica(practica_id)
        validadas = 0

        for r in registros:
            if r.estado_validacion == EstadoValidacionHoras.PENDIENTE:
                r.validar_por_supervisor()
                self._repositorio_horas.guardar(r)
                validadas += r.cantidad_horas

        return ResultadoValidacionDTO(
            exitoso=True,
            mensaje="Horas validadas exitosamente",
            horas_validadas=validadas,
        )
