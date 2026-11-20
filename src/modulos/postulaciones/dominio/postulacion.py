from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4
from src.modulos.postulaciones.dominio.estado_postulacion import EstadoPostulacion


@dataclass
class Postulacion:
    id: UUID
    estudiante_documento: str
    programa: str
    fecha_creacion: datetime
    estado: EstadoPostulacion
    fecha_ultimo_intento: datetime | None = None
    numero_reintentos: int = 0
    motivo_rechazo: str | None = None

    @staticmethod
    def crear(
        estudiante_documento: str,
        programa: str,
        fecha_creacion: datetime | None = None,
        id: UUID | None = None,
    ) -> "Postulacion":
        return Postulacion(
            id=id or uuid4(),
            estudiante_documento=estudiante_documento,
            programa=programa,
            fecha_creacion=fecha_creacion or datetime.now(timezone.utc),
            estado=EstadoPostulacion.PENDIENTE_VERIFICACION,
            fecha_ultimo_intento=None,
            numero_reintentos=0,
            motivo_rechazo=None,
        )

    def marcar_verificada(self) -> None:
        self.estado = EstadoPostulacion.VERIFICADA
        self.fecha_ultimo_intento = datetime.now(timezone.utc)

    def marcar_rechazada(self, motivo: str) -> None:
        self.estado = EstadoPostulacion.RECHAZADA
        self.motivo_rechazo = motivo
        self.fecha_ultimo_intento = datetime.now(timezone.utc)

    def registrar_intento_fallido(self, fecha: datetime | None = None) -> None:
        self.numero_reintentos += 1
        self.fecha_ultimo_intento = fecha or datetime.now(timezone.utc)

    def pasar_a_revision_manual(self) -> None:
        self.estado = EstadoPostulacion.REVISION_MANUAL
        self.fecha_ultimo_intento = datetime.now(timezone.utc)
