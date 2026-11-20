from collections.abc import Sequence

from src.modulos.practicas.dominio.empresa import Empresa
from src.modulos.practicas.dominio.puertos.empresa_repository import EmpresaRepository
from src.modulos.practicas.dominio.supervisor import Supervisor


class AdaptadorEmpresaMemoria(EmpresaRepository):
    """Adaptador en memoria para persistencia de empresas y supervisores (CU-10)."""

    def __init__(self) -> None:
        self._empresas: dict[str, Empresa] = {}
        self._supervisores: list[Supervisor] = []

    def guardar_empresa(self, empresa: Empresa) -> None:
        self._empresas[empresa.nit] = empresa

    def guardar_supervisor(self, supervisor: Supervisor) -> None:
        self._supervisores.append(supervisor)

    def obtener_empresa_por_nit(self, nit: str) -> Empresa | None:
        return self._empresas.get(nit)

    def obtener_supervisores_por_empresa(self, empresa_nit: str) -> Sequence[Supervisor]:
        return tuple(
            s for s in self._supervisores if s.empresa_nit == empresa_nit and s.activo
        )

    def listar_empresas(self) -> Sequence[Empresa]:
        return tuple(self._empresas.values())
