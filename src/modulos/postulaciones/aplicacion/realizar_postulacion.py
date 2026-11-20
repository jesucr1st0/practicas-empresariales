from src.modulos.postulaciones.aplicacion.dto import PostulacionDTO, ResultadoPostulacionDTO
from src.modulos.postulaciones.dominio.estado_postulacion import EstadoPostulacion
from src.modulos.postulaciones.dominio.postulacion import Postulacion
from src.modulos.postulaciones.dominio.puertos.consulta_academica import (
    ConsultaAcademica,
    SIATimeoutError,
    SIAError,
)
from src.modulos.postulaciones.dominio.puertos.envio_correo import EnvioCorreo
from src.modulos.postulaciones.dominio.puertos.postulacion_repository import PostulacionRepository


class PostulacionDuplicadaError(Exception):
    pass


class RealizarPostulacion:
    CORREO_COORDINADOR = "coordinacion.practicas@universidad.edu.co"

    def __init__(
        self,
        repositorio: PostulacionRepository,
        consulta_academica: ConsultaAcademica,
        envio_correo: EnvioCorreo,
    ) -> None:
        self._repositorio = repositorio
        self._consulta_academica = consulta_academica
        self._envio_correo = envio_correo

    def ejecutar(self, dto: PostulacionDTO) -> ResultadoPostulacionDTO:
        # 1. Verificar si ya existe postulación activa
        activa = self._repositorio.obtener_activa_por_estudiante(dto.estudiante_documento)
        if activa is not None and activa.estado in (
            EstadoPostulacion.PENDIENTE_VERIFICACION,
            EstadoPostulacion.VERIFICADA,
        ):
            raise PostulacionDuplicadaError(
                f"El estudiante {dto.estudiante_documento} ya cuenta con una postulación activa en estado '{activa.estado.value}'."
            )

        # 2. Crear postulación en estado PENDIENTE_VERIFICACION
        postulacion = Postulacion.crear(
            estudiante_documento=dto.estudiante_documento,
            programa=dto.programa,
        )
        # Se guarda inmediatamente para garantizar: 0 postulaciones perdidas (EAC-03)
        self._repositorio.guardar(postulacion)

        correo_dest = dto.correo_estudiante or f"{dto.estudiante_documento}@universidad.edu.co"

        # 3. Intentar consultar datos académicos al SIA con timeout de 10s
        try:
            resultado_sia = self._consulta_academica.verificar_requisitos(
                estudiante_documento=dto.estudiante_documento,
                programa=dto.programa,
                timeout_segundos=10.0,
            )

            if resultado_sia.cumple_requisitos:
                postulacion.marcar_verificada()
                self._repositorio.guardar(postulacion)

                self._envio_correo.enviar(
                    destinatario=correo_dest,
                    asunto="Confirmación de postulación a práctica",
                    cuerpo=f"Su postulación {postulacion.id} ha sido verificada exitosamente.",
                )
                self._envio_correo.enviar(
                    destinatario=self.CORREO_COORDINADOR,
                    asunto="Nueva postulación verificada",
                    cuerpo=f"La postulación {postulacion.id} del estudiante {postulacion.estudiante_documento} fue verificada.",
                )
                mensaje = "Postulación verificada exitosamente."
            else:
                motivo = resultado_sia.motivo or "No cumple con los requisitos académicos."
                postulacion.marcar_rechazada(motivo)
                self._repositorio.guardar(postulacion)

                self._envio_correo.enviar(
                    destinatario=correo_dest,
                    asunto="Resultado de postulación a práctica",
                    cuerpo=f"Su postulación fue rechazada por el siguiente motivo: {motivo}",
                )
                mensaje = f"Postulación rechazada: {motivo}"

        except (SIATimeoutError, SIAError):
            # El SIA no responde a tiempo (EAC-03): permanece en pendiente_verificacion
            postulacion.registrar_intento_fallido()
            self._repositorio.guardar(postulacion)

            self._envio_correo.enviar(
                destinatario=correo_dest,
                asunto="Postulación recibida - Verificación pendiente",
                cuerpo="El servicio del SIA no respondió a tiempo. Su postulación quedó en estado 'pendiente de verificación' y se reintentará automáticamente.",
            )
            mensaje = "El SIA no respondió a tiempo. La postulación se encuentra en verificación pendiente."

        return ResultadoPostulacionDTO(
            id=postulacion.id,
            estudiante_documento=postulacion.estudiante_documento,
            programa=postulacion.programa,
            estado=postulacion.estado.value,
            fecha_creacion=postulacion.fecha_creacion,
            mensaje=mensaje,
            motivo_rechazo=postulacion.motivo_rechazo,
        )
