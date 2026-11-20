from src.modulos.practicas.aplicacion.dto_empresa import (
    DetalleEmpresaDTO,
    DetalleSupervisorDTO,
)
from src.modulos.practicas.dominio.puertos.empresa_repository import EmpresaRepository


class ConsultarEmpresa:
    """Caso de uso para consultar información de una empresa y sus supervisores por NIT."""

    def __init__(self, empresa_repository: EmpresaRepository) -> None:
        self._empresa_repository = empresa_repository

    def ejecutar(self, nit: str) -> DetalleEmpresaDTO:
        nit_limpio = nit.strip() if nit else ""
        empresa = self._empresa_repository.obtener_empresa_por_nit(nit_limpio)
        if empresa is None:
            raise LookupError(f"No se encontró la empresa con NIT '{nit_limpio}'.")

        supervisores = self._empresa_repository.obtener_supervisores_por_empresa(empresa.nit)

        supervisores_dto = tuple(
            DetalleSupervisorDTO(
                id=s.id,
                nombre=s.nombre,
                correo=s.correo,
                telefono=s.telefono,
                activo=s.activo,
            )
            for s in supervisores
        )

        return DetalleEmpresaDTO(
            id=empresa.id,
            nit=empresa.nit,
            razon_social=empresa.razon_social,
            sector=empresa.sector,
            ciudad=empresa.ciudad,
            activa=empresa.activa,
            supervisores=supervisores_dto,
        )
