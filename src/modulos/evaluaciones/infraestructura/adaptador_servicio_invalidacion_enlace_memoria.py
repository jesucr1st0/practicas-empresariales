from src.modulos.evaluaciones.dominio.puertos.servicio_invalidacion_enlace import (
    ServicioInvalidacionEnlace,
)
from src.modulos.identidad_accesos.aplicacion.gestor_enlaces_acceso import (
    GestorEnlacesAcceso,
)


class AdaptadorServicioInvalidacionEnlaceMemoria(ServicioInvalidacionEnlace):
    def __init__(self, gestor_enlaces: GestorEnlacesAcceso):
        self._gestor_enlaces = gestor_enlaces

    def invalidar_enlace_usado(self, token: str) -> None:
        self._gestor_enlaces.marcar_usado(token)
