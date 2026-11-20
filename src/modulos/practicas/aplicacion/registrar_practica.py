from datetime import date
from src.modulos.practicas.aplicacion.dto import RegistrarPracticaDTO, ResultadoPracticaDTO
from src.modulos.practicas.dominio.estado_practica import EstadoPractica
from src.modulos.practicas.dominio.practica import Practica
from src.modulos.practicas.dominio.puertos.practica_repository import PracticaRepository
from src.modulos.practicas.dominio.puertos.servicio_consulta_postulacion import ServicioConsultaPostulacion
from src.modulos.practicas.dominio.puertos.servicio_consulta_reglas import ServicioConsultaReglas


class PostulacionNoVerificadaError(Exception):
    pass


class EstudianteConPracticaActivaError(Exception):
    pass


class ReglaNoConfiguradaError(Exception):
    pass


class RegistrarPractica:
    def __init__(
        self,
        repositorio: PracticaRepository,
        servicio_reglas: ServicioConsultaReglas,
        servicio_postulacion: ServicioConsultaPostulacion | None = None,
    ) -> None:
        self._repositorio = repositorio
        self._servicio_reglas = servicio_reglas
        self._servicio_postulacion = servicio_postulacion

    def ejecutar(self, dto: RegistrarPracticaDTO) -> ResultadoPracticaDTO:
        # 1. Si proviene de una postulación, validar que esté verificada
        if dto.postulacion_id is not None:
            if self._servicio_postulacion is None or not self._servicio_postulacion.postulacion_esta_verificada(dto.postulacion_id):
                raise PostulacionNoVerificadaError(
                    f"La postulación {dto.postulacion_id} no está en estado verificada."
                )

        # 2. Validar que el estudiante no tenga ya una práctica activa
        practica_activa = self._repositorio.obtener_activa_por_estudiante(dto.estudiante_documento)
        if practica_activa is not None:
            raise EstudianteConPracticaActivaError(
                f"El estudiante {dto.estudiante_documento} ya cuenta con una práctica en curso o registrada."
            )

        # 3. Resolver la regla vigente para el programa a la fecha de registro o fecha de inicio
        fecha_evaluacion = dto.fecha_registro or dto.fecha_inicio
        regla_vigente = self._servicio_reglas.consultar_regla_vigente(dto.programa, fecha_evaluacion)
        if regla_vigente is None:
            raise ReglaNoConfiguradaError(
                f"No existe versión de regla vigente para el programa {dto.programa} a la fecha {fecha_evaluacion}."
            )

        # 4. Crear la práctica fijando de manera inmutable la regla
        practica = Practica.registrar(
            estudiante_documento=dto.estudiante_documento,
            programa=dto.programa,
            empresa_id=dto.empresa_id,
            supervisor_id=dto.supervisor_id,
            periodo=dto.periodo,
            fecha_inicio=dto.fecha_inicio,
            fecha_fin=dto.fecha_fin,
            regla_id=regla_vigente.id,
            regla_version=regla_vigente.version,
            horas_minimas_exigidas=regla_vigente.horas_minimas,
            postulacion_id=dto.postulacion_id,
        )

        # 5. Persistir la práctica
        self._repositorio.guardar(practica)

        return ResultadoPracticaDTO(
            id=practica.id,
            estudiante_documento=practica.estudiante_documento,
            programa=practica.programa,
            estado=practica.estado.value,
            regla_version=practica.regla_version,
            horas_minimas_exigidas=practica.horas_minimas_exigidas,
            postulacion_id=practica.postulacion_id,
        )
