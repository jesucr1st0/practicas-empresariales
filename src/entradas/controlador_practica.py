from datetime import date
from uuid import UUID
from src.modulos.practicas.aplicacion.dto import RegistrarPracticaDTO, ResultadoPracticaDTO
from src.modulos.practicas.aplicacion.registrar_practica import RegistrarPractica


class ControladorPractica:
    def __init__(self, caso_uso_registrar: RegistrarPractica) -> None:
        self._caso_uso_registrar = caso_uso_registrar

    def registrar_practica(
        self,
        estudiante_documento: str,
        programa: str,
        empresa_id: str,
        supervisor_id: str,
        periodo: str,
        fecha_inicio: date,
        fecha_fin: date,
        postulacion_id: UUID | None = None,
        fecha_registro: date | None = None,
    ) -> ResultadoPracticaDTO:
        dto = RegistrarPracticaDTO(
            estudiante_documento=estudiante_documento,
            programa=programa,
            empresa_id=empresa_id,
            supervisor_id=supervisor_id,
            periodo=periodo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            postulacion_id=postulacion_id,
            fecha_registro=fecha_registro,
        )
        return self._caso_uso_registrar.ejecutar(dto)
