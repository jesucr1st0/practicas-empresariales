from collections.abc import Mapping


class AdaptadorServicioReglasMemoria:
    def __init__(self, capacidades_por_version_o_programa: Mapping[str, int]) -> None:
        self._capacidades = dict(capacidades_por_version_o_programa)

    def obtener_capacidad_maxima_por_tutor(self, version_regla: str) -> int:
        try:
            return self._capacidades[version_regla]
        except KeyError as error:
            raise LookupError(f"No existe capacidad configurada para la regla {version_regla!r}.") from error

    def obtener_capacidad_maxima_programa(self, programa: str) -> int:
        if programa in self._capacidades:
            return self._capacidades[programa]
        # Si no está por nombre de programa exacto, retornar la primera capacidad configurada si existe
        if self._capacidades:
            return next(iter(self._capacidades.values()))
        raise LookupError(f"No existe capacidad configurada para el programa {programa!r}.")
