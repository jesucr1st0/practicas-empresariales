from src.modulos.actas.dominio.puertos.consulta_reglas_acta import (
    ConsultaReglasActa,
)


class AdaptadorConsultaReglasMemoria(ConsultaReglasActa):
    def __init__(self, horas_minimas_por_version: dict[str, int] | None = None):
        self._reglas: dict[str, int] = horas_minimas_por_version or {
            "v1": 480,
            "v2": 540,
        }

    def fijar_regla(self, version_regla: str, horas_minimas: int) -> None:
        self._reglas[version_regla] = horas_minimas

    def obtener_horas_minimas(self, version_regla: str) -> int:
        if version_regla not in self._reglas:
            raise ValueError(f"Versión de regla '{version_regla}' no encontrada")
        return self._reglas[version_regla]
