from abc import ABC, abstractmethod


class ServicioNotificacionHoras(ABC):
    @abstractmethod
    def notificar_enlace_supervisor(self, email_destinatario: str, enlace: str) -> bool:
        pass
