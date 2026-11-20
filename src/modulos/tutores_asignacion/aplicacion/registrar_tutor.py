from src.modulos.tutores_asignacion.aplicacion.registrar_tutor_dto import (
    RegistrarTutorDTO,
)
from src.modulos.tutores_asignacion.aplicacion.resultado_tutor_dto import (
    ResultadoTutorDTO,
)
from src.modulos.tutores_asignacion.dominio.puertos.tutor_repository import (
    TutorRepository,
)
from src.modulos.tutores_asignacion.dominio.tutor import Tutor


class RegistrarTutor:
    def __init__(self, tutores: TutorRepository) -> None:
        self._tutores = tutores

    def ejecutar(self, dto: RegistrarTutorDTO) -> ResultadoTutorDTO:
        for campo in ("documento", "nombre", "correo", "programa"):
            if not getattr(dto, campo).strip():
                raise ValueError(f"El {campo} del tutor es obligatorio")

        if self._tutores.obtener_por_documento(dto.documento) is not None:
            raise ValueError(
                f"Ya existe un tutor registrado con documento {dto.documento}"
            )

        tutor = Tutor(
            documento=dto.documento,
            nombre=dto.nombre,
            correo=dto.correo,
            programa=dto.programa,
            activo=True,
        )
        self._tutores.guardar(tutor)

        return ResultadoTutorDTO(
            documento=tutor.documento,
            nombre=tutor.nombre,
            correo=tutor.correo,
            programa=tutor.programa,
            activo=tutor.activo,
        )
