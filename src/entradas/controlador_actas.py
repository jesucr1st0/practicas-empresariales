from uuid import UUID

from src.modulos.actas.aplicacion.dto import (
    ActaFinalDTO,
    GenerarActaDTO,
    ResultadoExportacionDTO,
)
from src.modulos.actas.aplicacion.exportar_acta_final import ExportarActaFinal
from src.modulos.actas.aplicacion.generar_acta_final import GenerarActaFinal


class ControladorActas:
    def __init__(
        self,
        caso_uso_generar: GenerarActaFinal,
        caso_uso_exportar: ExportarActaFinal,
    ):
        self._caso_uso_generar = caso_uso_generar
        self._caso_uso_exportar = caso_uso_exportar

    def generar_acta(self, dto: GenerarActaDTO) -> ActaFinalDTO:
        return self._caso_uso_generar.ejecutar(dto)

    def exportar_acta(self, practica_id: UUID) -> ResultadoExportacionDTO:
        return self._caso_uso_exportar.ejecutar(practica_id)
