from datetime import date
from uuid import UUID
from src.modulos.practicas.dominio.puertos.servicio_consulta_postulacion import ServicioConsultaPostulacion
from src.modulos.practicas.dominio.puertos.servicio_consulta_reglas import (
    InfoReglaVigente,
    ServicioConsultaReglas,
)
from src.modulos.reglas.aplicacion.resolver_regla_vigente import ResolverReglaVigente


class AdaptadorServicioReglas(ServicioConsultaReglas):
    def __init__(self, resolver_regla: ResolverReglaVigente) -> None:
        self._resolver_regla = resolver_regla

    def consultar_regla_vigente(self, programa: str, fecha: date) -> InfoReglaVigente | None:
        regla = self._resolver_regla.ejecutar(programa, fecha)
        if regla is None:
            return None
        return InfoReglaVigente(
            id=regla.id,
            version=regla.version,
            horas_minimas=regla.horas_minimas,
            capacidad_maxima_tutor=regla.capacidad_maxima_tutor,
        )


class AdaptadorServicioPostulacionSimulado(ServicioConsultaPostulacion):
    def __init__(self) -> None:
        self._postulaciones_verificadas: set[UUID] = set()

    def registrar_verificada(self, postulacion_id: UUID) -> None:
        self._postulaciones_verificadas.add(postulacion_id)

    def postulacion_esta_verificada(self, postulacion_id: UUID) -> bool:
        return postulacion_id in self._postulaciones_verificadas
