from uuid import UUID
from src.modulos.postulaciones.dominio.estado_postulacion import EstadoPostulacion
from src.modulos.postulaciones.dominio.postulacion import Postulacion
from src.modulos.postulaciones.dominio.puertos.postulacion_repository import PostulacionRepository


class AdaptadorPostulacionMemoria(PostulacionRepository):
    def __init__(self) -> None:
        self._postulaciones: dict[UUID, Postulacion] = {}

    def guardar(self, postulacion: Postulacion) -> None:
        self._postulaciones[postulacion.id] = postulacion

    def obtener_por_id(self, postulacion_id: UUID) -> Postulacion | None:
        return self._postulaciones.get(postulacion_id)

    def obtener_activa_por_estudiante(self, estudiante_documento: str) -> Postulacion | None:
        for p in self._postulaciones.values():
            if p.estudiante_documento == estudiante_documento and p.estado in (
                EstadoPostulacion.PENDIENTE_VERIFICACION,
                EstadoPostulacion.VERIFICADA,
            ):
                return p
        return None

    def listar_pendientes(self) -> list[Postulacion]:
        return [
            p for p in self._postulaciones.values()
            if p.estado == EstadoPostulacion.PENDIENTE_VERIFICACION
        ]

    def listar_todas(self) -> list[Postulacion]:
        return list(self._postulaciones.values())
