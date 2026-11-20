import hashlib
from uuid import UUID

from src.modulos.actas.aplicacion.dto import ResultadoExportacionDTO
from src.modulos.actas.dominio.puertos.acta_final_repository import (
    ActaFinalRepository,
)
from src.modulos.actas.dominio.puertos.almacen_archivos import AlmacenArchivos
from src.modulos.actas.dominio.puertos.consulta_practica_acta import (
    ConsultaPracticaActa,
)


class ExportarActaFinal:
    def __init__(
        self,
        repositorio: ActaFinalRepository,
        almacen_archivos: AlmacenArchivos,
        consulta_practica: ConsultaPracticaActa | None = None,
    ):
        self._repositorio = repositorio
        self._almacen_archivos = almacen_archivos
        self._consulta_practica = consulta_practica

    def ejecutar(
        self,
        practica_id: UUID,
        estudiante_documento: str | None = None,
    ) -> ResultadoExportacionDTO:
        if estudiante_documento is not None:
            self._verificar_alcance_estudiante(practica_id, estudiante_documento)

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

    def _verificar_alcance_estudiante(
        self, practica_id: UUID, estudiante_documento: str
    ) -> None:
        """Regla de alcance (ADR-005): el estudiante solo exporta el acta de su práctica."""
        if self._consulta_practica is None:
            raise PermissionError(
                "No es posible verificar el alcance del estudiante sobre la práctica"
            )
        datos = self._consulta_practica.consultar_practica(practica_id)
        if datos is None or datos.estudiante_documento != estudiante_documento:
            raise PermissionError(
                f"La práctica {practica_id} no está en el alcance del estudiante "
                f"{estudiante_documento}"
            )
