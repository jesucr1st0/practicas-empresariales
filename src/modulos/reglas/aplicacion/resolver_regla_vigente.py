from datetime import date
from src.modulos.reglas.dominio.puertos.regla_repository import ReglaRepository
from src.modulos.reglas.dominio.regla_programa import ReglaPrograma


class ResolverReglaVigente:
    def __init__(self, repositorio: ReglaRepository) -> None:
        self._repositorio = repositorio

    def ejecutar(self, programa: str, fecha: date) -> ReglaPrograma | None:
        return self._repositorio.obtener_vigente(programa, fecha)
