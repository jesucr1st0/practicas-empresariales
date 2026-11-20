from datetime import date
from uuid import UUID
from src.modulos.reglas.dominio.puertos.regla_repository import ReglaRepository
from src.modulos.reglas.dominio.regla_programa import ReglaPrograma


class AdaptadorReglaMemoria(ReglaRepository):
    def __init__(self) -> None:
        self._reglas: dict[UUID, ReglaPrograma] = {}

    def guardar(self, regla: ReglaPrograma) -> None:
        self._reglas[regla.id] = regla

    def obtener_por_id(self, regla_id: UUID) -> ReglaPrograma | None:
        return self._reglas.get(regla_id)

    def listar_por_programa(self, programa: str) -> list[ReglaPrograma]:
        return [r for r in self._reglas.values() if r.programa.lower() == programa.lower()]

    def obtener_vigente(self, programa: str, fecha: date) -> ReglaPrograma | None:
        reglas_programa = [
            r for r in self._reglas.values()
            if r.programa.lower() == programa.lower() and r.vigencia_desde <= fecha
        ]
        if not reglas_programa:
            return None
        # Seleccionar la de vigencia_desde más reciente
        reglas_programa.sort(key=lambda r: r.vigencia_desde, reverse=True)
        return reglas_programa[0]
