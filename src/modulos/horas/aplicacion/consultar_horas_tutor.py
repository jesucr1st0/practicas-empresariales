from uuid import UUID

from src.modulos.horas.aplicacion.dto import RegistroHorasDTO, ResumenHorasTutorDTO
from src.modulos.horas.dominio.estado_validacion_horas import EstadoValidacionHoras
from src.modulos.horas.dominio.puertos.consulta_asignacion_tutor import ConsultaAsignacionTutor
from src.modulos.horas.dominio.puertos.registro_horas_repository import RegistroHorasRepository
from src.modulos.identidad_accesos.dominio.puertos.bitacora_acceso_repository import BitacoraAccesoRepository
from src.modulos.identidad_accesos.dominio.registro_acceso import RegistroAcceso


class ConsultarHorasTutor:
    def __init__(
        self,
        repositorio_horas: RegistroHorasRepository,
        consulta_asignacion: ConsultaAsignacionTutor,
        bitacora: BitacoraAccesoRepository,
    ):
        self._repositorio_horas = repositorio_horas
        self._consulta_asignacion = consulta_asignacion
        self._bitacora = bitacora

    def ejecutar(
        self,
        tutor_documento: str,
        practica_id: UUID,
        ip: str = "127.0.0.1",
        agente_usuario: str = "Interfaz web interna",
    ) -> ResumenHorasTutorDTO:
        if not self._consulta_asignacion.esta_asignado(tutor_documento, practica_id):
            self._bitacora.registrar(
                RegistroAcceso(
                    sujeto=tutor_documento,
                    accion="consultar_horas_tutor",
                    ip=ip,
                    agente_usuario=agente_usuario,
                    exitoso=False,
                    detalle=f"Acceso denegado: práctica {practica_id} fuera de alcance del tutor {tutor_documento}",
                )
            )
            raise PermissionError("Acceso denegado: la práctica no está en su alcance asignado")

        self._bitacora.registrar(
            RegistroAcceso(
                sujeto=tutor_documento,
                accion="consultar_horas_tutor",
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=True,
                detalle=f"Consulta de horas autorizada para práctica {practica_id}",
            )
        )

        registros = self._repositorio_horas.listar_por_practica(practica_id)
        dtos: list[RegistroHorasDTO] = []
        total = 0
        validadas = 0
        pendientes = 0

        for r in registros:
            total += r.cantidad_horas
            if r.estado_validacion == EstadoValidacionHoras.VALIDADO_SUPERVISOR:
                validadas += r.cantidad_horas
            elif r.estado_validacion == EstadoValidacionHoras.PENDIENTE:
                pendientes += r.cantidad_horas

            dtos.append(
                RegistroHorasDTO(
                    id=r.id,
                    practica_id=r.practica_id,
                    estudiante_documento=r.estudiante_documento,
                    fecha=r.fecha,
                    cantidad_horas=r.cantidad_horas,
                    evidencia=r.evidencia,
                    estado_validacion=r.estado_validacion.value,
                )
            )

        return ResumenHorasTutorDTO(
            practica_id=practica_id,
            total_horas=total,
            horas_validadas=validadas,
            horas_pendientes=pendientes,
            registros=dtos,
        )
