from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.modulos.actas.dominio.estado_acta import EstadoActa


class ActaFinal:
    def __init__(
        self,
        practica_id: UUID,
        huella_integridad: str,
        version_regla: str,
        horas_validadas: int,
        calificacion_evaluacion: float,
        ruta_archivo: str,
        plantilla_version: str = "v1.0-oficial",
        id: UUID | None = None,
        fecha_emision: datetime | None = None,
        estado: EstadoActa = EstadoActa.VIGENTE,
    ):
        self.id = id or uuid4()
        self.practica_id = practica_id
        self.huella_integridad = huella_integridad
        self.version_regla = version_regla
        self.horas_validadas = horas_validadas
        self.calificacion_evaluacion = calificacion_evaluacion
        self.ruta_archivo = ruta_archivo
        self.plantilla_version = plantilla_version
        self.fecha_emision = fecha_emision or datetime.now(timezone.utc)
        self.estado = estado

    def anular(self) -> None:
        self.estado = EstadoActa.ANULADA
