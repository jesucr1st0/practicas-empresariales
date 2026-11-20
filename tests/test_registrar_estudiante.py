import unittest
from dataclasses import fields

from src.entradas.controlador_estudiante import ControladorEstudiante
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
from src.modulos.practicas.aplicacion.registrar_estudiante import RegistrarEstudiante
from src.modulos.practicas.dominio.estudiante import Estudiante
from src.modulos.practicas.infraestructura.adaptador_estudiante_memoria import (
    AdaptadorEstudianteMemoria,
)

IP = "10.0.0.20"
AGENTE = "Chrome"
DATOS = {
    "documento": "1001234567",
    "nombre": "Laura Gómez",
    "programa": "Ingeniería de Sistemas",
    "correo": "laura.gomez@ucaldas.edu.co",
}


class RegistrarEstudianteTests(unittest.TestCase):
    def setUp(self):
        self.estudiantes = AdaptadorEstudianteMemoria()
        self.bitacora = AdaptadorBitacoraMemoria()
        self.controlador = ControladorEstudiante(
            RegistrarEstudiante(self.estudiantes),
            AutorizadorAccesos(self.bitacora),
        )
        self.administrador = UsuarioAutenticado("A-001", Rol.ADMINISTRADOR)

    def _registrar(self, usuario=None, **cambios):
        datos = {**DATOS, **cambios}
        return self.controlador.registrar_estudiante(
            usuario or self.administrador, ip=IP, agente_usuario=AGENTE, **datos
        )

    def test_escenario_1_registro_exitoso(self):
        resultado = self._registrar()

        self.assertEqual("1001234567", resultado.documento)
        guardado = self.estudiantes.obtener_por_documento("1001234567")
        self.assertEqual("Laura Gómez", guardado.nombre)
        self.assertEqual("Ingeniería de Sistemas", guardado.programa)
        self.assertEqual("laura.gomez@ucaldas.edu.co", guardado.correo)

        registro = self.bitacora.listar()[-1]
        self.assertTrue(registro.exitoso)
        self.assertEqual("A-001", registro.sujeto)
        self.assertEqual("registrar_estudiante", registro.accion)
        self.assertEqual(IP, registro.ip)
        self.assertEqual(AGENTE, registro.agente_usuario)

    def test_escenario_2_sin_contrasena_ni_datos_academicos(self):
        self._registrar()

        atributos = {campo.name for campo in fields(Estudiante)}
        self.assertEqual({"documento", "nombre", "programa", "correo"}, atributos)

    def test_escenario_3_documento_repetido_es_rechazado(self):
        self._registrar()

        with self.assertRaisesRegex(ValueError, "Ya existe un estudiante"):
            self._registrar(nombre="Laura G.")

        self.assertEqual(
            "Laura Gómez", self.estudiantes.obtener_por_documento("1001234567").nombre
        )
        self.assertFalse(self.bitacora.listar()[-1].exitoso)

    def test_escenario_4_rol_no_autorizado(self):
        coordinador = UsuarioAutenticado("C-001", Rol.COORDINADOR)

        with self.assertRaisesRegex(PermissionError, "Coordinador"):
            self._registrar(usuario=coordinador)

        self.assertIsNone(self.estudiantes.obtener_por_documento("1001234567"))
        registro = self.bitacora.listar()[-1]
        self.assertFalse(registro.exitoso)
        self.assertEqual("C-001", registro.sujeto)

    def test_escenario_5_datos_incompletos(self):
        with self.assertRaisesRegex(ValueError, "nombre"):
            self._registrar(nombre="")

        self.assertIsNone(self.estudiantes.obtener_por_documento("1001234567"))
        self.assertFalse(self.bitacora.listar()[-1].exitoso)


if __name__ == "__main__":
    unittest.main()
