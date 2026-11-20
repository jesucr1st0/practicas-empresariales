from typing import Protocol
from uuid import UUID
from datetime import date
from src.modulos.reglas.dominio.regla_programa import ReglaPrograma


class ReglaRepository(Protocol):
    def guardar(self, regla: ReglaPrograma) -> None:
        ...

    def obtener_por_id(self, regla_id: UUID) -> ReglaPrograma | None:
        ...

    def listar_por_programa(self, programa: str) -> list[ReglaPrograma]:
        ...

    def obtener_vigente(self, programa: str, fecha: date) -> ReglaPrograma | None:
        ...
