from datetime import date, datetime, timezone
from uuid import UUID, uuid4

from src.modulos.horas.dominio.estado_validacion_horas import EstadoValidacionHoras


class RegistroHoras:
    def __init__(
        self,
        practica_id: UUID,
        estudiante_documento: str,
        fecha: date,
        cantidad_horas: int,
        evidencia: str,
        id: UUID | None = None,
        estado_validacion: EstadoValidacionHoras = EstadoValidacionHoras.PENDIENTE,
        fecha_registro: datetime | None = None,
    ):
        if cantidad_horas <= 0:
            raise ValueError("La cantidad de horas debe ser mayor a cero")
        self.id = id or uuid4()
        self.practica_id = practica_id
        self.estudiante_documento = estudiante_documento
        self.fecha = fecha
        self.cantidad_horas = cantidad_horas
        self.evidencia = evidencia
        self.estado_validacion = estado_validacion
        self.fecha_registro = fecha_registro or datetime.now(timezone.utc)

    def validar_por_supervisor(self) -> None:
        self.estado_validacion = EstadoValidacionHoras.VALIDADO_SUPERVISOR

    def rechazar(self) -> None:
        self.estado_validacion = EstadoValidacionHoras.RECHAZADO
