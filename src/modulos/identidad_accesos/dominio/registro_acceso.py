from datetime import datetime, timezone
from uuid import UUID, uuid4


class RegistroAcceso:
    def __init__(
        self,
        sujeto: str,
        accion: str,
        ip: str,
        agente_usuario: str,
        exitoso: bool,
        detalle: str,
        id: UUID | None = None,
        fecha: datetime | None = None,
    ):
        self.id = id or uuid4()
        self.sujeto = sujeto
        self.accion = accion
        self.fecha = fecha or datetime.now(timezone.utc)
        self.ip = ip
        self.agente_usuario = agente_usuario
        self.exitoso = exitoso
        self.detalle = detalle
