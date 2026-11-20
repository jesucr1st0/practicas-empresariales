# Validación: 002-registrar-practica (CU-02 Registrar práctica)

## 1. Validación por escenario

| Escenario | Cumple | Evidencia |
|-----------|:------:|-----------|
| **1. Registro exitoso fijando la regla vigente del programa** | **Sí** | `RegistrarPractica.ejecutar()` resuelve la regla vigente (v1, 480 horas) y almacena la práctica en estado `registrada` asociando la versión de regla. |
| **2. Registro a partir de una postulación verificada** | **Sí** | `RegistrarPractica.ejecutar()` valida mediante `ServicioConsultaPostulacion` que la postulación esté verificada y guarda la práctica asociando `postulacion_id`. |
| **3. Intento de registro con postulación no verificada** | **Sí** | Se lanza `PostulacionNoVerificadaError` y no se persiste ninguna práctica. |
| **4. Programa sin versión de regla vigente configurada** | **Sí** | Se lanza `ReglaNoConfiguradaError` al no encontrar regla vigente para el programa en la fecha, bloqueando el registro. |
| **5. Inmutabilidad de la regla en prácticas registradas ante cambios futuros (EAC-01)** | **Sí** | Al registrarse la regla `v2` (540 horas), la práctica previa mantiene fija su regla `v1` (480 horas). Las nuevas prácticas creadas bajo la nueva vigencia adoptan `v2`. Se verificó que 0 prácticas en curso fueron alteradas. |

## 2. Revisión de la regla de dependencia

Verificación estática ejecutada con script de validación arquitectónica:

- [x] `dominio/` no importa nada de `aplicacion/` ni de `infraestructura/` (0 violaciones encontradas en `src/modulos/reglas/dominio/` y `src/modulos/practicas/dominio/`).
- [x] Los puertos están declarados en `dominio/puertos/` (`ReglaRepository`, `PracticaRepository`, `ServicioConsultaReglas`, `ServicioConsultaPostulacion`).
- [x] Los adaptadores están implementados en `infraestructura/` (`AdaptadorReglaMemoria`, `AdaptadorPracticaMemoria`, `AdaptadorServicioReglas`, `AdaptadorServicioPostulacionSimulado`).

## 3. Revisión de trazabilidad

- [x] Cada tarea de `tasks.md` está marcada `[x]` (T-01 a T-13 completadas).
- [x] Cada escenario de `spec.md` aparece cubierto y probado en las tareas y el ejecutor.
- [x] Los nombres del código coinciden fielmente con el glosario de `docs/arquitectura.md §10` (`Practica`, `ReglaPrograma`, `EstadoPractica`, `horas_minimas`).
