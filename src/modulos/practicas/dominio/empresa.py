from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Empresa:
    """Organización donde se realiza la práctica empresarial (CU-10, CU-02)."""
    nit: str
    razon_social: str
    sector: str = ""
    ciudad: str = ""
    activa: bool = True
    id: UUID = field(default_factory=uuid4)
