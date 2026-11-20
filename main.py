from uuid import uuid4

from src.entradas.controlador_estudiante import ControladorEstudiante
from src.entradas.controlador_exportar_acta import ControladorExportarActa
from src.entradas.controlador_tutor import ControladorTutor
from src.modulos.actas.aplicacion.dto import GenerarActaDTO
from src.modulos.actas.aplicacion.exportar_acta_final import ExportarActaFinal
from src.modulos.actas.aplicacion.generar_acta_final import GenerarActaFinal
from src.modulos.actas.dominio.puertos.consulta_practica_acta import DatosPracticaActa
from src.modulos.actas.infraestructura.adaptador_acta_final_memoria import AdaptadorActaFinalMemoria
from src.modulos.actas.infraestructura.adaptador_almacen_archivos_memoria import AdaptadorAlmacenArchivosMemoria
from src.modulos.actas.infraestructura.adaptador_consulta_evaluacion_memoria import AdaptadorConsultaEvaluacionMemoria
from src.modulos.actas.infraestructura.adaptador_consulta_horas_memoria import AdaptadorConsultaHorasMemoria
from src.modulos.actas.infraestructura.adaptador_consulta_practica_memoria import AdaptadorConsultaPracticaMemoria
from src.modulos.actas.infraestructura.adaptador_consulta_reglas_memoria import AdaptadorConsultaReglasMemoria
from src.modulos.actas.infraestructura.adaptador_generador_plantilla_oficial import AdaptadorGeneradorPlantillaOficial
from src.modulos.identidad_accesos.aplicacion.autorizador_accesos import AutorizadorAccesos
from src.modulos.identidad_accesos.dominio.rol import Rol
from src.modulos.identidad_accesos.dominio.usuario_autenticado import UsuarioAutenticado
from src.modulos.identidad_accesos.infraestructura.adaptador_bitacora_memoria import AdaptadorBitacoraMemoria
from src.modulos.practicas.aplicacion.registrar_estudiante import RegistrarEstudiante
from src.modulos.practicas.infraestructura.adaptador_estudiante_memoria import AdaptadorEstudianteMemoria
from src.modulos.tutores_asignacion.aplicacion.registrar_tutor import RegistrarTutor
from src.modulos.tutores_asignacion.infraestructura.adaptador_tutor_memoria import AdaptadorTutorMemoria

IP, AGENTE = "10.0.0.20", "Chrome"
ADMIN = UsuarioAutenticado("A-001", Rol.ADMINISTRADOR)
COORDINADOR = UsuarioAutenticado("C-001", Rol.COORDINADOR)


def probar(descripcion, accion):
    try:
        resultado = accion()
        print(f"  [OK]       {descripcion} -> {resultado}")
    except (ValueError, PermissionError) as error:
        print(f"  [RECHAZO]  {descripcion} -> {error}")


def spec_008_registrar_estudiante(autorizador):
    print("\nSpec 008 - Registrar estudiante (CU-08)")
    controlador = ControladorEstudiante(RegistrarEstudiante(AdaptadorEstudianteMemoria()), autorizador)

    def registrar(usuario, documento="1001234567", nombre="Laura Gómez"):
        return lambda: controlador.registrar_estudiante(
            usuario, documento, nombre, "Ingeniería de Sistemas",
            "laura.gomez@ucaldas.edu.co", IP, AGENTE,
        ).documento

    probar("Administrador registra estudiante", registrar(ADMIN))
    probar("Documento repetido", registrar(ADMIN, nombre="Laura G."))
    probar("Coordinador intenta registrar", registrar(COORDINADOR, documento="1002222222"))
    probar("Nombre vacío", registrar(ADMIN, documento="1003333333", nombre=""))


def spec_009_registrar_tutor(autorizador):
    print("\nSpec 009 - Registrar tutor (CU-09)")
    controlador = ControladorTutor(RegistrarTutor(AdaptadorTutorMemoria()), autorizador)

    def registrar(usuario, documento="T-010", programa="Ingeniería de Sistemas"):
        return lambda: controlador.registrar_tutor(
            usuario, documento, "María López", "maria.lopez@ucaldas.edu.co",
            programa, IP, AGENTE,
        ).documento

    probar("Administrador registra tutor", registrar(ADMIN))
    probar("Documento repetido", registrar(ADMIN))
    probar("Coordinador intenta registrar", registrar(COORDINADOR, documento="T-011"))
    probar("Programa vacío", registrar(ADMIN, documento="T-012", programa=""))


def spec_007_exportar_acta(autorizador):
    print("\nSpec 007 - Exportar acta final (CU-07)")
    practica_id = uuid4()
    consulta_practica = AdaptadorConsultaPracticaMemoria({
        practica_id: DatosPracticaActa(
            practica_id, "v1", "Ingeniería de Sistemas",
            "1001234567", "Laura Gómez", "Tech Solutions S.A.S.",
        )
    })
    actas, almacen = AdaptadorActaFinalMemoria(), AdaptadorAlmacenArchivosMemoria()

    # Se genera un acta con CU-06 para poder exportarla
    acta = GenerarActaFinal(
        actas, almacen, consulta_practica,
        AdaptadorConsultaHorasMemoria({practica_id: 480}),
        AdaptadorConsultaEvaluacionMemoria({practica_id: 4.5}),
        AdaptadorConsultaReglasMemoria({"v1": 480}),
        AdaptadorGeneradorPlantillaOficial(),
    ).ejecutar(GenerarActaDTO(practica_id))

    controlador = ControladorExportarActa(
        ExportarActaFinal(actas, almacen, consulta_practica), autorizador
    )

    def exportar(usuario, practica=practica_id):
        return lambda: controlador.exportar_acta(usuario, practica, IP, AGENTE).nombre_archivo

    probar("Coordinador exporta", exportar(COORDINADOR))
    probar("Estudiante titular exporta", exportar(UsuarioAutenticado("1001234567", Rol.ESTUDIANTE)))
    probar("Estudiante ajeno", exportar(UsuarioAutenticado("1009999999", Rol.ESTUDIANTE)))
    probar("Tutor intenta exportar", exportar(UsuarioAutenticado("T-001", Rol.TUTOR)))
    probar("Práctica sin acta", exportar(COORDINADOR, uuid4()))

    almacen.guardar_archivo(acta.ruta_archivo, b"archivo alterado")
    probar("Archivo alterado", exportar(COORDINADOR))


def main():
    bitacora = AdaptadorBitacoraMemoria()
    autorizador = AutorizadorAccesos(bitacora)

    spec_007_exportar_acta(autorizador)
    spec_008_registrar_estudiante(autorizador)
    spec_009_registrar_tutor(autorizador)

    print(f"\nBitácora: {len(bitacora.listar())} accesos registrados")
    for registro in bitacora.listar():
        estado = "exitoso" if registro.exitoso else "fallido"
        print(f"  {registro.sujeto:<11} {registro.accion:<21} {estado}")


if __name__ == "__main__":
    main()
