from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4


@dataclass(frozen=True)
class ReglaPrograma:
    id: UUID
    programa: str
    version: str
    vigencia_desde: date
    horas_minimas: int
    capacidad_maxima_tutor: int

    @staticmethod
    def crear(
        programa: str,
        version: str,
        vigencia_desde: date,
        horas_minimas: int,
        capacidad_maxima_tutor: int,
        id: UUID | None = None,
    ) -> "ReglaPrograma":
        return ReglaPrograma(
            id=id or uuid4(),
            programa=programa,
            version=version,
            vigencia_desde=vigencia_desde,
            horas_minimas=horas_minimas,
            capacidad_maxima_tutor=capacidad_maxima_tutor,
        )
