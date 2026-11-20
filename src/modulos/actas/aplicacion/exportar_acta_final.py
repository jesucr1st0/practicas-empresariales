import hashlib
from uuid import UUID

from src.modulos.actas.aplicacion.dto import ResultadoExportacionDTO
from src.modulos.actas.dominio.puertos.acta_final_repository import (
    ActaFinalRepository,
)
from src.modulos.actas.dominio.puertos.almacen_archivos import AlmacenArchivos


class ExportarActaFinal:
    def __init__(
        self,
        repositorio: ActaFinalRepository,
        almacen_archivos: AlmacenArchivos,
    ):
        self._repositorio = repositorio
        self._almacen_archivos = almacen_archivos

    def ejecutar(self, practica_id: UUID) -> ResultadoExportacionDTO:
        acta = self._repositorio.buscar_vigente_por_practica(practica_id)
        if acta is None:
            raise ValueError(
                f"No existe un acta final vigente para la práctica {practica_id}"
            )

        contenido = self._almacen_archivos.obtener_archivo(acta.ruta_archivo)
        huella_calculada = hashlib.sha256(contenido).hexdigest()

        if huella_calculada != acta.huella_integridad:
            raise ValueError(
                "Fallo crítico de integridad: el archivo del acta final ha sido alterado"
            )

        return ResultadoExportacionDTO(
            contenido=contenido,
            huella_integridad=acta.huella_integridad,
            nombre_archivo=f"acta_final_{acta.practica_id}.pdf",
        )
