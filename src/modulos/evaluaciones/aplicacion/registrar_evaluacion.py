from src.modulos.evaluaciones.aplicacion.dto import (
    RegistrarEvaluacionDTO,
    ResultadoEvaluacionDTO,
)
from src.modulos.evaluaciones.dominio.evaluacion import Evaluacion
from src.modulos.evaluaciones.dominio.puertos.evaluacion_repository import (
    EvaluacionRepository,
)
from src.modulos.evaluaciones.dominio.puertos.servicio_actualizacion_practica_evaluacion import (
    ServicioActualizacionPracticaEvaluacion,
)
from src.modulos.evaluaciones.dominio.puertos.servicio_invalidacion_enlace import (
    ServicioInvalidacionEnlace,
)


class RegistrarEvaluacion:
    def __init__(
        self,
        repositorio: EvaluacionRepository,
        servicio_practica: ServicioActualizacionPracticaEvaluacion,
        servicio_invalidacion: ServicioInvalidacionEnlace,
    ):
        self._repositorio = repositorio
        self._servicio_practica = servicio_practica
        self._servicio_invalidacion = servicio_invalidacion

    def ejecutar(self, dto: RegistrarEvaluacionDTO) -> ResultadoEvaluacionDTO:
        if self._repositorio.existe_para_practica(dto.practica_id):
            raise ValueError(
                "La práctica ya cuenta con una evaluación registrada; solo se permite una evaluación por práctica"
            )

        evaluacion = Evaluacion(
            practica_id=dto.practica_id,
            fecha=dto.fecha,
            calificacion=dto.calificacion,
            observaciones=dto.observaciones,
        )
        self._repositorio.guardar(evaluacion)
        self._servicio_practica.registrar_evaluacion_recibida(dto.practica_id)
        self._servicio_invalidacion.invalidar_enlace_usado(dto.token)

        return ResultadoEvaluacionDTO(
            exitoso=True,
            mensaje="Evaluación registrada exitosamente",
            evaluacion_id=evaluacion.id,
        )
