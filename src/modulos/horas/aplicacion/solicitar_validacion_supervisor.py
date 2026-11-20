from uuid import UUID

from src.modulos.horas.dominio.puertos.servicio_enlace_horas import ServicioEnlaceHoras
from src.modulos.horas.dominio.puertos.servicio_notificacion_horas import ServicioNotificacionHoras


class SolicitarValidacionSupervisor:
    def __init__(
        self,
        servicio_enlace: ServicioEnlaceHoras,
        servicio_notificacion: ServicioNotificacionHoras,
    ):
        self._servicio_enlace = servicio_enlace
        self._servicio_notificacion = servicio_notificacion

    def ejecutar(self, practica_id: UUID, email_supervisor: str) -> str:
        token = self._servicio_enlace.emitir_enlace(practica_id, email_supervisor)
        enlace_url = f"https://practicas.universidad.edu.co/acceso-externo?token={token}"
        self._servicio_notificacion.notificar_enlace_supervisor(email_supervisor, enlace_url)
        return token
