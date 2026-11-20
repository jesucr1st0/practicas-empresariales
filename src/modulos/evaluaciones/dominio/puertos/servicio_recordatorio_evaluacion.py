from abc import ABC, abstractmethod


class ServicioRecordatorioEvaluacion(ABC):
    @abstractmethod
    def enviar_recordatorio(self, email_destinatario: str, enlace: str) -> bool:
        pass
