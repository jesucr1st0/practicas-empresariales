from abc import ABC, abstractmethod
from uuid import UUID


class ServicioActualizacionPracticaEvaluacion(ABC):
    @abstractmethod
    def registrar_evaluacion_recibida(self, practica_id: UUID) -> None:
        """Notifica al módulo Prácticas que la evaluación fue recibida para actualizar su estado."""
        pass
