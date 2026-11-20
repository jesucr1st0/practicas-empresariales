from typing import Protocol
from datetime import date
from uuid import UUID
from dataclasses import dataclass


@dataclass(frozen=True)
class InfoReglaVigente:
    id: UUID
    version: str
    horas_minimas: int
    capacidad_maxima_tutor: int


class ServicioConsultaReglas(Protocol):
    def consultar_regla_vigente(self, programa: str, fecha: date) -> InfoReglaVigente | None:
        ...
