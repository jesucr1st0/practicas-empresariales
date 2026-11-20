from uuid import UUID

from src.modulos.horas.dominio.puertos.servicio_enlace_horas import ServicioEnlaceHoras
from src.modulos.identidad_accesos.aplicacion.gestor_enlaces_acceso import GestorEnlacesAcceso


class AdaptadorServicioEnlaceMemoria(ServicioEnlaceHoras):
    def __init__(self, gestor_enlaces: GestorEnlacesAcceso):
        self._gestor = gestor_enlaces

    def emitir_enlace(self, practica_id: UUID, email_supervisor: str) -> str:
        return self._gestor.emitir_enlace(practica_id, email_supervisor)
