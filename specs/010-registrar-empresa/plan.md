# Plan: 010-registrar-empresa (CU-10 Registrar empresa)

## 1. Decisiones que aplican

| ADR | Decisión | Impacto en esta funcionalidad |
|-----|----------|-------------------------------|
| [ADR-001](../../docs/adr/ADR-001-monolito-modular.md) | Monolito modular con Clean Architecture | La entidad `Empresa` y `Supervisor` residen en el Módulo Prácticas como datos maestros vinculados a las prácticas empresariales (CU-02). |
| [ADR-004](../../docs/adr/ADR-004-autenticacion-sso-institucional.md) | Autenticación institucional SSO | El Coordinador de prácticas se encuentra autenticado con su usuario institucional para registrar entidades maestras. |
| [ADR-005](../../docs/adr/ADR-005-autorizacion-por-roles-y-bitacora.md) | Autorización basada en roles y bitácora | Solo el rol `Coordinador de prácticas` (o Administrador) puede registrar empresas; los datos personales de contacto del supervisor quedan sujetos a la Ley 1581 (RN-01) y su registro se asienta en la bitácora de auditoría. |
| [ADR-006](../../docs/adr/ADR-006-acceso-externo-enlace-un-solo-uso.md) | Acceso externo por enlace | El supervisor registrado aquí no posee cuenta ni contraseña (RN-04); su correo y datos sirven para la emisión futura de enlaces de un solo uso en seguimiento de horas y evaluación. |

## 2. Componentes por capa

Componentes alineados con la [vista de desarrollo](../../docs/vistas/03-desarrollo.md):

### dominio/ (Módulo Prácticas)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/practicas/dominio/empresa.py` | Entidad `Empresa`: representa a la organización con `id`, `nit`, `razon_social`, `sector`, `ciudad` y `activa`. |
| `src/modulos/practicas/dominio/supervisor.py` | Entidad `Supervisor`: persona de contacto de la empresa con `id`, `empresa_nit`, `nombre`, `correo`, `telefono` y `activo`. |
| `src/modulos/practicas/dominio/puertos/empresa_repository.py` | Puerto `EmpresaRepository`: operaciones de persistencia para guardar y consultar empresas y supervisores. |

### aplicacion/ (Módulo Prácticas)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/practicas/aplicacion/dto_empresa.py` | DTOs de entrada y salida: `RegistrarEmpresaDTO`, `SupervisorDTO`, `ResultadoEmpresaDTO`, `DetalleEmpresaDTO`. |
| `src/modulos/practicas/aplicacion/registrar_empresa.py` | Caso de uso `RegistrarEmpresa`: valida unicidad del NIT, regla de negocio de supervisor obligatorio (1..*), y persiste empresa y supervisor. |
| `src/modulos/practicas/aplicacion/consultar_empresa.py` | Caso de uso `ConsultarEmpresa`: consulta de datos de la empresa y sus supervisores asociados por NIT. |

### infraestructura/ (adaptadores)

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/modulos/practicas/infraestructura/adaptador_empresa_memoria.py` | Adaptador en memoria `AdaptadorEmpresaMemoria`: implementa `EmpresaRepository` almacenando empresas y supervisores en memoria. |

### entradas/

| Archivo | Responsabilidad |
|---------|-----------------|
| `src/entradas/controlador_empresa.py` | Controlador web interno: valida rol `Coordinador de prácticas` y asienta el 100 % de los accesos y registros en la bitácora (ADR-005, RN-01). |

## 3. Flujo

### Camino principal: Registro de empresa con supervisor

1. El Coordinador de prácticas invoca `ControladorEmpresa.registrar_empresa(dto, usuario_id, rol, ip, agente_usuario)`.
2. El controlador verifica el rol `Coordinador de prácticas`. Si no coincide, rechaza con `PermissionError` y registra acceso denegado en la bitácora.
3. Se invoca el caso de uso `RegistrarEmpresa.ejecutar(dto)`.
4. El caso de uso verifica que se proporcione al menos un supervisor. Si no hay supervisores, lanza `ValueError("La empresa debe contar con al menos un supervisor.")`.
5. Se valida en `EmpresaRepository.obtener_por_nit(nit)` que no exista otra empresa con el mismo NIT. Si existe, lanza `ValueError(f"Ya existe una empresa registrada con el NIT '{nit}'.")`.
6. Se crea la entidad `Empresa` y se persiste.
7. Se crean y persisten los supervisores asociados a la empresa.
8. Se construye y retorna `ResultadoEmpresaDTO`.
9. El controlador registra en la bitácora (`RegistroAcceso`) el registro exitoso de la empresa y del supervisor.

### Camino alterno: Consulta de empresa por NIT

1. El Coordinador invoca `ControladorEmpresa.consultar_por_nit(nit, usuario_id, rol, ip, agente_usuario)`.
2. Se valida rol y se registra acceso en la bitácora.
3. El caso de uso `ConsultarEmpresa.ejecutar(nit)` obtiene la empresa y sus supervisores asociados y retorna `DetalleEmpresaDTO`.

## 4. Modelo de datos

- **Empresa**: `id: UUID`, `nit: str`, `razon_social: str`, `sector: str`, `ciudad: str`, `activa: bool`.
- **Supervisor**: `id: UUID`, `empresa_nit: str`, `nombre: str`, `correo: str`, `telefono: str`, `activo: bool`.
- **RegistroAcceso**: `sujeto: str`, `accion: str`, `fecha: datetime`, `ip: str`, `agente_usuario: str`, `exitoso: bool`, `detalle: str`.

## 5. Fuera de alcance

- Registro de contratos o convenios macro (convenios institucionales).
- Emisión o invalidación de tokens/enlaces de acceso para el supervisor (cubierto en CU-04, CU-05).
- Registro de prácticas (cubierto en CU-02).
