from collections.abc import Mapping
from uuid import UUID


class AdaptadorServicioPracticaMemoria:
    def __init__(self, practicas: Mapping[UUID, tuple[str, str]]) -> None:
        self._practicas = {
            practica_id: (programa, version_regla, None)
            for practica_id, (programa, version_regla) in practicas.items()
        }

    def obtener_programa(self, practica_id: UUID) -> str:
        return self._obtener(practica_id)[0]

    def obtener_version_regla(self, practica_id: UUID) -> str:
        return self._obtener(practica_id)[1]

    def actualizar_tutor_vigente(self, practica_id: UUID, tutor_documento: str) -> None:
        programa, version_regla, _ = self._obtener(practica_id)
        self._practicas[practica_id] = (programa, version_regla, tutor_documento)

    def obtener_tutor_vigente(self, practica_id: UUID) -> str | None:
        return self._obtener(practica_id)[2]

    def puede_tutor_consultar(self, practica_id: UUID, tutor_documento: str) -> bool:
        return self.obtener_tutor_vigente(practica_id) == tutor_documento

    def _obtener(self, practica_id: UUID) -> tuple[str, str, str | None]:
        try:
            return self._practicas[practica_id]
        except KeyError as error:
            raise LookupError(f"No se encontró la práctica {practica_id}.") from error
