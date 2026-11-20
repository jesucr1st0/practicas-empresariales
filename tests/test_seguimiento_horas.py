from datetime import date, datetime, timedelta, timezone
import hashlib
import unittest
from uuid import UUID, uuid4

from src.entradas.controlador_acceso_externo_horas import ControladorAccesoExternoHoras
from src.entradas.controlador_horas_interno import ControladorHorasInterno
from src.modulos.horas.aplicacion.consultar_horas_supervisor import ConsultarHorasSupervisor
from src.modulos.horas.aplicacion.consultar_horas_tutor import ConsultarHorasTutor
from src.modulos.horas.aplicacion.dto import RegistrarHorasDTO
from src.modulos.horas.aplicacion.registrar_horas import RegistrarHoras
from src.modulos.horas.aplicacion.solicitar_validacion_supervisor import SolicitarValidacionSupervisor
from src.modulos.horas.aplicacion.validar_horas_supervisor import ValidarHorasSupervisor
from src.modulos.horas.dominio.estado_validacion_horas import EstadoValidacionHoras
from src.modulos.horas.dominio.registro_horas import RegistroHoras
from src.modulos.horas.infraestructura.adaptador_consulta_asignacion_memoria import (
    AdaptadorConsultaAsignacionMemoria,
)
from src.modulos.horas.infraestructura.adaptador_registro_horas_memoria import (
    AdaptadorRegistroHorasMemoria,
)
from src.modulos.horas.infraestructura.adaptador_servicio_enlace_memoria import (
    AdaptadorServicioEnlaceMemoria,
)
from src.modulos.horas.infraestructura.adaptador_servicio_notificacion_memoria import (
    AdaptadorServicioNotificacionMemoria,
)
from src.modulos.identidad_accesos.aplicacion.gestor_enlaces_acceso import GestorEnlacesAcceso
from src.modulos.identidad_accesos.dominio.enlace_acceso import EnlaceAcceso
from src.modulos.identidad_accesos.dominio.estado_enlace import EstadoEnlace
from src.modulos.identidad_accesos.infraestructura.adaptador_bitacora_memoria import (
    AdaptadorBitacoraMemoria,
)
from src.modulos.identidad_accesos.infraestructura.adaptador_enlace_acceso_memoria import (
    AdaptadorEnlaceAccesoMemoria,
)


class SeguimientoHorasTests(unittest.TestCase):
    def setUp(self):
        self.practica_id = uuid4()
        self.estudiante_documento = "1001234567"
        self.tutor_documento = "T-001"
        self.tutor_ajeno = "T-002"

        # Repositorios
        self.repo_horas = AdaptadorRegistroHorasMemoria()
        self.repo_enlaces = AdaptadorEnlaceAccesoMemoria()
        self.repo_bitacora = AdaptadorBitacoraMemoria()
        self.consulta_asignacion = AdaptadorConsultaAsignacionMemoria()
        self.consulta_asignacion.asignar(self.tutor_documento, self.practica_id)

        # Servicios y adaptadores
        self.gestor_enlaces = GestorEnlacesAcceso(self.repo_enlaces, self.repo_bitacora)
        self.servicio_enlace = AdaptadorServicioEnlaceMemoria(self.gestor_enlaces)
        self.servicio_notificacion = AdaptadorServicioNotificacionMemoria()

        # Casos de uso
        self.cu_registrar_horas = RegistrarHoras(self.repo_horas)
        self.cu_consultar_tutor = ConsultarHorasTutor(
            self.repo_horas, self.consulta_asignacion, self.repo_bitacora
        )
        self.cu_solicitar_supervisor = SolicitarValidacionSupervisor(
            self.servicio_enlace, self.servicio_notificacion
        )
        self.cu_consultar_supervisor = ConsultarHorasSupervisor(self.repo_horas)
        self.cu_validar_supervisor = ValidarHorasSupervisor(self.repo_horas)

        # Controladores de entrada
        self.controlador_interno = ControladorHorasInterno(
            self.cu_registrar_horas, self.cu_consultar_tutor
        )
        self.controlador_externo = ControladorAccesoExternoHoras(
            self.gestor_enlaces, self.cu_consultar_supervisor, self.cu_validar_supervisor
        )

    def test_escenario_1_registro_horas_estudiante_exitoso(self):
        dto = RegistrarHorasDTO(
            practica_id=self.practica_id,
            estudiante_documento=self.estudiante_documento,
            fecha=date(2026, 11, 20),
            cantidad_horas=40,
            evidencia="informe_semanal_1.pdf",
        )
        resultado = self.controlador_interno.registrar_horas(dto)

        self.assertEqual(40, resultado.cantidad_horas)
        self.assertEqual("pendiente", resultado.estado_validacion)
        self.assertEqual(self.practica_id, resultado.practica_id)

        guardado = self.repo_horas.buscar_por_id(resultado.id)
        self.assertIsNotNone(guardado)
        self.assertEqual(EstadoValidacionHoras.PENDIENTE, guardado.estado_validacion)

    def test_escenario_2_consulta_horas_tutor_asignado(self):
        # Crear 40 horas validadas y 20 pendientes
        r1 = RegistroHoras(
            practica_id=self.practica_id,
            estudiante_documento=self.estudiante_documento,
            fecha=date(2026, 11, 10),
            cantidad_horas=40,
            evidencia="informe_semana_1.pdf",
            estado_validacion=EstadoValidacionHoras.VALIDADO_SUPERVISOR,
        )
        r2 = RegistroHoras(
            practica_id=self.practica_id,
            estudiante_documento=self.estudiante_documento,
            fecha=date(2026, 11, 17),
            cantidad_horas=20,
            evidencia="informe_semana_2.pdf",
            estado_validacion=EstadoValidacionHoras.PENDIENTE,
        )
        self.repo_horas.guardar(r1)
        self.repo_horas.guardar(r2)

        resumen = self.controlador_interno.consultar_horas_tutor(
            tutor_documento=self.tutor_documento,
            practica_id=self.practica_id,
        )

        self.assertEqual(60, resumen.total_horas)
        self.assertEqual(40, resumen.horas_validadas)
        self.assertEqual(20, resumen.horas_pendientes)
        self.assertEqual(2, len(resumen.registros))

        # Verificar que el acceso quedó en la bitácora
        accesos = self.repo_bitacora.listar()
        self.assertTrue(any(a.sujeto == self.tutor_documento and a.exitoso for a in accesos))

    def test_escenario_3_tutor_no_asignado_denegado(self):
        with self.assertRaises(PermissionError) as context:
            self.controlador_interno.consultar_horas_tutor(
                tutor_documento=self.tutor_ajeno,
                practica_id=self.practica_id,
                ip="192.168.1.50",
                agente_usuario="Navegador Docente",
            )
        self.assertIn("alcance asignado", str(context.exception))

        # Verificar que el intento no autorizado quedó en la bitácora (ADR-005)
        accesos = self.repo_bitacora.listar()
        denegados = [a for a in accesos if a.sujeto == self.tutor_ajeno and not a.exitoso]
        self.assertEqual(1, len(denegados))
        self.assertEqual("192.168.1.50", denegados[0].ip)

    def test_escenario_4_emision_y_envio_enlace_supervisor(self):
        email_supervisor = "supervisor@empresa.com"
        token = self.cu_solicitar_supervisor.ejecutar(self.practica_id, email_supervisor)

        # Token seguro no vacío
        self.assertTrue(len(token) >= 20)

        # En la BD se guardó SOLO el hash criptográfico (ADR-006)
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        enlace_guardado = self.repo_enlaces.buscar_por_hash(token_hash)
        self.assertIsNotNone(enlace_guardado)
        self.assertEqual(self.practica_id, enlace_guardado.practica_id)
        self.assertEqual(EstadoEnlace.VIGENTE, enlace_guardado.estado)

        # Vigencia fijada a 30 días
        delta_dias = (enlace_guardado.fecha_vencimiento - enlace_guardado.fecha_emision).days
        self.assertEqual(30, delta_dias)

        # Se envió correo de notificación
        self.assertEqual(1, len(self.servicio_notificacion.notificaciones))
        notif = self.servicio_notificacion.notificaciones[0]
        self.assertEqual(email_supervisor, notif.email_destinatario)
        self.assertIn(token, notif.enlace)

    def test_escenario_5_validacion_supervisor_sin_cuenta(self):
        # Crear horas pendientes
        registro = RegistroHoras(
            practica_id=self.practica_id,
            estudiante_documento=self.estudiante_documento,
            fecha=date(2026, 11, 20),
            cantidad_horas=40,
            evidencia="informe_final.pdf",
        )
        self.repo_horas.guardar(registro)

        # Emitir enlace vigente
        token = self.gestor_enlaces.emitir_enlace(self.practica_id, "supervisor@empresa.com")

        # Supervisor consulta horas sin contraseña desde celular 4G (EAC-02)
        ip_movil = "190.85.12.34"
        agente_movil = "Mobile Safari"
        horas_pendientes = self.controlador_externo.consultar_horas_pendientes(
            token=token, ip=ip_movil, agente_usuario=agente_movil
        )
        self.assertEqual(1, len(horas_pendientes))
        self.assertEqual(40, horas_pendientes[0].cantidad_horas)

        # Supervisor valida las horas
        resultado = self.controlador_externo.validar_horas(
            token=token, ip=ip_movil, agente_usuario=agente_movil
        )
        self.assertTrue(resultado.exitoso)
        self.assertEqual(40, resultado.horas_validadas)

        # El registro queda en estado validado
        actualizado = self.repo_horas.buscar_por_id(registro.id)
        self.assertEqual(EstadoValidacionHoras.VALIDADO_SUPERVISOR, actualizado.estado_validacion)

        # El 100 % de accesos quedó registrado en la bitácora
        accesos = self.repo_bitacora.listar()
        accesos_supervisor = [a for a in accesos if a.ip == ip_movil]
        self.assertGreaterEqual(len(accesos_supervisor), 2)
        for a in accesos_supervisor:
            self.assertEqual(agente_movil, a.agente_usuario)
            self.assertTrue(a.exitoso)

    def test_escenario_6_enlace_vencido_usado_o_revocado_denegado(self):
        token_vencido = "token_de_prueba_vencido"
        hash_vencido = hashlib.sha256(token_vencido.encode("utf-8")).hexdigest()
        enlace_vencido = EnlaceAcceso(
            token_hash=hash_vencido,
            practica_id=self.practica_id,
            email_destinatario="supervisor@empresa.com",
            fecha_vencimiento=datetime.now(timezone.utc) - timedelta(days=1),
            estado=EstadoEnlace.VIGENTE,
        )
        self.repo_enlaces.guardar(enlace_vencido)

        ip_externa = "190.85.12.34"
        agente_externo = "Mobile Safari"

        with self.assertRaises(ValueError) as context:
            self.controlador_externo.consultar_horas_pendientes(
                token=token_vencido, ip=ip_externa, agente_usuario=agente_externo
            )
        self.assertIn("enlace no disponible; pida al coordinador que lo reemita", str(context.exception))

        # Intento denegado registrado en bitácora
        accesos = self.repo_bitacora.listar()
        denegados = [a for a in accesos if not a.exitoso and a.ip == ip_externa]
        self.assertGreaterEqual(len(denegados), 1)

        # Probar con enlace en estado REVOCADO
        token_revocado = "token_de_prueba_revocado"
        hash_revocado = hashlib.sha256(token_revocado.encode("utf-8")).hexdigest()
        enlace_revocado = EnlaceAcceso(
            token_hash=hash_revocado,
            practica_id=self.practica_id,
            email_destinatario="supervisor@empresa.com",
            fecha_vencimiento=datetime.now(timezone.utc) + timedelta(days=10),
            estado=EstadoEnlace.REVOCADO,
        )
        self.repo_enlaces.guardar(enlace_revocado)

        with self.assertRaises(ValueError) as context_revocado:
            self.controlador_externo.validar_horas(
                token=token_revocado, ip=ip_externa, agente_usuario=agente_externo
            )
        self.assertIn("enlace no disponible; pida al coordinador que lo reemita", str(context_revocado.exception))


if __name__ == "__main__":
    unittest.main()
