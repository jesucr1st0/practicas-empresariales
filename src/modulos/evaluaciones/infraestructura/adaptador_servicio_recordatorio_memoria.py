from dataclasses import dataclass
from datetime import datetime, timezone

from src.modulos.evaluaciones.dominio.puertos.servicio_recordatorio_evaluacion import (
    ServicioRecordatorioEvaluacion,
)


@dataclass(frozen=True)
class RecordatorioEnviado:
    email_destinatario: str
    enlace: str
    fecha_envio: datetime


class AdaptadorServicioRecordatorioMemoria(ServicioRecordatorioEvaluacion):
    def __init__(self) -> None:
        self.recordatorios: list[RecordatorioEnviado] = []

    def enviar_recordatorio(self, email_destinatario: str, enlace: str) -> bool:
        self.recordatorios.append(
            RecordatorioEnviado(
                email_destinatario=email_destinatario,
                enlace=enlace,
                fecha_envio=datetime.now(timezone.utc),
            )
        )
        return True
