from src.modulos.practicas.aplicacion.dto_consulta_estudiante import DatosEstudianteDTO
from src.modulos.practicas.dominio.puertos.consulta_academica_estudiante import (
    ConsultaAcademicaEstudiante,
    SIAError,
    SIATimeoutError,
)
from src.modulos.practicas.dominio.puertos.practica_repository import PracticaRepository


class ConsultarDatosEstudiante:
    """Caso de uso CU-12: Consultar datos del estudiante con regla de alcance y tolerancia a fallos del SIA."""

    ROL_COORDINADOR = "Coordinador de prácticas"
    ROL_ADMINISTRADOR = "Administrador"
    ROL_TUTOR = "Tutor"

    def __init__(
        self,
        practica_repository: PracticaRepository,
        servicio_sia: ConsultaAcademicaEstudiante,
    ) -> None:
        self._practica_repository = practica_repository
        self._servicio_sia = servicio_sia

    def ejecutar(
        self,
        estudiante_documento: str,
        rol: str,
        tutor_documento: str | None = None,
    ) -> DatosEstudianteDTO:
        doc_limpio = estudiante_documento.strip() if estudiante_documento else ""
        if not doc_limpio:
            raise ValueError("El documento del estudiante es obligatorio.")

        # Obtener práctica activa del estudiante si existe
        practica = self._practica_repository.obtener_activa_por_estudiante(doc_limpio)

        # Regla de alcance y control de acceso (ADR-005)
        if rol == self.ROL_TUTOR:
            if not tutor_documento:
                raise PermissionError(
                    "Regla de alcance: se requiere la identificación del tutor para validar la asignación."
                )
            if practica is None or practica.tutor_documento != tutor_documento:
                raise PermissionError(
                    "Regla de alcance: el tutor solo puede consultar datos de sus estudiantes asignados."
                )
        elif rol not in (self.ROL_COORDINADOR, self.ROL_ADMINISTRADOR):
            raise PermissionError(
                f"El rol {rol!r} no tiene permisos para consultar datos de estudiantes."
            )

        # Consulta de datos académicos al SIA con tolerancia a fallos (RT-03, EAC-03)
        try:
            datos_academicos = self._servicio_sia.consultar_academica(doc_limpio)
            creditos = datos_academicos.creditos_aprobados
            promedio = datos_academicos.promedio_acumulado
            semestre = datos_academicos.semestre_actual
            matricula = datos_academicos.matricula_activa
            disponible_sia = datos_academicos.disponible_sia
            mensaje_sia = (
                datos_academicos.mensaje_estado
                or "Datos académicos sincronizados correctamente desde el SIA."
            )
        except (SIATimeoutError, SIAError, Exception) as error:
            creditos = None
            promedio = None
            semestre = None
            matricula = None
            disponible_sia = False
            mensaje_sia = f"Datos académicos del SIA no disponibles temporalmente ({error})."

        tiene_practica = practica is not None
        practica_id = practica.id if practica else None
        programa = practica.programa if practica else None
        estado_practica = (
            practica.estado.value if practica and hasattr(practica.estado, "value")
            else str(practica.estado) if practica else None
        )
        periodo = practica.periodo if practica else None
        empresa_id = practica.empresa_id if practica else None
        supervisor_id = practica.supervisor_id if practica else None
        tutor_vigente = practica.tutor_documento if practica else None
        horas_minimas = practica.horas_minimas_exigidas if practica else None

        return DatosEstudianteDTO(
            estudiante_documento=doc_limpio,
            tiene_practica_activa=tiene_practica,
            practica_id=practica_id,
            programa=programa,
            estado_practica=estado_practica,
            periodo=periodo,
            empresa_id=empresa_id,
            supervisor_id=supervisor_id,
            tutor_documento=tutor_vigente,
            horas_minimas_exigidas=horas_minimas,
            creditos_aprobados=creditos,
            promedio_acumulado=promedio,
            semestre_actual=semestre,
            matricula_activa=matricula,
            disponible_sia=disponible_sia,
            mensaje_sia=mensaje_sia,
        )
