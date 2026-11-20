from datetime import datetime, timezone

from src.modulos.actas.aplicacion.dto import ActaFinalDTO, GenerarActaDTO
from src.modulos.actas.dominio.acta_final import ActaFinal
from src.modulos.actas.dominio.puertos.acta_final_repository import (
    ActaFinalRepository,
)
from src.modulos.actas.dominio.puertos.almacen_archivos import AlmacenArchivos
from src.modulos.actas.dominio.puertos.consulta_evaluacion_acta import (
    ConsultaEvaluacionActa,
)
from src.modulos.actas.dominio.puertos.consulta_horas_acta import ConsultaHorasActa
from src.modulos.actas.dominio.puertos.consulta_practica_acta import (
    ConsultaPracticaActa,
)
from src.modulos.actas.dominio.puertos.consulta_reglas_acta import (
    ConsultaReglasActa,
)
from src.modulos.actas.dominio.puertos.generador_plantilla_acta import (
    GeneradorPlantillaActa,
)


class GenerarActaFinal:
    def __init__(
        self,
        repositorio: ActaFinalRepository,
        almacen_archivos: AlmacenArchivos,
        consulta_practica: ConsultaPracticaActa,
        consulta_horas: ConsultaHorasActa,
        consulta_evaluacion: ConsultaEvaluacionActa,
        consulta_reglas: ConsultaReglasActa,
        generador_plantilla: GeneradorPlantillaActa,
    ):
        self._repositorio = repositorio
        self._almacen_archivos = almacen_archivos
        self._consulta_practica = consulta_practica
        self._consulta_horas = consulta_horas
        self._consulta_evaluacion = consulta_evaluacion
        self._consulta_reglas = consulta_reglas
        self._generador_plantilla = generador_plantilla

    def ejecutar(self, dto: GenerarActaDTO) -> ActaFinalDTO:
        datos_practica = self._consulta_practica.consultar_practica(dto.practica_id)
        if datos_practica is None:
            raise ValueError(f"Práctica {dto.practica_id} no encontrada")

        horas_minimas = self._consulta_reglas.obtener_horas_minimas(
            datos_practica.version_regla
        )
        horas_validadas = self._consulta_horas.obtener_horas_validadas(dto.practica_id)

        if horas_validadas < horas_minimas:
            raise ValueError(
                f"Horas validadas insuficientes ({horas_validadas}/{horas_minimas}); "
                f"no se cumplen las horas mínimas de la versión {datos_practica.version_regla}"
            )

        calificacion = self._consulta_evaluacion.obtener_calificacion_evaluacion(
            dto.practica_id
        )
        if calificacion is None:
            raise ValueError(
                "Evaluación de empresa pendiente; no se puede generar el acta sin evaluación"
            )

        fecha_emision = datetime.now(timezone.utc)
        contenido_bytes, huella_sha256 = self._generador_plantilla.generar_documento(
            programa=datos_practica.programa,
            estudiante_nombre=datos_practica.estudiante_nombre,
            estudiante_documento=datos_practica.estudiante_documento,
            empresa_nombre=datos_practica.empresa_nombre,
            version_regla=datos_practica.version_regla,
            horas_validadas=horas_validadas,
            calificacion=calificacion,
            fecha_emision=fecha_emision,
        )

        ruta_archivo = f"actas/{dto.practica_id}_{int(fecha_emision.timestamp())}.pdf"
        self._almacen_archivos.guardar_archivo(ruta_archivo, contenido_bytes)

        # Si ya existía un acta vigente (corrección), anula la anterior (ADR-010)
        acta_previa = self._repositorio.buscar_vigente_por_practica(dto.practica_id)
        if acta_previa:
            acta_previa.anular()
            self._repositorio.guardar(acta_previa)

        nueva_acta = ActaFinal(
            practica_id=dto.practica_id,
            huella_integridad=huella_sha256,
            version_regla=datos_practica.version_regla,
            horas_validadas=horas_validadas,
            calificacion_evaluacion=calificacion,
            ruta_archivo=ruta_archivo,
            fecha_emision=fecha_emision,
        )
        self._repositorio.guardar(nueva_acta)

        return ActaFinalDTO(
            id=nueva_acta.id,
            practica_id=nueva_acta.practica_id,
            fecha_emision=nueva_acta.fecha_emision,
            huella_integridad=nueva_acta.huella_integridad,
            estado=nueva_acta.estado.value,
            version_regla=nueva_acta.version_regla,
            horas_validadas=nueva_acta.horas_validadas,
            calificacion_evaluacion=nueva_acta.calificacion_evaluacion,
            ruta_archivo=nueva_acta.ruta_archivo,
            plantilla_version=nueva_acta.plantilla_version,
        )
