from src.modulos.tutores_asignacion.dominio.tutor import Tutor


class AdaptadorTutorMemoria:
    """Implementación en memoria de TutorRepository."""

    def __init__(self) -> None:
        self._tutores: dict[str, Tutor] = {}

    def guardar(self, tutor: Tutor) -> None:
        self._tutores[tutor.documento] = tutor

    def obtener_por_documento(self, documento: str) -> Tutor | None:
        return self._tutores.get(documento)
