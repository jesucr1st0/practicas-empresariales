from datetime import date
import unittest
from uuid import uuid4

from src.entradas.controlador_consulta_tutor import ControladorConsultaTutor
from src.modulos.identidad_accesos.infraestructura.adaptador_bitacora_memoria import (
    AdaptadorBitacoraMemoria,
)
from src.modulos.tutores_asignacion.aplicacion.consultar_datos_tutor import ConsultarDatosTutor
from src.modulos.tutores_asignacion.aplicacion.listar_tutores_programa import ListarTutoresPrograma
from src.modulos.tutores_asignacion.dominio.asignacion_tutor import AsignacionTutor
from src.modulos.tutores_asignacion.dominio.origen_asignacion import OrigenAsignacion
from src.modulos.tutores_asignacion.dominio.tutor import Tutor
from src.modulos.tutores_asignacion.infraestructura.adaptador_asignacion_memoria import (
    AdaptadorAsignacionMemoria,
)
from src.modulos.tutores_asignacion.infraestructura.adaptador_servicio_reglas_memoria import (
    AdaptadorServicioReglasMemoria,
)
from src.modulos.tutores_asignacion.infraestructura.adaptador_sia_tutor_memoria import (
    AdaptadorSIATutorMemoria,
)


class ConsultarDatosTutorTests(unittest.TestCase):
    def setUp(self):
        self.tutor_101 = Tutor(
            documento="T-101",
            nombre="Profesor Juan Pérez",
            correo="juan.perez@universidad.edu.co",
            programa="Ingeniería de Sistemas",
            activo=True,
        )
        self.tutor_102 = Tutor(
            documento="T-102",
            nombre="Profesora María Gómez",
            correo="maria.gomez@universidad.edu.co",
            programa="Ingeniería de Sistemas",
            activo=True,
        )

        self.repo_asignaciones = AdaptadorAsignacionMemoria([self.tutor_101, self.tutor_102])
        self.repo_reglas = AdaptadorServicioReglasMemoria({"Ingeniería de Sistemas": 10})
        self.adaptador_sia = AdaptadorSIATutorMemoria()
        self.adaptador_sia.configurar_docente(
            documento="T-101",
            departamento="Sistemas e Informática",
            categoria="Asociado",
            dedicacion="Tiempo Completo",
        )

        self.bitacora = AdaptadorBitacoraMemoria()

        self.caso_uso_consultar = ConsultarDatosTutor(
            asignaciones=self.repo_asignaciones,
            reglas=self.repo_reglas,
            servicio_sia=self.adaptador_sia,
        )
        self.caso_uso_listar = ListarTutoresPrograma(
            asignaciones=self.repo_asignaciones,
            reglas=self.repo_reglas,
        )

        self.controlador = ControladorConsultaTutor(
            consultar_datos_tutor=self.caso_uso_consultar,
            listar_tutores_programa=self.caso_uso_listar,
            registrar_acceso=self.bitacora,
        )

    def _asignar_practicas(self, tutor_documento: str, cantidad: int):
        for _ in range(cantidad):
            self.repo_asignaciones.guardar(
                AsignacionTutor(
                    practica_id=uuid4(),
                    tutor_documento=tutor_documento,
                    fecha=date(2026, 8, 15),
                    vigente=True,
                    origen=OrigenAsignacion.SUGERIDA,
                )
            )

    def test_consulta_exitosa_datos_tutor_con_sia_y_bitacora(self):
        """Escenario 1: Consulta exitosa de datos de tutor por el Coordinador de prácticas."""
        self._asignar_practicas("T-101", 3)

        dto = self.controlador.consultar_tutor(
            tutor_documento="T-101",
            usuario_id="coordinador-01",
            rol="Coordinador de prácticas",
            ip="192.168.1.50",
            agente_usuario="Mozilla/5.0",
        )

        self.assertEqual("T-101", dto.documento)
        self.assertEqual("Profesor Juan Pérez", dto.nombre)
        self.assertEqual("juan.perez@universidad.edu.co", dto.correo)
        self.assertEqual("Ingeniería de Sistemas", dto.programa)
        self.assertEqual("Sistemas e Informática", dto.departamento)
        self.assertEqual("Asociado", dto.categoria)
        self.assertEqual("Tiempo Completo", dto.dedicacion)
        self.assertTrue(dto.disponible_sia)
        self.assertEqual(3, dto.carga_actual)
        self.assertEqual(10, dto.capacidad_maxima)
        self.assertEqual(7, dto.cupos_disponibles)
        self.assertFalse(dto.sobrecupo)
        self.assertEqual(3, len(dto.practicas_asignadas))

        # Verificar bitácora de accesos (ADR-005, RN-01)
        registros = self.bitacora.listar()
        self.assertEqual(1, len(registros))
        self.assertEqual("coordinador-01", registros[0].sujeto)
        self.assertEqual("CU-11: consultar datos tutor", registros[0].accion)
        self.assertEqual("192.168.1.50", registros[0].ip)
        self.assertEqual("Mozilla/5.0", registros[0].agente_usuario)
        self.assertTrue(registros[0].exitoso)

    def test_consulta_tutor_inexistente_registra_en_bitacora(self):
        """Escenario 2: Consulta de tutor inexistente."""
        with self.assertRaises(LookupError):
            self.controlador.consultar_tutor(
                tutor_documento="T-999",
                usuario_id="coordinador-01",
                rol="Coordinador de prácticas",
                ip="192.168.1.50",
            )

        registros = self.bitacora.listar()
        self.assertEqual(1, len(registros))
        self.assertFalse(registros[0].exitoso)
        self.assertIn("T-999", registros[0].detalle)

    def test_usuario_no_autorizado_es_denegado_y_registrado_en_bitacora(self):
        """Escenario 3: Usuario no autorizado intenta consultar datos de tutor (ADR-005)."""
        with self.assertRaises(PermissionError):
            self.controlador.consultar_tutor(
                tutor_documento="T-101",
                usuario_id="estudiante-45",
                rol="Estudiante",
                ip="192.168.1.80",
            )

        registros = self.bitacora.listar()
        self.assertEqual(1, len(registros))
        self.assertEqual("estudiante-45", registros[0].sujeto)
        self.assertFalse(registros[0].exitoso)
        self.assertIn("Acceso denegado", registros[0].detalle)

    def test_tolerancia_a_fallos_cuando_sia_no_responde_o_timeout(self):
        """Escenario 4: SIA no responde o se encuentra caído (EAC-03, RT-03, PA-01)."""
        self._asignar_practicas("T-101", 3)
        self.adaptador_sia.simular_timeout(True)

        dto = self.controlador.consultar_tutor(
            tutor_documento="T-101",
            usuario_id="coordinador-01",
            rol="Coordinador de prácticas",
        )

        self.assertEqual("T-101", dto.documento)
        self.assertFalse(dto.disponible_sia)
        self.assertEqual("No disponible", dto.departamento)
        self.assertIn("no disponibles temporalmente", dto.mensaje_sia)
        self.assertEqual(3, dto.carga_actual)
        self.assertEqual(3, len(dto.practicas_asignadas))

    def test_listar_tutores_por_programa_para_tablero_de_estado(self):
        """Escenario 5: Listar tutores por programa para el tablero de estado (CU-11, ADR-012)."""
        self._asignar_practicas("T-101", 3)
        self._asignar_practicas("T-102", 7)

        resumenes = self.controlador.listar_tutores_programa(
            programa="Ingeniería de Sistemas",
            usuario_id="coordinador-01",
            rol="Coordinador de prácticas",
        )

        self.assertEqual(2, len(resumenes))
        t1 = next(t for t in resumenes if t.documento == "T-101")
        t2 = next(t for t in resumenes if t.documento == "T-102")

        self.assertEqual(3, t1.carga_actual)
        self.assertEqual(7, t1.cupos_disponibles)
        self.assertFalse(t1.sobrecupo)

        self.assertEqual(7, t2.carga_actual)
        self.assertEqual(3, t2.cupos_disponibles)
        self.assertFalse(t2.sobrecupo)

        registros = self.bitacora.listar()
        self.assertEqual(1, len(registros))
        self.assertTrue(registros[0].exitoso)


if __name__ == "__main__":
    unittest.main()
