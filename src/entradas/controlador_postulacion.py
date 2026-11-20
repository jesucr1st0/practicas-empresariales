from src.modulos.postulaciones.aplicacion.dto import PostulacionDTO, ResultadoPostulacionDTO
from src.modulos.postulaciones.aplicacion.realizar_postulacion import RealizarPostulacion


class ControladorPostulacion:
    def __init__(self, caso_uso_realizar: RealizarPostulacion) -> None:
        self._caso_uso_realizar = caso_uso_realizar

    def postularse(
        self,
        estudiante_documento: str,
        programa: str,
        correo_estudiante: str = "",
    ) -> ResultadoPostulacionDTO:
        dto = PostulacionDTO(
            estudiante_documento=estudiante_documento,
            programa=programa,
            correo_estudiante=correo_estudiante,
        )
        return self._caso_uso_realizar.ejecutar(dto)
