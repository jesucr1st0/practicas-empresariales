# Plan: 009-registrar-tutor (CU-09 Registrar tutor)

## 1. Decisiones que aplican

| ADR | Decisión | Impacto en esta funcionalidad |
|-----|----------|-------------------------------|
| [ADR-005](../../docs/adr/ADR-005-autorizacion-por-roles-y-bitacora.md) | Autorización por roles y bitácora de solo inserción | Solo el rol Administrador registra tutores; cada intento (exitoso o fallido) queda en la bitácora (RN-01). |
| [ADR-004](../../docs/adr/ADR-004-autenticacion-sso-institucional.md) | Autenticación interna con SSO | El tutor no tiene contraseña en el sistema; la entidad `Tutor` no tiene ese atributo. |
| [ADR-012](../../docs/adr/ADR-012-asignacion-tutores-sugerida-con-confirmacion.md) | Asignación de tutores sugerida con confirmación | El tutor registrado queda activo en su programa, que es el dato del que parte la sugerencia de CU-01. |
| [ADR-001](../../docs/adr/ADR-001-monolito-modular.md) | Monolito modular con Clean Architecture | La vista de desarrollo asigna CU-09 al **Módulo Tutores y asignación**; la autorización y la bitácora se aplican en el adaptador de entrada. |

## 2. Componentes por capa

Basado en la [vista de desarrollo](../../docs/vistas/03-desarrollo.md): Módulo Tutores y asignación (CU-01, CU-09, CU-11).

### dominio/ (`src/modulos/tutores_asignacion/dominio/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `tutor.py` (existente, sin cambios) | Entidad `Tutor`: `documento`, `nombre`, `correo`, `programa`, `activo`. |
| `puertos/tutor_repository.py` | Puerto `TutorRepository`: `guardar`, `obtener_por_documento`. |

### aplicacion/ (`src/modulos/tutores_asignacion/aplicacion/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `registrar_tutor_dto.py` | DTO de entrada `RegistrarTutorDTO`. |
| `resultado_tutor_dto.py` | DTO de salida `ResultadoTutorDTO`. |
| `registrar_tutor.py` | Caso de uso `RegistrarTutor`: valida los datos obligatorios, rechaza documentos repetidos, crea el `Tutor` activo y lo guarda. |

### infraestructura/ (`src/modulos/tutores_asignacion/infraestructura/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `adaptador_tutor_memoria.py` | Implementación en memoria de `TutorRepository`. |

### entradas/ (`src/entradas/`)

| Archivo | Responsabilidad |
|---------|-----------------|
| `controlador_tutor.py` | Interfaz web interna: aplica el rol Administrador con `AutorizadorAccesos` (spec 007) y registra el resultado en la bitácora. |

### Pruebas

| Archivo | Responsabilidad |
|---------|-----------------|
| `tests/test_registrar_tutor.py` | Un caso por escenario de spec.md. |

## 3. Flujo

### Camino principal
1. La Interfaz web interna recibe `UsuarioAutenticado(documento="A-001", rol=ADMINISTRADOR)`, los datos del tutor, IP y agente.
2. `ControladorTutor` llama a `AutorizadorAccesos.verificar_rol(...)` con rol permitido `{ADMINISTRADOR}`.
3. Construye `RegistrarTutorDTO` e invoca `RegistrarTutor.ejecutar(dto)`:
   1. Verifica que documento, nombre, correo y programa no estén vacíos; si alguno falta, lanza `ValueError`.
   2. Consulta `TutorRepository.obtener_por_documento`; si existe, lanza `ValueError`.
   3. Crea `Tutor(..., activo=True)`, lo guarda y retorna `ResultadoTutorDTO`.
4. El controlador registra el acceso exitoso en la bitácora y retorna el resultado.

### Caminos alternos
- **Documento repetido / datos incompletos:** el caso de uso lanza `ValueError`; el controlador registra el intento fallido con el motivo y propaga el error.
- **Rol no autorizado:** `AutorizadorAccesos` registra el intento fallido y lanza `PermissionError` antes de invocar el caso de uso.

## 4. Modelo de datos

```
Tutor (existente)
├── documento: str   (identificador único)
├── nombre: str
├── correo: str
├── programa: str
└── activo: bool     (True al registrarse)
```

Sin contraseña (ADR-004).

## 5. Fuera de alcance

- Conectar `TutorRepository` con `AsignacionRepository.listar_tutores_activos` (spec 001). Hoy el adaptador en memoria de asignaciones recibe su propia lista de tutores. Con la base de datos relacional (ADR-002), ambos puertos leerán la misma tabla. Queda **pendiente** para la composición (`src/composicion/`).
- Editar o desactivar tutores.
- Consultar datos del tutor (CU-11) y verificarlos en el SIA.
- Crear la cuenta en el SSO institucional (ADR-004).
