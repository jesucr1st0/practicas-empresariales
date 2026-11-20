from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from src.modulos.practicas.dominio.estado_practica import EstadoPractica


@dataclass
class Practica:
    id: UUID
    estudiante_documento: str
    programa: str
    empresa_id: str
    supervisor_id: str
    periodo: str
    fecha_inicio: date
    fecha_fin: date
    estado: EstadoPractica
    regla_id: UUID
    regla_version: str
    horas_minimas_exigidas: int
    postulacion_id: UUID | None = None
    tutor_documento: str | None = None

    @staticmethod
    def registrar(
        estudiante_documento: str,
        programa: str,
        empresa_id: str,
        supervisor_id: str,
        periodo: str,
        fecha_inicio: date,
        fecha_fin: date,
        regla_id: UUID,
        regla_version: str,
        horas_minimas_exigidas: int,
        postulacion_id: UUID | None = None,
        id: UUID | None = None,
    ) -> "Practica":
        return Practica(
            id=id or uuid4(),
            estudiante_documento=estudiante_documento,
            programa=programa,
            empresa_id=empresa_id,
            supervisor_id=supervisor_id,
            periodo=periodo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=EstadoPractica.REGISTRADA,
            regla_id=regla_id,
            regla_version=regla_version,
            horas_minimas_exigidas=horas_minimas_exigidas,
            postulacion_id=postulacion_id,
            tutor_documento=None,
        )

    def asignar_tutor(self, tutor_documento: str) -> None:
        self.tutor_documento = tutor_documento
