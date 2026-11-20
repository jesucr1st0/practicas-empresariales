# Plan: 007-exportar-acta (CU-07 Exportar acta final)

## 1. Decisiones que aplican

| ADR | Decisión | Impacto en esta funcionalidad |
|-----|----------|-------------------------------|
| [ADR-010](../../docs/adr/ADR-010-acta-final-plantilla-oficial-inmutable.md) | Acta inmutable con huella SHA-256; CU-07 descarga ese mismo PDF | La exportación no regenera el acta: recupera el archivo guardado en CU-06, verifica su huella y entrega solo el acta vigente. |
| [ADR-005](../../docs/adr/ADR-005-autorizacion-por-roles-y-bitacora.md) | Autorización por roles con regla de alcance y bitácora de solo inserción | Solo los roles Coordinador y Estudiante exportan; el estudiante solo exporta el acta de su propia práctica; cada intento (exitoso o fallido) se registra en la bitácora. |
| [ADR-004](../../docs/adr/ADR-004-autenticacion-sso-institucional.md) | Autenticación interna con SSO | El usuario llega ya autenticado (documento y rol); esta funcionalidad no maneja contraseñas. |
| [ADR-011](../../docs/adr/ADR-011-retencion-documental-y-datos-personales.md) | Retención documental, sin borrado físico | La exportación es de solo lectura: no modifica ni elimina el acta ni el archivo. |
| [ADR-001](../../docs/adr/ADR-001-monolito-modular.md) | Monolito modular con Clean Architecture | La autorización y la bitácora viven en el Módulo Identidad y accesos y se aplican en el adaptador de entrada (vista de desarrollo §3, RN-01 / ADR-005). |

## 2. Componentes por capa

Basado en la [vista de desarrollo](../../docs/vistas/03-desarrollo.md): Módulo Actas (CU-07), Módulo Identidad y accesos (roles y bitácora) e Interfaz web interna.

### Módulo Identidad y accesos (`src/modulos/identidad_accesos/`)

| Capa | Archivo | Responsabilidad |
|------|---------|-----------------|
| dominio | `dominio/rol.py` | Enum `Rol`: `ESTUDIANTE`, `TUTOR`, `COORDINADOR`, `ADMINISTRADOR`, `SUPERVISOR_EXTERNO` (roles de ADR-005). |
| dominio | `dominio/usuario_autenticado.py` | Valor `UsuarioAutenticado`: `documento`, `rol` (lo entrega el SSO, ADR-004). |
| aplicacion | `aplicacion/autorizador_accesos.py` | `AutorizadorAccesos`: verifica que el rol del usuario esté permitido para una acción y registra cada intento en la bitácora (`BitacoraAccesoRepository`, ya existente). Reutilizable por CU-08 y CU-09. |

### Módulo Actas (`src/modulos/actas/`)

| Capa | Archivo | Responsabilidad |
|------|---------|-----------------|
| aplicacion | `aplicacion/exportar_acta_final.py` (modificar) | `ExportarActaFinal` recibe opcionalmente el documento del estudiante solicitante y, si llega, verifica con `ConsultaPracticaActa` (puerto ya existente) que la práctica le pertenezca antes de entregar el archivo. Se mantiene compatible con el uso de CU-06. |

Los puertos `ActaFinalRepository`, `AlmacenArchivos` y `ConsultaPracticaActa` y sus adaptadores en memoria ya existen (spec 006) y se reutilizan sin cambios.

### Entradas (`src/entradas/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `controlador_exportar_acta.py` | Interfaz web interna para CU-07: recibe el `UsuarioAutenticado`, aplica el rol con `AutorizadorAccesos`, invoca `ExportarActaFinal` (con alcance si es Estudiante) y registra el resultado en la bitácora. |

### Pruebas

| Archivo | Responsabilidad |
|---------|-----------------|
| `tests/test_exportar_acta.py` | Un caso por escenario de spec.md. |

## 3. Flujo

### Camino principal (Coordinador)
1. La Interfaz web interna recibe `UsuarioAutenticado(documento="C-001", rol=COORDINADOR)`, `practica_id`, IP y agente.
2. `ControladorExportarActa` llama a `AutorizadorAccesos.verificar_rol(...)` con roles permitidos `{COORDINADOR, ESTUDIANTE}`.
3. Invoca `ExportarActaFinal.ejecutar(practica_id)`:
   1. Busca el acta vigente en `ActaFinalRepository`.
   2. Recupera los bytes desde `AlmacenArchivos`.
   3. Calcula SHA-256 y lo compara con `huella_integridad`.
   4. Retorna `ResultadoExportacionDTO`.
4. El controlador registra en la bitácora el acceso exitoso (quién, qué, cuándo, IP, agente) y retorna el archivo.

### Caminos alternos
- **Estudiante titular:** en el paso 3 se pasa `estudiante_documento`; `ExportarActaFinal` consulta `ConsultaPracticaActa` y continúa si `estudiante_documento` coincide.
- **Estudiante ajeno:** `ExportarActaFinal` lanza `PermissionError`; el controlador registra el intento fallido y propaga el error.
- **Rol no autorizado:** `AutorizadorAccesos` registra el intento fallido y lanza `PermissionError` antes de tocar el Módulo Actas.
- **Sin acta vigente / archivo alterado:** `ExportarActaFinal` lanza `ValueError`; el controlador registra el intento fallido con el motivo y propaga el error.
- **Acta corregida:** `buscar_vigente_por_practica` solo retorna el acta en estado `VIGENTE`; la anulada no se entrega.

## 4. Modelo de datos

```
UsuarioAutenticado            RegistroAcceso (existente, solo inserción)
├── documento: str            ├── sujeto: str      (documento del usuario)
└── rol: Rol                  ├── accion: str      ("exportar_acta")
                              ├── fecha: datetime
Rol (enum)                    ├── ip: str
├── ESTUDIANTE                ├── agente_usuario: str
├── TUTOR                     ├── exitoso: bool
├── COORDINADOR               └── detalle: str
├── ADMINISTRADOR
└── SUPERVISOR_EXTERNO
```

`ActaFinal` y `ResultadoExportacionDTO` se usan sin cambios (spec 006).

## 5. Fuera de alcance

- Generar o corregir el acta (CU-06, spec 006).
- Exportar actas anuladas o el historial de actas.
- Firma digital con validez legal (ADR-010).
- Gestión de permisos en base de datos (ADR-005 la plantea; en esta etapa los roles permitidos se declaran en el controlador).
- Integración real con el SSO: el `UsuarioAutenticado` se recibe ya resuelto.
