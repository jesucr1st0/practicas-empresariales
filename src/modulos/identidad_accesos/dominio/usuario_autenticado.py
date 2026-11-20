from dataclasses import dataclass

from src.modulos.identidad_accesos.dominio.rol import Rol


@dataclass(frozen=True)
class UsuarioAutenticado:
    """Usuario interno ya autenticado por el SSO institucional (ADR-004)."""

    documento: str
    rol: Rol
