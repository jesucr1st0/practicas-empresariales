from datetime import datetime
import hashlib

from src.modulos.actas.dominio.puertos.generador_plantilla_acta import (
    GeneradorPlantillaActa,
)


class AdaptadorGeneradorPlantillaOficial(GeneradorPlantillaActa):
    PLANTILLA_VERSION = "v1.0-oficial-consejo-facultad"

    def generar_documento(
        self,
        programa: str,
        estudiante_nombre: str,
        estudiante_documento: str,
        empresa_nombre: str,
        version_regla: str,
        horas_validadas: int,
        calificacion: float,
        fecha_emision: datetime,
    ) -> tuple[bytes, str]:
        # Formato oficial del Consejo de Facultad (RN-03, ADR-010)
        cuerpo = (
            f"UNIVERSIDAD - CONSEJO DE FACULTAD\n"
            f"ACTA FINAL DE PRÁCTICA EMPRESARIAL\n"
            f"Plantilla Oficial: {self.PLANTILLA_VERSION}\n"
            f"----------------------------------------\n"
            f"Programa: {programa}\n"
            f"Estudiante: {estudiante_nombre} (Doc: {estudiante_documento})\n"
            f"Empresa: {empresa_nombre}\n"
            f"Versión de regla aplicada: {version_regla}\n"
            f"Horas validadas: {horas_validadas}\n"
            f"Calificación de empresa: {calificacion:.2f}\n"
            f"Fecha de emisión: {fecha_emision.isoformat()}\n"
            f"----------------------------------------\n"
            f"Estado: Aprobado y Cierre Oficial de Práctica.\n"
        )
        contenido_bytes = cuerpo.encode("utf-8")
        huella = hashlib.sha256(contenido_bytes).hexdigest()
        return contenido_bytes, huella
