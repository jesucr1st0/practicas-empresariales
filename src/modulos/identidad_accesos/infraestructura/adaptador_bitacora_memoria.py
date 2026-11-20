from src.modulos.identidad_accesos.dominio.puertos.bitacora_acceso_repository import BitacoraAccesoRepository
from src.modulos.identidad_accesos.dominio.registro_acceso import RegistroAcceso


class AdaptadorBitacoraMemoria(BitacoraAccesoRepository):
    def __init__(self) -> None:
        self._entradas: list[RegistroAcceso] = []

    def registrar(self, registro: RegistroAcceso) -> None:
        """Bitácora de solo inserción (ADR-005, RN-01)."""
        self._entradas.append(registro)

    def listar(self) -> list[RegistroAcceso]:
        return list(self._entradas)
