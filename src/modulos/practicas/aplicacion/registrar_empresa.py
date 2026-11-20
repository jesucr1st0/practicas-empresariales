from src.modulos.practicas.aplicacion.dto_empresa import (
    RegistrarEmpresaDTO,
    ResultadoEmpresaDTO,
)
from src.modulos.practicas.dominio.empresa import Empresa
from src.modulos.practicas.dominio.puertos.empresa_repository import EmpresaRepository
from src.modulos.practicas.dominio.supervisor import Supervisor


class RegistrarEmpresa:
    """Caso de uso CU-10: Registrar empresa y sus supervisores iniciales."""

    def __init__(self, empresa_repository: EmpresaRepository) -> None:
        self._empresa_repository = empresa_repository

    def ejecutar(self, dto: RegistrarEmpresaDTO) -> ResultadoEmpresaDTO:
        nit = dto.nit.strip() if dto.nit else ""
        razon_social = dto.razon_social.strip() if dto.razon_social else ""

        if not nit:
            raise ValueError("El NIT de la empresa es obligatorio.")
        if not razon_social:
            raise ValueError("La razón social de la empresa es obligatoria.")

        # Regla del negocio: La empresa debe contar con al menos un supervisor (1..*)
        if not dto.supervisores:
            raise ValueError("La empresa debe contar con al menos un supervisor.")

        # Validar unicidad del NIT
        empresa_existente = self._empresa_repository.obtener_empresa_por_nit(nit)
        if empresa_existente is not None:
            raise ValueError(f"Ya existe una empresa registrada con el NIT '{nit}'.")

        # Crear y persistir la empresa
        empresa = Empresa(
            nit=nit,
            razon_social=razon_social,
            sector=dto.sector.strip() if dto.sector else "",
            ciudad=dto.ciudad.strip() if dto.ciudad else "",
            activa=True,
        )
        self._empresa_repository.guardar_empresa(empresa)

        # Crear y persistir supervisores
        supervisores_guardados = 0
        for sup_dto in dto.supervisores:
            nombre = sup_dto.nombre.strip() if sup_dto.nombre else ""
            correo = sup_dto.correo.strip() if sup_dto.correo else ""
            if not nombre:
                raise ValueError("El nombre del supervisor es obligatorio.")
            if not correo:
                raise ValueError("El correo del supervisor es obligatorio.")

            supervisor = Supervisor(
                empresa_nit=empresa.nit,
                nombre=nombre,
                correo=correo,
                telefono=sup_dto.telefono.strip() if sup_dto.telefono else "",
                activo=True,
            )
            self._empresa_repository.guardar_supervisor(supervisor)
            supervisores_guardados += 1

        return ResultadoEmpresaDTO(
            empresa_id=empresa.id,
            nit=empresa.nit,
            razon_social=empresa.razon_social,
            activa=empresa.activa,
            supervisores_registrados=supervisores_guardados,
        )
