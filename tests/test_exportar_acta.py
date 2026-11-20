import hashlib
import unittest
from uuid import uuid4

from src.entradas.controlador_exportar_acta import ControladorExportarActa
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
from src.modulos.identidad_accesos.aplicacion.autorizador_accesos import (
    AutorizadorAccesos,
)
from src.modulos.identidad_accesos.dominio.rol import Rol
from src.modulos.identidad_accesos.dominio.usuario_autenticado import (
    UsuarioAutenticado,
)
from src.modulos.identidad_accesos.infraestructura.adaptador_bitacora_memoria import (
    AdaptadorBitacoraMemoria,
)

IP = "10.0.0.15"
AGENTE = "Firefox"


class ExportarActaTests(unittest.TestCase):
    def setUp(self):
        self.practica_id = uuid4()
        self.consulta_practica = AdaptadorConsultaPracticaMemoria(
            {
                self.practica_id: DatosPracticaActa(
                    practica_id=self.practica_id,
                    version_regla="v1",
                    programa="Ingeniería de Sistemas",
                    estudiante_documento="1001234567",
                    estudiante_nombre="Laura Gómez",
                    empresa_nombre="Tech Solutions S.A.S.",
                )
            }
        )
        self.repo_actas = AdaptadorActaFinalMemoria()
        self.almacen = AdaptadorAlmacenArchivosMemoria()
        self.generar = GenerarActaFinal(
            self.repo_actas,
            self.almacen,
            self.consulta_practica,
            AdaptadorConsultaHorasMemoria({self.practica_id: 480}),
            AdaptadorConsultaEvaluacionMemoria({self.practica_id: 4.5}),
            AdaptadorConsultaReglasMemoria({"v1": 480}),
            AdaptadorGeneradorPlantillaOficial(),
        )
        self.acta = self.generar.ejecutar(GenerarActaDTO(practica_id=self.practica_id))

        self.bitacora = AdaptadorBitacoraMemoria()
        self.controlador = ControladorExportarActa(
            ExportarActaFinal(self.repo_actas, self.almacen, self.consulta_practica),
            AutorizadorAccesos(self.bitacora),
        )
        self.coordinador = UsuarioAutenticado("C-001", Rol.COORDINADOR)

    def _ultimo_registro(self):
        return self.bitacora.listar()[-1]

    def test_escenario_1_coordinador_exporta_acta_vigente(self):
        resultado = self.controlador.exportar_acta(
            self.coordinador, self.practica_id, IP, AGENTE
        )

        contenido_original = self.almacen.obtener_archivo(self.acta.ruta_archivo)
        self.assertEqual(contenido_original, resultado.contenido)
        self.assertEqual(
            self.acta.huella_integridad, hashlib.sha256(resultado.contenido).hexdigest()
        )
        self.assertEqual(f"acta_final_{self.practica_id}.pdf", resultado.nombre_archivo)

        registro = self._ultimo_registro()
        self.assertTrue(registro.exitoso)
        self.assertEqual("C-001", registro.sujeto)
        self.assertEqual("exportar_acta", registro.accion)
        self.assertEqual(IP, registro.ip)
        self.assertEqual(AGENTE, registro.agente_usuario)
        self.assertIsNotNone(registro.fecha)

    def test_escenario_2_estudiante_titular_exporta_su_acta(self):
        estudiante = UsuarioAutenticado("1001234567", Rol.ESTUDIANTE)

        resultado = self.controlador.exportar_acta(
            estudiante, self.practica_id, IP, AGENTE
        )

        self.assertEqual(self.acta.huella_integridad, resultado.huella_integridad)
        self.assertTrue(self._ultimo_registro().exitoso)
        self.assertEqual("1001234567", self._ultimo_registro().sujeto)

    def test_escenario_3_estudiante_ajeno_es_denegado(self):
        ajeno = UsuarioAutenticado("1009999999", Rol.ESTUDIANTE)

        with self.assertRaisesRegex(PermissionError, "alcance"):
            self.controlador.exportar_acta(ajeno, self.practica_id, IP, AGENTE)

        registro = self._ultimo_registro()
        self.assertFalse(registro.exitoso)
        self.assertEqual("1009999999", registro.sujeto)

    def test_escenario_4_rol_no_autorizado_es_denegado(self):
        tutor = UsuarioAutenticado("T-001", Rol.TUTOR)

        with self.assertRaisesRegex(PermissionError, "Tutor"):
            self.controlador.exportar_acta(tutor, self.practica_id, IP, AGENTE)

        registro = self._ultimo_registro()
        self.assertFalse(registro.exitoso)
        self.assertEqual("T-001", registro.sujeto)
        self.assertEqual(1, len(self.bitacora.listar()))

    def test_escenario_5_exporta_solo_el_acta_vigente_tras_correccion(self):
        acta_corregida = self.generar.ejecutar(
            GenerarActaDTO(practica_id=self.practica_id)
        )
        resultado = self.controlador.exportar_acta(
            self.coordinador, self.practica_id, IP, AGENTE
        )

        estados = {a.id: a.estado for a in self.repo_actas.listar_por_practica(self.practica_id)}
        self.assertEqual(EstadoActa.ANULADA, estados[self.acta.id])
        self.assertEqual(EstadoActa.VIGENTE, estados[acta_corregida.id])
        self.assertEqual(acta_corregida.huella_integridad, resultado.huella_integridad)

    def test_escenario_6_practica_sin_acta_vigente(self):
        otra_practica = uuid4()

        with self.assertRaisesRegex(ValueError, "No existe un acta final vigente"):
            self.controlador.exportar_acta(self.coordinador, otra_practica, IP, AGENTE)

        self.assertFalse(self._ultimo_registro().exitoso)

    def test_escenario_7_archivo_alterado_no_se_entrega(self):
        self.almacen.guardar_archivo(self.acta.ruta_archivo, b"contenido adulterado")

        with self.assertRaisesRegex(ValueError, "integridad"):
            self.controlador.exportar_acta(
                self.coordinador, self.practica_id, IP, AGENTE
            )

        registro = self._ultimo_registro()
        self.assertFalse(registro.exitoso)
        self.assertIn("integridad", registro.detalle)


if __name__ == "__main__":
    unittest.main()
