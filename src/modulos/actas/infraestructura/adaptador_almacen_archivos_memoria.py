from src.modulos.actas.dominio.puertos.almacen_archivos import AlmacenArchivos


class AdaptadorAlmacenArchivosMemoria(AlmacenArchivos):
    def __init__(self, archivos_iniciales: dict[str, bytes] | None = None):
        self._archivos: dict[str, bytes] = archivos_iniciales or {}

    def guardar_archivo(self, ruta: str, contenido: bytes) -> str:
        self._archivos[ruta] = contenido
        return ruta

    def obtener_archivo(self, ruta: str) -> bytes:
        if ruta not in self._archivos:
            raise FileNotFoundError(f"Archivo no encontrado en ruta {ruta}")
        return self._archivos[ruta]
