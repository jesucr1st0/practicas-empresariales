from uuid import UUID

from src.modulos.horas.dominio.puertos.registro_horas_repository import RegistroHorasRepository
from src.modulos.horas.dominio.registro_horas import RegistroHoras


class AdaptadorRegistroHorasMemoria(RegistroHorasRepository):
    def __init__(self, registros_iniciales: list[RegistroHoras] | None = None):
        self._registros: dict[UUID, RegistroHoras] = {}
        if registros_iniciales:
            for r in registros_iniciales:
                self._registros[r.id] = r

    def guardar(self, registro: RegistroHoras) -> None:
        self._registros[registro.id] = registro

    def buscar_por_id(self, id: UUID) -> RegistroHoras | None:
        return self._registros.get(id)

    def listar_por_practica(self, practica_id: UUID) -> list[RegistroHoras]:
        return [r for r in self._registros.values() if r.practica_id == practica_id]
