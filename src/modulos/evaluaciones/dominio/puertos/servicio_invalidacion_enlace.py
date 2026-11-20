from abc import ABC, abstractmethod


class ServicioInvalidacionEnlace(ABC):
    @abstractmethod
    def invalidar_enlace_usado(self, token: str) -> None:
        """Invalida el enlace de un solo uso pasando su estado a USADO (ADR-006)."""
        pass
