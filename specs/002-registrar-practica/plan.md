# Plan: 002-registrar-practica (CU-02 Registrar práctica)

## 1. Decisiones que aplican

| ADR | Decisión | Impacto en esta funcionalidad |
|-----|----------|-------------------------------|
| [ADR-009](../../docs/adr/ADR-009-reglas-versionadas-por-programa.md) | Reglas versionadas e inmutables por programa | La práctica almacena una referencia fija a la `ReglaPrograma` vigente al momento de su registro. Cambios posteriores en las reglas no alteran prácticas existentes (EAC-01). |
| [ADR-001](../../docs/adr/ADR-001-monolito-modular.md) | Monolito modular con Clean Architecture | El `Módulo Prácticas` consume al `Módulo Reglas` mediante interfaces/puertos desacoplados sin dependencia circular ni acceso directo a tablas ajenas. |
| [ADR-002](../../docs/adr/ADR-002-persistencia-relacional.md) | Persistencia relacional (adaptadores en memoria en esta etapa) | Repositorios aislados por módulo implementados en memoria. |

## 2. Componentes por capa

Basado en la [vista de desarrollo](../../docs/vistas/03-desarrollo.md):

### Módulo Reglas (`src/modulos/reglas/`)

#### Dominio
- `src/modulos/reglas/dominio/regla_programa.py`: Entidad `ReglaPrograma`: `id`, `programa`, `version`, `vigencia_desde`, `horas_minimas`, `capacidad_maxima_tutor`.
- `src/modulos/reglas/dominio/puertos/regla_repository.py`: Puerto `ReglaRepository`: guardar regla, buscar por programa y fecha de vigencia, buscar por id.

#### Aplicación
- `src/modulos/reglas/aplicacion/resolver_regla_vigente.py`: Caso de uso `ResolverReglaVigente`: dada una fecha y un programa, busca la versión de regla cuya `vigencia_desde <= fecha` sea la más reciente.

#### Infraestructura
- `src/modulos/reglas/infraestructura/adaptador_regla_memoria.py`: Adaptador `AdaptadorReglaMemoria` implementando `ReglaRepository`.

---

### Módulo Prácticas (`src/modulos/practicas/`)

#### Dominio
- `src/modulos/practicas/dominio/estado_practica.py`: Enum `EstadoPractica`: `REGISTRADA`, `EN_CURSO`, `FINALIZADA`, `CERRADA`.
- `src/modulos/practicas/dominio/practica.py`: Entidad `Practica`: `id`, `estudiante_documento`, `programa`, `empresa_id`, `supervisor_id`, `periodo`, `fecha_inicio`, `fecha_fin`, `estado`, `regla_id`, `horas_minimas_exigidas`, `postulacion_id`, `tutor_documento`.
- `src/modulos/practicas/dominio/puertos/practica_repository.py`: Puerto `PracticaRepository`: guardar, buscar por ID, buscar activa por estudiante.
- `src/modulos/practicas/dominio/puertos/servicio_consulta_postulacion.py`: Puerto `ServicioConsultaPostulacion`: verifica si una postulación existe y está en estado `VERIFICADA`.
- `src/modulos/practicas/dominio/puertos/servicio_consulta_reglas.py`: Puerto `ServicioConsultaReglas`: invoca la resolución de regla vigente para programa y fecha.

#### Aplicación
- `src/modulos/practicas/aplicacion/dto.py`: `RegistrarPracticaDTO`, `ResultadoPracticaDTO`.
- `src/modulos/practicas/aplicacion/registrar_practica.py`: Caso de uso `RegistrarPractica`:
  1. Si se envía `postulacion_id`, valida con `ServicioConsultaPostulacion` que esté verificada.
  2. Valida que el estudiante no tenga ya una práctica activa (`REGISTRADA` o `EN_CURSO`).
  3. Consulta la versión de regla vigente con `ServicioConsultaReglas`. Si no existe, falla con error de configuración de regla.
  4. Crea la entidad `Practica` asociando la regla encontrada (inmutable).
  5. Guarda en `PracticaRepository` y retorna `ResultadoPracticaDTO`.

#### Infraestructura
- `src/modulos/practicas/infraestructura/adaptador_practica_memoria.py`: Adaptador `AdaptadorPracticaMemoria` implementando `PracticaRepository`.
- `src/modulos/practicas/infraestructura/adaptador_servicio_reglas.py`: Adaptador `AdaptadorServicioReglas` que delega en el caso de uso `ResolverReglaVigente`.
- `src/modulos/practicas/infraestructura/adaptador_servicio_postulacion_simulado.py`: Adaptador `AdaptadorServicioPostulacionSimulado` implementando `ServicioConsultaPostulacion`.

---

### Entradas (`src/entradas/`)
- `src/entradas/controlador_practica.py`: Punto de entrada `ControladorPractica` para registrar y consultar prácticas.

## 3. Flujo de ejecución

1. Se recibe solicitud de registro de práctica.
2. Si incluye `postulacion_id`, se consulta `ServicioConsultaPostulacion`: si no está verificada, se lanza excepción `PostulacionNoVerificadaError`.
3. Se invoca `ServicioConsultaReglas(programa, fecha_registro)`:
   - Si no hay regla vigente para la fecha y programa, se lanza excepción `ReglaNoConfiguradaError`.
4. Se crea la entidad `Practica` con estado `EstadoPractica.REGISTRADA` y la referencia fija a `regla.id` y `regla.horas_minimas`.
5. Se almacena en `PracticaRepository`.

## 4. Modelo de datos

```
Practica
├── id: UUID
├── estudiante_documento: str
├── programa: str
├── empresa_id: str
├── supervisor_id: str
├── periodo: str
├── fecha_inicio: date
├── fecha_fin: date
├── estado: EstadoPractica (REGISTRADA)
├── regla_id: UUID
├── regla_version: str
├── horas_minimas_exigidas: int
├── postulacion_id: UUID | None
└── tutor_documento: str | None
```

## 5. Fuera de alcance

- Asignación inmediata de tutores (corresponde a CU-01).
- Registro de horas de práctica (corresponde a CU-04).
- Base de datos relacional externa PostgreSQL (en esta fase adaptadores en memoria según ADR-002).
- Interfaz gráfica web (HTML/CSS); se provee controlador / API de entrada en Python.
