from typing import Protocol


class ConsultaReglaTutor(Protocol):
    def obtener_capacidad_maxima_por_tutor(self, version_regla: str) -> int: ...

    def obtener_capacidad_maxima_programa(self, programa: str) -> int: ...
