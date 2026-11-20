from datetime import date
import unittest
from uuid import uuid4

from src.entradas.controlador_consulta_estudiante import ControladorConsultaEstudiante
from src.modulos.identidad_accesos.infraestructura.adaptador_bitacora_memoria import (
    AdaptadorBitacoraMemoria,
)
from src.modulos.practicas.aplicacion.consultar_datos_estudiante import ConsultarDatosEstudiante
from src.modulos.practicas.dominio.estado_practica import EstadoPractica
from src.modulos.practicas.dominio.practica import Practica
from src.modulos.practicas.infraestructura.adaptador_practica_memoria import (
    AdaptadorPracticaMemoria,
)
from src.modulos.practicas.infraestructura.adaptador_sia_estudiante_memoria import (
    AdaptadorSIAEstudianteMemoria,
)


class ConsultarDatosEstudianteTests(unittest.TestCase):
    def setUp(self):
        self.repo_practicas = AdaptadorPracticaMemoria()
        self.bitacora = AdaptadorBitacoraMemoria()
        self.adaptador_sia = AdaptadorSIAEstudianteMemoria()

        self.caso_uso_consultar = ConsultarDatosEstudiante(
            practica_repository=self.repo_practicas,
            servicio_sia=self.adaptador_sia,
        )

        self.controlador = ControladorConsultaEstudiante(
            caso_uso_consultar=self.caso_uso_consultar,
            registrar_acceso=self.bitacora,
        )

        # Configurar práctica para estudiante 1001234567 asignado a tutor T-101
        self.practica_1 = Practica(
            id=uuid4(),
            estudiante_documento="1001234567",
            programa="Ingeniería de Sistemas",
            empresa_id="TechCorp",
            supervisor_id="Carlos Pérez",
            periodo="2026-2",
            fecha_inicio=date(2026, 8, 1),
            fecha_fin=date(2026, 12, 15),
            estado=EstadoPractica.EN_CURSO,
            regla_id=uuid4(),
            regla_version="v1",
            horas_minimas_exigidas=480,
            tutor_documento="T-101",
        )
        self.repo_practicas.guardar(self.practica_1)

        # Configurar SIA para estudiante 1001234567
        self.adaptador_sia.configurar_estudiante(
            documento="1001234567",
            creditos_aprobados=140,
            promedio_acumulado=4.2,
            semestre_actual=9,
            matricula_activa=True,
        )

    def test_coordinador_consulta_estudiante_con_practica_y_sia(self):
        """Escenario 1: Coordinador consulta datos de estudiante con práctica activa y datos del SIA (flujo básico)."""
        dto = self.controlador.consultar_estudiante(
            estudiante_documento="1001234567",
            usuario_id="coordinador-01",
            rol="Coordinador de prácticas",
            ip="192.168.1.50",
            agente_usuario="Mozilla/5.0",
        )

        self.assertEqual("1001234567", dto.estudiante_documento)
        self.assertTrue(dto.tiene_practica_activa)
        self.assertEqual(self.practica_1.id, dto.practica_id)
        self.assertEqual("Ingeniería de Sistemas", dto.programa)
        self.assertEqual("en curso", dto.estado_practica)
        self.assertEqual("TechCorp", dto.empresa_id)
        self.assertEqual("T-101", dto.tutor_documento)
        self.assertEqual(480, dto.horas_minimas_exigidas)

        # Datos académicos del SIA
        self.assertTrue(dto.disponible_sia)
        self.assertEqual(140, dto.creditos_aprobados)
        self.assertEqual(4.2, dto.promedio_acumulado)
        self.assertEqual(9, dto.semestre_actual)
        self.assertTrue(dto.matricula_activa)

        # Bitácora (ADR-005, RN-01)
        registros = self.bitacora.listar()
        self.assertEqual(1, len(registros))
        self.assertEqual("coordinador-01", registros[0].sujeto)
        self.assertEqual("CU-12: consultar datos estudiante", registros[0].accion)
        self.assertEqual("192.168.1.50", registros[0].ip)
        self.assertTrue(registros[0].exitoso)

    def test_tutor_consulta_estudiante_asignado_por_regla_de_alcance(self):
        """Escenario 2: Tutor consulta los datos de un estudiante asignado a su cargo (ADR-005)."""
        dto = self.controlador.consultar_estudiante(
            estudiante_documento="1001234567",
            usuario_id="tutor-101",
            rol="Tutor",
            tutor_documento="T-101",
            ip="192.168.1.60",
        )

        self.assertEqual("1001234567", dto.estudiante_documento)
        self.assertEqual("T-101", dto.tutor_documento)
        self.assertTrue(dto.disponible_sia)

        registros = self.bitacora.listar()
        self.assertEqual(1, len(registros))
        self.assertTrue(registros[0].exitoso)

    def test_tutor_intenta_consultar_estudiante_ajeno_violando_regla_de_alcance(self):
        """Escenario 3: Tutor intenta consultar un estudiante no asignado a su cargo (ADR-005)."""
        with self.assertRaises(PermissionError) as ctx:
            self.controlador.consultar_estudiante(
                estudiante_documento="1001234567",
                usuario_id="tutor-102",
                rol="Tutor",
                tutor_documento="T-102",
                ip="192.168.1.60",
            )

        self.assertIn("Regla de alcance", str(ctx.exception))

        registros = self.bitacora.listar()
        self.assertEqual(1, len(registros))
        self.assertEqual("tutor-102", registros[0].sujeto)
        self.assertFalse(registros[0].exitoso)
        self.assertIn("Regla de alcance", registros[0].detalle)

    def test_tolerancia_a_fallos_cuando_sia_presenta_timeout(self):
        """Escenario 4: SIA no responde dentro del tiempo límite de 10 segundos (EAC-03, RT-03, PA-01)."""
        self.adaptador_sia.simular_timeout(True)

        dto = self.controlador.consultar_estudiante(
            estudiante_documento="1001234567",
            usuario_id="coordinador-01",
            rol="Coordinador de prácticas",
        )

        self.assertEqual("1001234567", dto.estudiante_documento)
        self.assertTrue(dto.tiene_practica_activa)
        self.assertEqual("Ingeniería de Sistemas", dto.programa)
        self.assertFalse(dto.disponible_sia)
        self.assertIsNone(dto.creditos_aprobados)
        self.assertIn("no disponibles temporalmente", dto.mensaje_sia)

        registros = self.bitacora.listar()
        self.assertEqual(1, len(registros))
        self.assertTrue(registros[0].exitoso)

    def test_consulta_estudiante_sin_practica_registrada(self):
        """Escenario 5: Consulta de estudiante sin práctica registrada en el sistema."""
        self.adaptador_sia.configurar_estudiante(
            documento="1009876543",
            creditos_aprobados=110,
            promedio_acumulado=3.9,
            semestre_actual=7,
            matricula_activa=True,
        )

        dto = self.controlador.consultar_estudiante(
            estudiante_documento="1009876543",
            usuario_id="coordinador-01",
            rol="Coordinador de prácticas",
        )

        self.assertEqual("1009876543", dto.estudiante_documento)
        self.assertFalse(dto.tiene_practica_activa)
        self.assertIsNone(dto.practica_id)
        self.assertTrue(dto.disponible_sia)
        self.assertEqual(110, dto.creditos_aprobados)

        registros = self.bitacora.listar()
        self.assertEqual(1, len(registros))
        self.assertTrue(registros[0].exitoso)

    def test_usuario_no_autorizado_es_denegado_y_registrado(self):
        """Escenario 6: Usuario no autorizado intenta consultar datos de estudiante (ADR-005, RN-01)."""
        with self.assertRaises(PermissionError):
            self.controlador.consultar_estudiante(
                estudiante_documento="1001234567",
                usuario_id="estudiante-99",
                rol="Estudiante",
                ip="192.168.1.99",
            )

        registros = self.bitacora.listar()
        self.assertEqual(1, len(registros))
        self.assertEqual("estudiante-99", registros[0].sujeto)
        self.assertFalse(registros[0].exitoso)
        self.assertIn("Acceso denegado", registros[0].detalle)


if __name__ == "__main__":
    unittest.main()
