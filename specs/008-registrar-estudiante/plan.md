# Plan: 008-registrar-estudiante (CU-08 Registrar estudiante)

## 1. Decisiones que aplican

| ADR | Decisión | Impacto en esta funcionalidad |
|-----|----------|-------------------------------|
| [ADR-005](../../docs/adr/ADR-005-autorizacion-por-roles-y-bitacora.md) | Autorización por roles y bitácora de solo inserción | Solo el rol Administrador registra estudiantes; cada intento (exitoso o fallido) queda en la bitácora (RN-01: tratamiento de datos personales). |
| [ADR-004](../../docs/adr/ADR-004-autenticacion-sso-institucional.md) | Autenticación interna con SSO | El estudiante no tiene contraseña en el sistema: `Estudiante` no tiene ese atributo. El Administrador llega ya autenticado. |
| [ADR-007](../../docs/adr/ADR-007-integracion-sia-adaptador-aislado.md) | Datos académicos solo por el Adaptador SIA | `Estudiante` no replica datos académicos (vista lógica: «se consultan al SIA, no se replican»). |
| [ADR-001](../../docs/adr/ADR-001-monolito-modular.md) | Monolito modular con Clean Architecture | La entidad, el puerto, el caso de uso y el adaptador viven en un solo módulo; autorización y bitácora se aplican en el adaptador de entrada. |

## 2. Componentes por capa

Basado en la [vista de desarrollo](../../docs/vistas/03-desarrollo.md). **Pendiente:** la vista no asigna CU-08 a un módulo; se ubica en el **Módulo Prácticas**, que ya atiende CU-12 (Consultar datos estudiante) y guarda `estudiante_documento` en cada `Practica`.

### dominio/ (`src/modulos/practicas/dominio/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `estudiante.py` | Entidad `Estudiante`: `documento`, `nombre`, `programa`, `correo`. Valida que ningún dato obligatorio esté vacío. |
| `puertos/estudiante_repository.py` | Puerto `EstudianteRepository`: `guardar`, `obtener_por_documento`. |

### aplicacion/ (`src/modulos/practicas/aplicacion/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `registrar_estudiante_dto.py` | DTO de entrada `RegistrarEstudianteDTO`. |
| `resultado_estudiante_dto.py` | DTO de salida `ResultadoEstudianteDTO`. |
| `registrar_estudiante.py` | Caso de uso `RegistrarEstudiante`: rechaza documentos repetidos, crea el `Estudiante` y lo guarda. |

### infraestructura/ (`src/modulos/practicas/infraestructura/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `adaptador_estudiante_memoria.py` | Implementación en memoria de `EstudianteRepository`. |

### entradas/ (`src/entradas/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `controlador_estudiante.py` | Interfaz web interna: aplica el rol Administrador con `AutorizadorAccesos` (spec 007) y registra el resultado en la bitácora. |

### Pruebas

| Archivo | Responsabilidad |
|---------|-----------------|
| `tests/test_registrar_estudiante.py` | Un caso por escenario de spec.md. |

## 3. Flujo

### Camino principal
1. La Interfaz web interna recibe `UsuarioAutenticado(documento="A-001", rol=ADMINISTRADOR)`, los datos del estudiante, IP y agente.
2. `ControladorEstudiante` llama a `AutorizadorAccesos.verificar_rol(...)` con rol permitido `{ADMINISTRADOR}`.
3. Construye `RegistrarEstudianteDTO` e invoca `RegistrarEstudiante.ejecutar(dto)`:
   1. Consulta `EstudianteRepository.obtener_por_documento`; si existe, lanza `ValueError`.
   2. Crea `Estudiante(...)`, que valida los datos obligatorios.
   3. Guarda el estudiante y retorna `ResultadoEstudianteDTO`.
4. El controlador registra el acceso exitoso en la bitácora y retorna el resultado.

### Caminos alternos
- **Documento repetido / datos incompletos:** el caso de uso lanza `ValueError`; el controlador registra el intento fallido con el motivo y propaga el error.
- **Rol no autorizado:** `AutorizadorAccesos` registra el intento fallido y lanza `PermissionError` antes de invocar el caso de uso.

## 4. Modelo de datos

```
Estudiante
├── documento: str   (identificador único)
├── nombre: str
├── programa: str
└── correo: str      (correo institucional, ADR-013)
```

Sin contraseña (ADR-004) y sin datos académicos (ADR-007).

## 5. Fuera de alcance

- Verificar en el SIA que el documento corresponde a un estudiante activo (no lo piden drivers.md ni la vista; queda pendiente de confirmar con el Administrador del SIA, R-07).
- Editar o dar de baja estudiantes.
- Consultar datos del estudiante (CU-12).
- Crear la cuenta en el SSO institucional (la gestiona el SSO, ADR-004).
