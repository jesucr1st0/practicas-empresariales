import unittest

from src.entradas.controlador_empresa import ControladorEmpresa
from src.modulos.identidad_accesos.infraestructura.adaptador_bitacora_memoria import (
    AdaptadorBitacoraMemoria,
)
from src.modulos.practicas.aplicacion.consultar_empresa import ConsultarEmpresa
from src.modulos.practicas.aplicacion.dto_empresa import (
    RegistrarEmpresaDTO,
    SupervisorDTO,
)
from src.modulos.practicas.aplicacion.registrar_empresa import RegistrarEmpresa
from src.modulos.practicas.infraestructura.adaptador_empresa_memoria import (
    AdaptadorEmpresaMemoria,
)


class RegistrarEmpresaTests(unittest.TestCase):
    def setUp(self):
        self.repo_empresa = AdaptadorEmpresaMemoria()
        self.bitacora = AdaptadorBitacoraMemoria()

        self.cu_registrar = RegistrarEmpresa(self.repo_empresa)
        self.cu_consultar = ConsultarEmpresa(self.repo_empresa)

        self.controlador = ControladorEmpresa(
            caso_uso_registrar=self.cu_registrar,
            caso_uso_consultar=self.cu_consultar,
            registrar_acceso=self.bitacora,
        )

        self.dto_valido = RegistrarEmpresaDTO(
            nit="900123456-1",
            razon_social="Tech Solutions S.A.S.",
            sector="Tecnología",
            ciudad="Manizales",
            supervisores=(
                SupervisorDTO(
                    nombre="Carlos Pérez",
                    correo="carlos.perez@techsolutions.com",
                    telefono="3001234567",
                ),
            ),
        )

    def test_registro_exitoso_empresa_con_supervisor_inicial(self):
        """Escenario 1: Registro exitoso de empresa con supervisor inicial (flujo básico)."""
        resultado = self.controlador.registrar_empresa(
            dto=self.dto_valido,
            usuario_id="coordinador-01",
            rol="Coordinador de prácticas",
            ip="192.168.1.50",
            agente_usuario="Mozilla/5.0",
        )

        self.assertEqual("900123456-1", resultado.nit)
        self.assertEqual("Tech Solutions S.A.S.", resultado.razon_social)
        self.assertTrue(resultado.activa)
        self.assertEqual(1, resultado.supervisores_registrados)

        # Verificar persistencia en repositorio
        empresa = self.repo_empresa.obtener_empresa_por_nit("900123456-1")
        self.assertIsNotNone(empresa)
        supervisores = self.repo_empresa.obtener_supervisores_por_empresa("900123456-1")
        self.assertEqual(1, len(supervisores))
        self.assertEqual("Carlos Pérez", supervisores[0].nombre)

        # Verificar bitácora de auditoría (ADR-005, RN-01)
        registros = self.bitacora.listar()
        self.assertEqual(1, len(registros))
        self.assertEqual("coordinador-01", registros[0].sujeto)
        self.assertEqual("CU-10: registrar empresa", registros[0].accion)
        self.assertEqual("192.168.1.50", registros[0].ip)
        self.assertTrue(registros[0].exitoso)

    def test_intento_registro_con_nit_duplicado(self):
        """Escenario 2: Intento de registro con NIT duplicado."""
        self.controlador.registrar_empresa(
            dto=self.dto_valido,
            usuario_id="coordinador-01",
            rol="Coordinador de prácticas",
        )

        dto_duplicado = RegistrarEmpresaDTO(
            nit="900123456-1",
            razon_social="Tech Solutions Otra S.A.S.",
            sector="Servicios",
            ciudad="Pereira",
            supervisores=(
                SupervisorDTO(
                    nombre="Ana López",
                    correo="ana@techsolutions.com",
                ),
            ),
        )

        with self.assertRaises(ValueError) as ctx:
            self.controlador.registrar_empresa(
                dto=dto_duplicado,
                usuario_id="coordinador-01",
                rol="Coordinador de prácticas",
            )

        self.assertIn("Ya existe una empresa registrada con el NIT '900123456-1'", str(ctx.exception))

        registros = self.bitacora.listar()
        self.assertEqual(2, len(registros))
        self.assertFalse(registros[1].exitoso)

    def test_intento_registro_sin_supervisor_inicial(self):
        """Escenario 3: Intento de registrar empresa sin supervisor inicial."""
        dto_sin_supervisor = RegistrarEmpresaDTO(
            nit="900987654-3",
            razon_social="Innovar Ltda.",
            sector="Consultoría",
            ciudad="Manizales",
            supervisores=(),
        )

        with self.assertRaises(ValueError) as ctx:
            self.controlador.registrar_empresa(
                dto=dto_sin_supervisor,
                usuario_id="coordinador-01",
                rol="Coordinador de prácticas",
            )

        self.assertIn("al menos un supervisor", str(ctx.exception))

        empresa = self.repo_empresa.obtener_empresa_por_nit("900987654-3")
        self.assertIsNone(empresa)

        registros = self.bitacora.listar()
        self.assertEqual(1, len(registros))
        self.assertFalse(registros[0].exitoso)

    def test_usuario_no_autorizado_es_denegado_y_registrado(self):
        """Escenario 4: Usuario no autorizado intenta registrar una empresa (ADR-005, RN-01)."""
        with self.assertRaises(PermissionError):
            self.controlador.registrar_empresa(
                dto=self.dto_valido,
                usuario_id="estudiante-12",
                rol="Estudiante",
                ip="192.168.1.88",
            )

        registros = self.bitacora.listar()
        self.assertEqual(1, len(registros))
        self.assertEqual("estudiante-12", registros[0].sujeto)
        self.assertFalse(registros[0].exitoso)
        self.assertIn("Acceso denegado", registros[0].detalle)

    def test_consulta_empresa_registrada_por_nit(self):
        """Escenario 5: Consulta de empresa registrada por NIT."""
        self.controlador.registrar_empresa(
            dto=self.dto_valido,
            usuario_id="coordinador-01",
            rol="Coordinador de prácticas",
        )

        detalle = self.controlador.consultar_por_nit(
            nit="900123456-1",
            usuario_id="coordinador-01",
            rol="Coordinador de prácticas",
            ip="192.168.1.50",
        )

        self.assertEqual("900123456-1", detalle.nit)
        self.assertEqual("Tech Solutions S.A.S.", detalle.razon_social)
        self.assertEqual("Tecnología", detalle.sector)
        self.assertEqual("Manizales", detalle.ciudad)
        self.assertTrue(detalle.activa)
        self.assertEqual(1, len(detalle.supervisores))
        self.assertEqual("Carlos Pérez", detalle.supervisores[0].nombre)
        self.assertEqual("carlos.perez@techsolutions.com", detalle.supervisores[0].correo)

        registros = self.bitacora.listar()
        self.assertEqual(2, len(registros))
        self.assertEqual("CU-10: consultar empresa", registros[1].accion)
        self.assertTrue(registros[1].exitoso)


if __name__ == "__main__":
    unittest.main()
