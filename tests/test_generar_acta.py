import hashlib
import unittest
from uuid import uuid4

from src.entradas.controlador_actas import ControladorActas
from src.modulos.actas.aplicacion.dto import GenerarActaDTO
from src.modulos.actas.aplicacion.exportar_acta_final import ExportarActaFinal
from src.modulos.actas.aplicacion.generar_acta_final import GenerarActaFinal
from src.modulos.actas.dominio.estado_acta import EstadoActa
from src.modulos.actas.dominio.puertos.consulta_practica_acta import (
    DatosPracticaActa,
)
from src.modulos.actas.infraestructura.adaptador_acta_final_memoria import (
    AdaptadorActaFinalMemoria,
)
from src.modulos.actas.infraestructura.adaptador_almacen_archivos_memoria import (
    AdaptadorAlmacenArchivosMemoria,
)
from src.modulos.actas.infraestructura.adaptador_consulta_evaluacion_memoria import (
    AdaptadorConsultaEvaluacionMemoria,
)
from src.modulos.actas.infraestructura.adaptador_consulta_horas_memoria import (
    AdaptadorConsultaHorasMemoria,
)
from src.modulos.actas.infraestructura.adaptador_consulta_practica_memoria import (
    AdaptadorConsultaPracticaMemoria,
)
from src.modulos.actas.infraestructura.adaptador_consulta_reglas_memoria import (
    AdaptadorConsultaReglasMemoria,
)
from src.modulos.actas.infraestructura.adaptador_generador_plantilla_oficial import (
    AdaptadorGeneradorPlantillaOficial,
)


class GenerarActaTests(unittest.TestCase):
    def setUp(self):
        self.practica_id = uuid4()
        self.datos_practica = DatosPracticaActa(
            practica_id=self.practica_id,
            version_regla="v1",
            programa="Ingeniería de Sistemas",
            estudiante_documento="1001234567",
            estudiante_nombre="Carlos Rodríguez",
            empresa_nombre="Tech Solutions S.A.S.",
        )

        # Repositorios y adaptadores
        self.repo_actas = AdaptadorActaFinalMemoria()
        self.almacen_archivos = AdaptadorAlmacenArchivosMemoria()
        self.consulta_practica = AdaptadorConsultaPracticaMemoria({self.practica_id: self.datos_practica})
        self.consulta_horas = AdaptadorConsultaHorasMemoria({self.practica_id: 480})
        self.consulta_evaluacion = AdaptadorConsultaEvaluacionMemoria({self.practica_id: 4.5})
        self.consulta_reglas = AdaptadorConsultaReglasMemoria({"v1": 480, "v2": 540})
        self.generador_plantilla = AdaptadorGeneradorPlantillaOficial()

        # Casos de uso
        self.cu_generar = GenerarActaFinal(
            self.repo_actas,
            self.almacen_archivos,
            self.consulta_practica,
            self.consulta_horas,
            self.consulta_evaluacion,
            self.consulta_reglas,
            self.generador_plantilla,
        )
        self.cu_exportar = ExportarActaFinal(self.repo_actas, self.almacen_archivos)

        # Controlador
        self.controlador = ControladorActas(self.cu_generar, self.cu_exportar)

    def test_escenario_1_generacion_exitosa_acta_final(self):
        dto = GenerarActaDTO(practica_id=self.practica_id)
        resultado = self.controlador.generar_acta(dto)

        self.assertEqual("vigente", resultado.estado)
        self.assertEqual(480, resultado.horas_validadas)
        self.assertEqual(4.5, resultado.calificacion_evaluacion)
        self.assertEqual("v1", resultado.version_regla)
        self.assertTrue(len(resultado.huella_integridad) == 64)  # SHA-256

        # Archivo guardado inmutablemente en el almacén
        archivo_bytes = self.almacen_archivos.obtener_archivo(resultado.ruta_archivo)
        huella_calculada = hashlib.sha256(archivo_bytes).hexdigest()
        self.assertEqual(resultado.huella_integridad, huella_calculada)

        # Trazabilidad en repositorio
        acta_guardada = self.repo_actas.buscar_vigente_por_practica(self.practica_id)
        self.assertIsNotNone(acta_guardada)
        self.assertEqual(EstadoActa.VIGENTE, acta_guardada.estado)

    def test_escenario_2_rechazo_horas_validadas_insuficientes(self):
        # Fijar 360 horas cuando la regla v1 pide 480
        self.consulta_horas.fijar_horas(self.practica_id, 360)

        with self.assertRaises(ValueError) as context:
            self.controlador.generar_acta(GenerarActaDTO(practica_id=self.practica_id))

        self.assertIn("Horas validadas insuficientes (360/480)", str(context.exception))
        self.assertIsNone(self.repo_actas.buscar_vigente_por_practica(self.practica_id))

    def test_escenario_3_rechazo_evaluacion_empresa_pendiente(self):
        # Práctica sin evaluación registrada
        practica_sin_eval = uuid4()
        self.consulta_practica.agregar_practica(
            DatosPracticaActa(
                practica_id=practica_sin_eval,
                version_regla="v1",
                programa="Ingeniería Industrial",
                estudiante_documento="1009876543",
                estudiante_nombre="Ana Gómez",
                empresa_nombre="Logística Andina",
            )
        )
        self.consulta_horas.fijar_horas(practica_sin_eval, 480)

        with self.assertRaises(ValueError) as context:
            self.controlador.generar_acta(GenerarActaDTO(practica_id=practica_sin_eval))

        self.assertIn("Evaluación de empresa pendiente", str(context.exception))

    def test_escenario_4_correccion_acta_anula_anterior_conservando_inmutabilidad(self):
        # Primera generación
        acta_1 = self.controlador.generar_acta(GenerarActaDTO(practica_id=self.practica_id))
        self.assertEqual("vigente", acta_1.estado)

        # Supongamos que se corrige la calificación a 4.8 y se genera nueva acta
        self.consulta_evaluacion.registrar_evaluacion(self.practica_id, 4.8)
        acta_2 = self.controlador.generar_acta(GenerarActaDTO(practica_id=self.practica_id))

        self.assertEqual("vigente", acta_2.estado)
        self.assertEqual(4.8, acta_2.calificacion_evaluacion)
        self.assertNotEqual(acta_1.id, acta_2.id)

        # Verificar que el acta previa pasó a ANULADA en el historial (ADR-010)
        historial = self.repo_actas.listar_por_practica(self.practica_id)
        self.assertEqual(2, len(historial))

        actas_anuladas = [a for a in historial if a.estado == EstadoActa.ANULADA]
        self.assertEqual(1, len(actas_anuladas))
        self.assertEqual(acta_1.id, actas_anuladas[0].id)

        acta_vigente = self.repo_actas.buscar_vigente_por_practica(self.practica_id)
        self.assertEqual(acta_2.id, acta_vigente.id)

    def test_escenario_5_exportar_acta_final_y_verificar_integridad(self):
        acta = self.controlador.generar_acta(GenerarActaDTO(practica_id=self.practica_id))

        # Exportación exitosa (CU-07)
        exportacion = self.controlador.exportar_acta(self.practica_id)
        self.assertEqual(acta.huella_integridad, exportacion.huella_integridad)
        self.assertTrue(exportacion.nombre_archivo.startswith("acta_final_"))

        # Simular alteración indebida del archivo en el almacén (falla de integridad)
        self.almacen_archivos.guardar_archivo(acta.ruta_archivo, b"contenido_corrupto_o_modificado")

        with self.assertRaises(ValueError) as context:
            self.controlador.exportar_acta(self.practica_id)
        self.assertIn("Fallo crítico de integridad", str(context.exception))


if __name__ == "__main__":
    unittest.main()
