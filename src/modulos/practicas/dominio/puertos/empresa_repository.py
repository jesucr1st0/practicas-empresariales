from collections.abc import Sequence
from typing import Protocol

from src.modulos.practicas.dominio.empresa import Empresa
from src.modulos.practicas.dominio.supervisor import Supervisor


class EmpresaRepository(Protocol):
    """Puerto de persistencia para empresas y sus supervisores (CU-10)."""

    def guardar_empresa(self, empresa: Empresa) -> None: ...

    def guardar_supervisor(self, supervisor: Supervisor) -> None: ...

    def obtener_empresa_por_nit(self, nit: str) -> Empresa | None: ...

    def obtener_supervisores_por_empresa(self, empresa_nit: str) -> Sequence[Supervisor]: ...

    def listar_empresas(self) -> Sequence[Empresa]: ...
