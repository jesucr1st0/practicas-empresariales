# Plan: 006-generar-acta (CU-06 Generar acta final)

## 1. Decisiones que aplican

| ADR | Decisión | Impacto en esta funcionalidad |
|-----|----------|-------------------------------|
| [ADR-010](../../docs/adr/ADR-010-acta-final-plantilla-oficial-inmutable.md) | Acta final desde plantilla oficial e inmutable con huella SHA-256 | El acta se genera una sola vez; el documento se almacena inmutable con su huella; si hay corrección se crea una nueva acta vigente y se marca la anterior como anulada; CU-07 descarga ese mismo archivo verificando su huella. |
| [ADR-001](../../docs/adr/ADR-001-monolito-modular.md) | Monolito modular con Clean Architecture | Módulo `actas` interactúa con `practicas`, `horas`, `evaluaciones` y `reglas` mediante puertos limpios sin dependencias circulares. |
| [ADR-009](../../docs/adr/ADR-009-reglas-versionadas-por-programa.md) | Reglas versionadas por programa | Las horas mínimas requeridas se consultan de la versión de regla fijada en la práctica al registrarse (EAC-01). |
| [ADR-011](../../docs/adr/ADR-011-retencion-documental-y-datos-personales.md) | Retención documental y datos personales | El archivo del acta final no se borra ni modifica; permanece almacenado de forma inmutable. |

## 2. Componentes por capa

Basado en la [vista de desarrollo](../../docs/vistas/03-desarrollo.md):

### dominio/ (`src/modulos/actas/dominio/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `estado_acta.py` | Enum `EstadoActa`: `VIGENTE`, `ANULADA`. |
| `acta_final.py` | Entidad `ActaFinal`: `id`, `practica_id`, `fecha_emision`, `huella_integridad`, `estado`, `version_regla`, `horas_validadas`, `calificacion_evaluacion`, `ruta_archivo`, `plantilla_version`. Método `anular()`. |
| `puertos/acta_final_repository.py` | Puerto `ActaFinalRepository`: guardar, buscar_vigente_por_practica, buscar_por_id, listar_por_practica. |
| `puertos/almacen_archivos.py` | Puerto `AlmacenArchivos`: guardar_archivo, obtener_archivo (bytes). |
| `puertos/consulta_practica_acta.py` | Puerto `ConsultaPracticaActa`: consultar versión de regla y datos de la práctica. |
| `puertos/consulta_horas_acta.py` | Puerto `ConsultaHorasActa`: consultar total de horas validadas de la práctica. |
| `puertos/consulta_evaluacion_acta.py` | Puerto `ConsultaEvaluacionActa`: consultar calificación y existencia de evaluación de la empresa. |
| `puertos/consulta_reglas_acta.py` | Puerto `ConsultaReglasActa`: consultar horas mínimas para la versión de regla. |
| `puertos/generador_plantilla_acta.py` | Puerto `GeneradorPlantillaActa`: generar documento con plantilla oficial y calcular huella SHA-256. |

### aplicacion/ (`src/modulos/actas/aplicacion/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `dto.py` | DTOs: `GenerarActaDTO`, `ActaFinalDTO`, `ResultadoExportacionDTO`. |
| `generar_acta_final.py` | Caso de uso `GenerarActaFinal`: valida precondiciones (horas validadas >= mínimas, evaluación presente), genera documento oficial con huella SHA-256, almacena archivo inmutable, anula acta vigente previa si existe corrección, y registra metadatos en estado vigente. |
| `exportar_acta_final.py` | Caso de uso `ExportarActaFinal`: recupera el archivo almacenado, valida integridad contra la huella SHA-256 registrada y retorna los bytes para su descarga. |

### infraestructura/ (`src/modulos/actas/infraestructura/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `adaptador_acta_final_memoria.py` | Implementación en memoria de `ActaFinalRepository`. |
| `adaptador_almacen_archivos_memoria.py` | Implementación en memoria de `AlmacenArchivos`. |
| `adaptador_consulta_practica_memoria.py` | Adaptador en memoria de consulta de datos de práctica. |
| `adaptador_consulta_horas_memoria.py` | Adaptador en memoria de consulta de horas validadas. |
| `adaptador_consulta_evaluacion_memoria.py` | Adaptador en memoria de consulta de evaluación. |
| `adaptador_consulta_reglas_memoria.py` | Adaptador en memoria de consulta de reglas versionadas. |
| `adaptador_generador_plantilla_oficial.py` | Implementación de `GeneradorPlantillaActa` usando plantilla oficial institucional. |

### entradas/ (`src/entradas/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `controlador_actas.py` | Interfaz web interna: controlador para que el Coordinador genere y exporte el acta final. |

## 3. Flujo

### Generar acta final (Camino principal)
1. El Coordinador solicita generar el acta final para `practica_id`.
2. `GenerarActaFinal` consulta la versión de regla de la práctica vía `ConsultaPracticaActa`.
3. Consulta las horas mínimas de dicha versión vía `ConsultaReglasActa`.
4. Consulta el total de horas validadas vía `ConsultaHorasActa`:
   - Si horas_validadas < horas_minimas -> Lanza error con el motivo detallado (ej. "Horas insuficientes: 360/480").
5. Consulta la evaluación de la empresa vía `ConsultaEvaluacionActa`:
   - Si no existe evaluación -> Lanza error con el motivo ("Evaluación de empresa pendiente").
6. `GeneradorPlantillaActa` genera el documento del acta final e integra metadatos oficiales, calculando la huella SHA-256.
7. Guarda el documento binario en `AlmacenArchivos`.
8. Si ya existía un acta vigente previa para esa práctica:
   - Marca el acta anterior como `ANULADA` (nunca se borra ni edita).
9. Registra el nuevo `ActaFinal(estado=VIGENTE, huella_integridad=..., version_regla=...)`.
10. Retorna `ActaFinalDTO` al Coordinador.

### Exportar acta final (CU-07)
1. El usuario solicita exportar el acta final de la práctica.
2. `ExportarActaFinal` busca el acta vigente en `ActaFinalRepository`.
3. Recupera los bytes del archivo desde `AlmacenArchivos`.
4. Calcula el hash SHA-256 de los bytes recuperados y comprueba que coincida con `huella_integridad`.
5. Retorna `ResultadoExportacionDTO(contenido=bytes, huella=..., nombre_archivo=...)`.

## 4. Modelo de datos

```
ActaFinal
├── id: UUID
├── practica_id: UUID
├── fecha_emision: datetime
├── huella_integridad: str (SHA-256)
├── estado: EstadoActa (VIGENTE | ANULADA)
├── version_regla: str
├── horas_validadas: int
├── calificacion_evaluacion: float
├── ruta_archivo: str
└── plantilla_version: str
```

## 5. Fuera de alcance

- Firma digital PKI con validez legal (ADR-010 define huella SHA-256; firma digital con entidad certificadora está excluida en visión).
- Edición de actas ya generadas (prohibido por ADR-010).
- Eliminación de actas (prohibido por ADR-011 y RN-02).
