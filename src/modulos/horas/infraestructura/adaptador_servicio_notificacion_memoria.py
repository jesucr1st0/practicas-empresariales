from dataclasses import dataclass
from datetime import datetime, timezone

from src.modulos.horas.dominio.puertos.servicio_notificacion_horas import ServicioNotificacionHoras


@dataclass(frozen=True)
class NotificacionEnviada:
    email_destinatario: str
    enlace: str
    fecha_envio: datetime


class AdaptadorServicioNotificacionMemoria(ServicioNotificacionHoras):
    def __init__(self) -> None:
        self.notificaciones: list[NotificacionEnviada] = []

    def notificar_enlace_supervisor(self, email_destinatario: str, enlace: str) -> bool:
        self.notificaciones.append(
            NotificacionEnviada(
                email_destinatario=email_destinatario,
                enlace=enlace,
                fecha_envio=datetime.now(timezone.utc),
            )
        )
        return True
