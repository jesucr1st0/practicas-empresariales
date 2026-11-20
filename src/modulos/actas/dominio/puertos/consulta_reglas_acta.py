from abc import ABC, abstractmethod


class ConsultaReglasActa(ABC):
    @abstractmethod
    def obtener_horas_minimas(self, version_regla: str) -> int:
        pass
