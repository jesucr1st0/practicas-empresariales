from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.modulos.identidad_accesos.dominio.estado_enlace import EstadoEnlace


class EnlaceAcceso:
    def __init__(
        self,
        token_hash: str,
        practica_id: UUID,
        email_destinatario: str,
        fecha_vencimiento: datetime,
        id: UUID | None = None,
        fecha_emision: datetime | None = None,
        estado: EstadoEnlace = EstadoEnlace.VIGENTE,
        acciones_permitidas: list[str] | None = None,
    ):
        self.id = id or uuid4()
        self.token_hash = token_hash
        self.practica_id = practica_id
        self.email_destinatario = email_destinatario
        self.fecha_emision = fecha_emision or datetime.now(timezone.utc)
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.acciones_permitidas = acciones_permitidas or ["validar_horas", "evaluar"]

    def esta_vigente(self, ahora: datetime | None = None) -> bool:
        momento = ahora or datetime.now(timezone.utc)
        if self.estado != EstadoEnlace.VIGENTE:
            return False
        if momento > self.fecha_vencimiento:
            self.estado = EstadoEnlace.VENCIDO
            return False
        return True

    def marcar_usado(self) -> None:
        self.estado = EstadoEnlace.USADO

    def revocar(self) -> None:
        self.estado = EstadoEnlace.REVOCADO
