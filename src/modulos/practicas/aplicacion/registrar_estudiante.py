from src.modulos.practicas.aplicacion.registrar_estudiante_dto import (
    RegistrarEstudianteDTO,
)
from src.modulos.practicas.aplicacion.resultado_estudiante_dto import (
    ResultadoEstudianteDTO,
)
from src.modulos.practicas.dominio.estudiante import Estudiante
from src.modulos.practicas.dominio.puertos.estudiante_repository import (
    EstudianteRepository,
)


class RegistrarEstudiante:
    def __init__(self, estudiantes: EstudianteRepository) -> None:
        self._estudiantes = estudiantes

    def ejecutar(self, dto: RegistrarEstudianteDTO) -> ResultadoEstudianteDTO:
        if self._estudiantes.obtener_por_documento(dto.documento) is not None:
            raise ValueError(
                f"Ya existe un estudiante registrado con documento {dto.documento}"
            )

        estudiante = Estudiante(
            documento=dto.documento,
            nombre=dto.nombre,
            programa=dto.programa,
            correo=dto.correo,
        )
        self._estudiantes.guardar(estudiante)

        return ResultadoEstudianteDTO(
            documento=estudiante.documento,
            nombre=estudiante.nombre,
            programa=estudiante.programa,
            correo=estudiante.correo,
        )
