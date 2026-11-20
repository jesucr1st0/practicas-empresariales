from datetime import datetime, timezone, timedelta
from uuid import UUID
from src.modulos.postulaciones.dominio.estado_postulacion import EstadoPostulacion
from src.modulos.postulaciones.dominio.puertos.consulta_academica import (
    ConsultaAcademica,
    SIATimeoutError,
    SIAError,
)
from src.modulos.postulaciones.dominio.puertos.envio_correo import EnvioCorreo
from src.modulos.postulaciones.dominio.puertos.postulacion_repository import PostulacionRepository


class VerificarPostulacionPendiente:
    CORREO_COORDINADOR = "coordinacion.practicas@universidad.edu.co"
    VENTANA_MAXIMA_HORAS = 24.0

    def __init__(
        self,
        repositorio: PostulacionRepository,
        consulta_academica: ConsultaAcademica,
        envio_correo: EnvioCorreo,
    ) -> None:
        self._repositorio = repositorio
        self._consulta_academica = consulta_academica
        self._envio_correo = envio_correo

    def ejecutar_para_postulacion(
        self,
        postulacion_id: UUID,
        ahora: datetime | None = None,
    ) -> bool:
        postulacion = self._repositorio.obtener_por_id(postulacion_id)
        if postulacion is None or postulacion.estado != EstadoPostulacion.PENDIENTE_VERIFICACION:
            return False

        momento_actual = ahora or datetime.now(timezone.utc)
        tiempo_transcurrido = momento_actual - postulacion.fecha_creacion

        # Si se superan las 24 horas de reintentos sin éxito
        if tiempo_transcurrido >= timedelta(hours=self.VENTANA_MAXIMA_HORAS):
            postulacion.pasar_a_revision_manual()
            self._repositorio.guardar(postulacion)

            self._envio_correo.enviar(
                destinatario=self.CORREO_COORDINADOR,
                asunto="Postulación derivada a revisión manual",
                cuerpo=f"La postulación {postulacion.id} del estudiante {postulacion.estudiante_documento} superó 24h sin respuesta del SIA y requiere revisión manual.",
            )
            return True

        # Intento de reintento contra el SIA
        correo_est = f"{postulacion.estudiante_documento}@universidad.edu.co"
        try:
            resultado = self._consulta_academica.verificar_requisitos(
                estudiante_documento=postulacion.estudiante_documento,
                programa=postulacion.programa,
                timeout_segundos=5.0,
            )
            if resultado.cumple_requisitos:
                postulacion.marcar_verificada()
                self._repositorio.guardar(postulacion)
                self._envio_correo.enviar(
                    destinatario=correo_est,
                    asunto="Postulación verificada tras reintento",
                    cuerpo=f"Su postulación {postulacion.id} ha sido verificada exitosamente.",
                )
            else:
                motivo = resultado.motivo or "Requisitos académicos no cumplidos."
                postulacion.marcar_rechazada(motivo)
                self._repositorio.guardar(postulacion)
                self._envio_correo.enviar(
                    destinatario=correo_est,
                    asunto="Postulación rechazada tras reintento",
                    cuerpo=f"Su postulación fue rechazada: {motivo}",
                )
            return True

        except (SIATimeoutError, SIAError):
            postulacion.registrar_intento_fallido(fecha=momento_actual)
            self._repositorio.guardar(postulacion)
            return False

    def procesar_todas_las_pendientes(self, ahora: datetime | None = None) -> int:
        pendientes = self._repositorio.listar_pendientes()
        procesadas = 0
        for p in pendientes:
            if self.ejecutar_para_postulacion(p.id, ahora=ahora):
                procesadas += 1
        return procesadas
