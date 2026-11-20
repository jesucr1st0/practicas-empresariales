from datetime import date

from src.modulos.evaluaciones.aplicacion.dto import (
    RegistrarEvaluacionDTO,
    ResultadoEvaluacionDTO,
)
from src.modulos.evaluaciones.aplicacion.registrar_evaluacion import (
    RegistrarEvaluacion,
)
from src.modulos.identidad_accesos.aplicacion.gestor_enlaces_acceso import (
    GestorEnlacesAcceso,
)


class ControladorAccesoExternoEvaluacion:
    def __init__(
        self,
        gestor_enlaces: GestorEnlacesAcceso,
        caso_uso_registrar: RegistrarEvaluacion,
    ):
        self._gestor_enlaces = gestor_enlaces
        self._caso_uso_registrar = caso_uso_registrar

    def enviar_evaluacion(
        self,
        token: str,
        fecha: date,
        calificacion: float,
        observaciones: str,
        ip: str,
        agente_usuario: str,
    ) -> ResultadoEvaluacionDTO:
        enlace = self._gestor_enlaces.validar_token(token, ip, agente_usuario)
        if "evaluar" not in enlace.acciones_permitidas:
            raise PermissionError("Acción 'evaluar' no permitida para este enlace")

        dto = RegistrarEvaluacionDTO(
            token=token,
            practica_id=enlace.practica_id,
            fecha=fecha,
            calificacion=calificacion,
            observaciones=observaciones,
        )
        return self._caso_uso_registrar.ejecutar(dto)
