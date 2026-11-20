from datetime import date, datetime, timedelta, timezone
import hashlib
import unittest
from uuid import uuid4

from src.entradas.controlador_acceso_externo_evaluacion import (
    ControladorAccesoExternoEvaluacion,
)
from src.modulos.evaluaciones.aplicacion.consultar_evaluacion import (
    ConsultarEvaluacion,
)
from src.modulos.evaluaciones.aplicacion.dto import RegistrarEvaluacionDTO
from src.modulos.evaluaciones.aplicacion.enviar_recordatorio_evaluacion import (
    EnviarRecordatorioEvaluacion,
)
from src.modulos.evaluaciones.aplicacion.registrar_evaluacion import (
    RegistrarEvaluacion,
)
from src.modulos.evaluaciones.infraestructura.adaptador_evaluacion_memoria import (
    AdaptadorEvaluacionMemoria,
)
from src.modulos.evaluaciones.infraestructura.adaptador_servicio_invalidacion_enlace_memoria import (
    AdaptadorServicioInvalidacionEnlaceMemoria,
)
from src.modulos.evaluaciones.infraestructura.adaptador_servicio_practica_evaluacion_memoria import (
    AdaptadorServicioPracticaEvaluacionMemoria,
)
from src.modulos.evaluaciones.infraestructura.adaptador_servicio_recordatorio_memoria import (
    AdaptadorServicioRecordatorioMemoria,
)
from src.modulos.identidad_accesos.aplicacion.gestor_enlaces_acceso import (
    GestorEnlacesAcceso,
)
from src.modulos.identidad_accesos.dominio.enlace_acceso import EnlaceAcceso
from src.modulos.identidad_accesos.dominio.estado_enlace import EstadoEnlace
from src.modulos.identidad_accesos.infraestructura.adaptador_bitacora_memoria import (
    AdaptadorBitacoraMemoria,
)
from src.modulos.identidad_accesos.infraestructura.adaptador_enlace_acceso_memoria import (
    AdaptadorEnlaceAccesoMemoria,
)


class EvaluarEstudianteTests(unittest.TestCase):
    def setUp(self):
        self.practica_id = uuid4()
        self.email_supervisor = "supervisor@empresa.com"
        self.ip_movil = "190.85.12.34"
        self.agente_movil = "Mobile Safari"

        # Repositorios
        self.repo_evaluaciones = AdaptadorEvaluacionMemoria()
        self.repo_enlaces = AdaptadorEnlaceAccesoMemoria()
        self.repo_bitacora = AdaptadorBitacoraMemoria()

        # Adaptadores
        self.gestor_enlaces = GestorEnlacesAcceso(self.repo_enlaces, self.repo_bitacora)
        self.servicio_practica = AdaptadorServicioPracticaEvaluacionMemoria()
        self.servicio_invalidacion = AdaptadorServicioInvalidacionEnlaceMemoria(
            self.gestor_enlaces
        )
        self.servicio_recordatorio = AdaptadorServicioRecordatorioMemoria()

        # Casos de uso
        self.cu_registrar = RegistrarEvaluacion(
            self.repo_evaluaciones, self.servicio_practica, self.servicio_invalidacion
        )
        self.cu_consultar = ConsultarEvaluacion(self.repo_evaluaciones)
        self.cu_recordatorio = EnviarRecordatorioEvaluacion(
            self.repo_evaluaciones, self.servicio_recordatorio
        )

        # Entrada
        self.controlador_externo = ControladorAccesoExternoEvaluacion(
            self.gestor_enlaces, self.cu_registrar
        )

    def test_escenario_1_evaluacion_exitosa_sin_contraseña_invalida_enlace(self):
        token = self.gestor_enlaces.emitir_enlace(
            self.practica_id, self.email_supervisor, acciones_permitidas=["evaluar"]
        )

        resultado = self.controlador_externo.enviar_evaluacion(
            token=token,
            fecha=date(2026, 11, 20),
            calificacion=4.5,
            observaciones="Excelente desempeño técnico y puntualidad",
            ip=self.ip_movil,
            agente_usuario=self.agente_movil,
        )

        self.assertTrue(resultado.exitoso)
        self.assertIsNotNone(resultado.evaluacion_id)

        # Verificar que la evaluación quedó guardada
        evaluacion = self.cu_consultar.ejecutar(self.practica_id)
        self.assertIsNotNone(evaluacion)
        self.assertEqual(4.5, evaluacion.calificacion)
        self.assertEqual("Excelente desempeño técnico y puntualidad", evaluacion.observaciones)

        # Verificar que la práctica fue marcada como evaluada
        self.assertIn(self.practica_id, self.servicio_practica.practicas_evaluadas)

        # Verificar que el enlace fue invalidado a estado USADO (ADR-006)
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        enlace = self.repo_enlaces.buscar_por_hash(token_hash)
        self.assertEqual(EstadoEnlace.USADO, enlace.estado)

        # Verificar que el acceso quedó registrado en la bitácora
        accesos = self.repo_bitacora.listar()
        self.assertTrue(any(a.ip == self.ip_movil and a.exitoso for a in accesos))

    def test_escenario_2_recordatorio_evaluacion_pendiente(self):
        token = self.gestor_enlaces.emitir_enlace(self.practica_id, self.email_supervisor)

        # Envío exitoso cuando está pendiente
        enviado = self.cu_recordatorio.ejecutar(
            self.practica_id, self.email_supervisor, token
        )
        self.assertTrue(enviado)
        self.assertEqual(1, len(self.servicio_recordatorio.recordatorios))
        self.assertEqual(self.email_supervisor, self.servicio_recordatorio.recordatorios[0].email_destinatario)

        # Ya con evaluación, no envía recordatorio
        self.cu_registrar.ejecutar(
            RegistrarEvaluacionDTO(
                token=token,
                practica_id=self.practica_id,
                fecha=date(2026, 11, 20),
                calificacion=4.0,
                observaciones="Bien",
            )
        )
        enviado_despues = self.cu_recordatorio.ejecutar(
            self.practica_id, self.email_supervisor, token
        )
        self.assertFalse(enviado_despues)

    def test_escenario_3_intento_reenvio_con_enlace_ya_usado(self):
        token = self.gestor_enlaces.emitir_enlace(
            self.practica_id, self.email_supervisor, acciones_permitidas=["evaluar"]
        )
        self.controlador_externo.enviar_evaluacion(
            token=token,
            fecha=date(2026, 11, 20),
            calificacion=4.8,
            observaciones="Primera evaluación",
            ip=self.ip_movil,
            agente_usuario=self.agente_movil,
        )

        # Intentar acceder de nuevo con el mismo token
        with self.assertRaises(ValueError) as context:
            self.controlador_externo.enviar_evaluacion(
                token=token,
                fecha=date(2026, 11, 21),
                calificacion=5.0,
                observaciones="Segunda evaluación",
                ip=self.ip_movil,
                agente_usuario=self.agente_movil,
            )
        self.assertIn("enlace no disponible; pida al coordinador que lo reemita", str(context.exception))

        # Intento denegado registrado en bitácora
        accesos = self.repo_bitacora.listar()
        denegados = [a for a in accesos if not a.exitoso and a.ip == self.ip_movil]
        self.assertGreaterEqual(len(denegados), 1)

    def test_escenario_4_acceso_enlace_vencido_denegado(self):
        token_vencido = "token_evaluacion_vencido"
        hash_vencido = hashlib.sha256(token_vencido.encode("utf-8")).hexdigest()
        enlace_vencido = EnlaceAcceso(
            token_hash=hash_vencido,
            practica_id=self.practica_id,
            email_destinatario=self.email_supervisor,
            fecha_vencimiento=datetime.now(timezone.utc) - timedelta(days=2),
            estado=EstadoEnlace.VIGENTE,
            acciones_permitidas=["evaluar"],
        )
        self.repo_enlaces.guardar(enlace_vencido)

        with self.assertRaises(ValueError) as context:
            self.controlador_externo.enviar_evaluacion(
                token=token_vencido,
                fecha=date(2026, 11, 20),
                calificacion=3.5,
                observaciones="Tardía",
                ip=self.ip_movil,
                agente_usuario=self.agente_movil,
            )
        self.assertIn("enlace no disponible; pida al coordinador que lo reemita", str(context.exception))

        # Registro en bitácora verificado
        accesos = self.repo_bitacora.listar()
        self.assertTrue(any(not a.exitoso and "vencido" in a.detalle.lower() for a in accesos))

    def test_escenario_5_rechazo_segunda_evaluacion_misma_practica(self):
        token1 = self.gestor_enlaces.emitir_enlace(
            self.practica_id, self.email_supervisor, acciones_permitidas=["evaluar"]
        )
        token2 = self.gestor_enlaces.emitir_enlace(
            self.practica_id, "otro@empresa.com", acciones_permitidas=["evaluar"]
        )

        self.cu_registrar.ejecutar(
            RegistrarEvaluacionDTO(
                token=token1,
                practica_id=self.practica_id,
                fecha=date(2026, 11, 20),
                calificacion=4.0,
                observaciones="Evaluación 1",
            )
        )

        with self.assertRaises(ValueError) as context:
            self.cu_registrar.ejecutar(
                RegistrarEvaluacionDTO(
                    token=token2,
                    practica_id=self.practica_id,
                    fecha=date(2026, 11, 20),
                    calificacion=4.5,
                    observaciones="Evaluación duplicada",
                )
            )
        self.assertIn("solo se permite una evaluación por práctica", str(context.exception))


if __name__ == "__main__":
    unittest.main()
