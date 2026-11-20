from collections.abc import Mapping


class AdaptadorServicioReglasMemoria:
    def __init__(self, capacidades_por_version: Mapping[str, int]) -> None:
        self._capacidades = dict(capacidades_por_version)

    def obtener_capacidad_maxima_por_tutor(self, version_regla: str) -> int:
        try:
            return self._capacidades[version_regla]
        except KeyError as error:
            raise LookupError(f"No existe capacidad configurada para la regla {version_regla!r}.") from error
