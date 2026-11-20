from src.modulos.identidad_accesos.dominio.enlace_acceso import EnlaceAcceso
from src.modulos.identidad_accesos.dominio.puertos.enlace_acceso_repository import EnlaceAccesoRepository


class AdaptadorEnlaceAccesoMemoria(EnlaceAccesoRepository):
    def __init__(self, enlaces_iniciales: list[EnlaceAcceso] | None = None):
        self._enlaces: dict[str, EnlaceAcceso] = {}
        if enlaces_iniciales:
            for e in enlaces_iniciales:
                self._enlaces[e.token_hash] = e

    def guardar(self, enlace: EnlaceAcceso) -> None:
        self._enlaces[enlace.token_hash] = enlace

    def buscar_por_hash(self, token_hash: str) -> EnlaceAcceso | None:
        return self._enlaces.get(token_hash)
