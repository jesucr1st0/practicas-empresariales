from src.modulos.horas.aplicacion.dto import RegistrarHorasDTO, RegistroHorasDTO
from src.modulos.horas.dominio.puertos.registro_horas_repository import RegistroHorasRepository
from src.modulos.horas.dominio.registro_horas import RegistroHoras


class RegistrarHoras:
    def __init__(self, repositorio: RegistroHorasRepository):
        self._repositorio = repositorio

    def ejecutar(self, dto: RegistrarHorasDTO) -> RegistroHorasDTO:
        registro = RegistroHoras(
            practica_id=dto.practica_id,
            estudiante_documento=dto.estudiante_documento,
            fecha=dto.fecha,
            cantidad_horas=dto.cantidad_horas,
            evidencia=dto.evidencia,
        )
        self._repositorio.guardar(registro)
        return RegistroHorasDTO(
            id=registro.id,
            practica_id=registro.practica_id,
            estudiante_documento=registro.estudiante_documento,
            fecha=registro.fecha,
            cantidad_horas=registro.cantidad_horas,
            evidencia=registro.evidencia,
            estado_validacion=registro.estado_validacion.value,
        )
