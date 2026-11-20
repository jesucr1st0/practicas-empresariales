import unittest
from uuid import uuid4

from src.modulos.tutores_asignacion.aplicacion.confirmar_asignacion import ConfirmarAsignacion
from src.modulos.tutores_asignacion.aplicacion.confirmar_asignacion_dto import ConfirmarAsignacionDTO
from src.modulos.tutores_asignacion.aplicacion.sugerir_tutor import SugerirTutor
from src.modulos.tutores_asignacion.dominio.asignacion_tutor import AsignacionTutor
from src.modulos.tutores_asignacion.dominio.origen_asignacion import OrigenAsignacion
from src.modulos.tutores_asignacion.dominio.tutor import Tutor
from src.entradas.controlador_asignacion_tutor import ControladorAsignacionTutor
from src.modulos.tutores_asignacion.infraestructura.adaptador_asignacion_memoria import AdaptadorAsignacionMemoria
from src.modulos.tutores_asignacion.infraestructura.adaptador_servicio_practica_memoria import AdaptadorServicioPracticaMemoria
from src.modulos.tutores_asignacion.infraestructura.adaptador_servicio_reglas_memoria import AdaptadorServicioReglasMemoria


class AsignacionTutorTests(unittest.TestCase):
    def setUp(self):
        self.practica_id = uuid4()
        self.tutor_a = Tutor("T-001", "Profesor A", "a@example.edu", "Ingeniería de Sistemas")
        self.tutor_b = Tutor("T-002", "Profesor B", "b@example.edu", "Ingeniería de Sistemas")
        self.tutor_c = Tutor("T-003", "Profesor C", "c@example.edu", "Ingeniería Industrial")
        self.tutor_d = Tutor("T-004", "Profesor D", "d@example.edu", "Ingeniería de Sistemas")
        self.repositorio = AdaptadorAsignacionMemoria([self.tutor_a, self.tutor_b])
        self.practicas = AdaptadorServicioPracticaMemoria(
            {self.practica_id: ("Ingeniería de Sistemas", "regla-v1")}
        )
        self.reglas = AdaptadorServicioReglasMemoria({"regla-v1": 10})
        self.sugerir = SugerirTutor(self.repositorio, self.practicas, self.reglas)
        self.confirmar = ConfirmarAsignacion(self.repositorio, self.practicas, self.reglas)

    def _agregar_carga(self, tutor, cantidad):
        for _ in range(cantidad):
            self.repositorio.guardar(
                AsignacionTutor(practica_id=uuid4(), tutor_documento=tutor.documento)
            )

    def test_suggests_least_loaded_tutor_and_confirms_suggestion(self):
        self._agregar_carga(self.tutor_a, 4)
        self._agregar_carga(self.tutor_b, 7)

        sugerencia = self.sugerir.ejecutar(self.practica_id)
        resultado = self.confirmar.ejecutar(
            ConfirmarAsignacionDTO(
                self.practica_id,
                self.tutor_a.documento,
                OrigenAsignacion.SUGERIDA,
            )
        )

        self.assertEqual(self.tutor_a.documento, sugerencia.tutor_documento)
        self.assertEqual(4, sugerencia.carga_actual)
        self.assertIsNotNone(resultado.asignacion)
        self.assertTrue(resultado.asignacion.vigente)
        self.assertEqual(OrigenAsignacion.SUGERIDA, resultado.asignacion.origen)
        self.assertEqual(self.tutor_a.documento, self.practicas.obtener_tutor_vigente(self.practica_id))

    def test_manual_choice_is_saved_without_persisting_unconfirmed_suggestion(self):
        self._agregar_carga(self.tutor_a, 4)
        self._agregar_carga(self.tutor_b, 7)
        self.sugerir.ejecutar(self.practica_id)

        resultado = self.confirmar.ejecutar(
            ConfirmarAsignacionDTO(
                self.practica_id,
                self.tutor_b.documento,
                OrigenAsignacion.MANUAL,
            )
        )

        self.assertEqual(OrigenAsignacion.MANUAL, resultado.asignacion.origen)
        self.assertEqual(self.tutor_b.documento, resultado.asignacion.tutor_documento)
        self.assertEqual(1, len(self.repositorio.obtener_historial_por_practica(self.practica_id)))

    def test_over_capacity_requires_explicit_confirmation_and_is_recorded(self):
        self.repositorio = AdaptadorAsignacionMemoria(
            [self.tutor_a, self.tutor_b, self.tutor_c]
        )
        self.practicas = AdaptadorServicioPracticaMemoria(
            {self.practica_id: ("Ingeniería Industrial", "regla-v1")}
        )
        self._agregar_carga(self.tutor_c, 8)
        self.reglas = AdaptadorServicioReglasMemoria({"regla-v1": 8})
        self.confirmar = ConfirmarAsignacion(self.repositorio, self.practicas, self.reglas)

        advertencia = self.confirmar.ejecutar(
            ConfirmarAsignacionDTO(
                self.practica_id,
                self.tutor_c.documento,
                OrigenAsignacion.MANUAL,
            )
        )
        confirmacion = self.confirmar.ejecutar(
            ConfirmarAsignacionDTO(
                self.practica_id,
                self.tutor_c.documento,
                OrigenAsignacion.MANUAL,
                confirmar_sobrecupo=True,
            )
        )

        self.assertTrue(advertencia.advertencia_sobrecupo)
        self.assertIsNone(advertencia.asignacion)
        self.assertIsNotNone(confirmacion.asignacion)
        self.assertEqual(OrigenAsignacion.MANUAL, confirmacion.asignacion.origen)
        self.assertIn("8/8", confirmacion.asignacion.observaciones)

    def test_reassignment_keeps_old_assignment_as_inactive_history(self):
        self.repositorio = AdaptadorAsignacionMemoria(
            [self.tutor_a, self.tutor_b, self.tutor_d]
        )
        self.confirmar = ConfirmarAsignacion(self.repositorio, self.practicas, self.reglas)
        asignacion_previa = AsignacionTutor(
            practica_id=self.practica_id,
            tutor_documento=self.tutor_a.documento,
            origen=OrigenAsignacion.SUGERIDA,
        )
        self.repositorio.guardar(asignacion_previa)

        resultado = self.confirmar.ejecutar(
            ConfirmarAsignacionDTO(
                self.practica_id,
                self.tutor_d.documento,
                OrigenAsignacion.MANUAL,
            )
        )
        historial = self.repositorio.obtener_historial_por_practica(self.practica_id)

        self.assertFalse(asignacion_previa.vigente)
        self.assertEqual(2, len(historial))
        self.assertEqual(self.tutor_d.documento, resultado.asignacion.tutor_documento)
        self.assertEqual(self.tutor_d.documento, self.practicas.obtener_tutor_vigente(self.practica_id))
        self.assertFalse(self.practicas.puede_tutor_consultar(self.practica_id, self.tutor_a.documento))
        self.assertTrue(self.practicas.puede_tutor_consultar(self.practica_id, self.tutor_d.documento))

    def test_controller_checks_coordinator_role_and_records_access(self):
        accesos = []
        controlador = ControladorAsignacionTutor(
            self.sugerir,
            self.confirmar,
            lambda usuario, accion: accesos.append((usuario, accion)),
        )

        with self.assertRaises(PermissionError):
            controlador.sugerir(self.practica_id, "usuario-1", "Tutor")

        self.assertEqual("usuario-1", accesos[0][0])
        self.assertEqual(1, len(accesos))


if __name__ == "__main__":
    unittest.main()
