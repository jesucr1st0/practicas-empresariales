import unittest
from dataclasses import fields

from src.entradas.controlador_tutor import ControladorTutor
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
from src.modulos.tutores_asignacion.aplicacion.registrar_tutor import RegistrarTutor
from src.modulos.tutores_asignacion.dominio.tutor import Tutor
from src.modulos.tutores_asignacion.infraestructura.adaptador_tutor_memoria import (
    AdaptadorTutorMemoria,
)

IP = "10.0.0.20"
AGENTE = "Chrome"
DATOS = {
    "documento": "T-010",
    "nombre": "María López",
    "correo": "maria.lopez@ucaldas.edu.co",
    "programa": "Ingeniería de Sistemas",
}


class RegistrarTutorTests(unittest.TestCase):
    def setUp(self):
        self.tutores = AdaptadorTutorMemoria()
        self.bitacora = AdaptadorBitacoraMemoria()
        self.controlador = ControladorTutor(
            RegistrarTutor(self.tutores),
            AutorizadorAccesos(self.bitacora),
        )
        self.administrador = UsuarioAutenticado("A-001", Rol.ADMINISTRADOR)

    def _registrar(self, usuario=None, **cambios):
        datos = {**DATOS, **cambios}
        return self.controlador.registrar_tutor(
            usuario or self.administrador, ip=IP, agente_usuario=AGENTE, **datos
        )

    def test_escenario_1_registro_exitoso(self):
        resultado = self._registrar()

        self.assertEqual("T-010", resultado.documento)
        self.assertTrue(resultado.activo)
        guardado = self.tutores.obtener_por_documento("T-010")
        self.assertEqual(
            Tutor(
                "T-010",
                "María López",
                "maria.lopez@ucaldas.edu.co",
                "Ingeniería de Sistemas",
                True,
            ),
            guardado,
        )

        registro = self.bitacora.listar()[-1]
        self.assertTrue(registro.exitoso)
        self.assertEqual("A-001", registro.sujeto)
        self.assertEqual("registrar_tutor", registro.accion)
        self.assertEqual(IP, registro.ip)
        self.assertEqual(AGENTE, registro.agente_usuario)

    def test_escenario_2_sin_contrasena(self):
        self._registrar()

        atributos = {campo.name for campo in fields(Tutor)}
        self.assertEqual({"documento", "nombre", "correo", "programa", "activo"}, atributos)

    def test_escenario_3_documento_repetido_es_rechazado(self):
        self._registrar()

        with self.assertRaisesRegex(ValueError, "Ya existe un tutor"):
            self._registrar(nombre="M. López")

        self.assertEqual("María López", self.tutores.obtener_por_documento("T-010").nombre)
        self.assertFalse(self.bitacora.listar()[-1].exitoso)

    def test_escenario_4_rol_no_autorizado(self):
        coordinador = UsuarioAutenticado("C-001", Rol.COORDINADOR)

        with self.assertRaisesRegex(PermissionError, "Coordinador"):
            self._registrar(usuario=coordinador)

        self.assertIsNone(self.tutores.obtener_por_documento("T-010"))
        registro = self.bitacora.listar()[-1]
        self.assertFalse(registro.exitoso)
        self.assertEqual("C-001", registro.sujeto)

    def test_escenario_5_datos_incompletos(self):
        with self.assertRaisesRegex(ValueError, "programa"):
            self._registrar(programa="")

        self.assertIsNone(self.tutores.obtener_por_documento("T-010"))
        self.assertFalse(self.bitacora.listar()[-1].exitoso)


if __name__ == "__main__":
    unittest.main()
