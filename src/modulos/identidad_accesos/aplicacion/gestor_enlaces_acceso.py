from datetime import datetime, timedelta, timezone
import hashlib
import secrets
from uuid import UUID

from src.modulos.identidad_accesos.dominio.enlace_acceso import EnlaceAcceso
from src.modulos.identidad_accesos.dominio.puertos.bitacora_acceso_repository import BitacoraAccesoRepository
from src.modulos.identidad_accesos.dominio.puertos.enlace_acceso_repository import EnlaceAccesoRepository
from src.modulos.identidad_accesos.dominio.registro_acceso import RegistroAcceso


class GestorEnlacesAcceso:
    def __init__(
        self,
        enlace_repositorio: EnlaceAccesoRepository,
        bitacora_repositorio: BitacoraAccesoRepository,
    ):
        self._enlace_repositorio = enlace_repositorio
        self._bitacora_repositorio = bitacora_repositorio

    def emitir_enlace(
        self,
        practica_id: UUID,
        email_destinatario: str,
        dias_vigencia: int = 30,
        acciones_permitidas: list[str] | None = None,
    ) -> str:
        # Token aleatorio criptográfico de 256 bits (> 128 bits requeridos por ADR-006)
        token = secrets.token_urlsafe(32)
        token_hash = self.calcular_hash(token)
        fecha_emision = datetime.now(timezone.utc)
        fecha_vencimiento = fecha_emision + timedelta(days=dias_vigencia)

        enlace = EnlaceAcceso(
            token_hash=token_hash,
            practica_id=practica_id,
            email_destinatario=email_destinatario,
            fecha_emision=fecha_emision,
            fecha_vencimiento=fecha_vencimiento,
            acciones_permitidas=acciones_permitidas or ["validar_horas", "evaluar"],
        )
        self._enlace_repositorio.guardar(enlace)
        return token

    def validar_token(self, token: str, ip: str, agente_usuario: str) -> EnlaceAcceso:
        token_hash = self.calcular_hash(token)
        enlace = self._enlace_repositorio.buscar_por_hash(token_hash)

        if enlace is None:
            self._bitacora_repositorio.registrar(
                RegistroAcceso(
                    sujeto=token_hash[:10],
                    accion="validar_enlace",
                    ip=ip,
                    agente_usuario=agente_usuario,
                    exitoso=False,
                    detalle="Acceso denegado: token no existe",
                )
            )
            raise ValueError("enlace no disponible; pida al coordinador que lo reemita")

        if not enlace.esta_vigente():
            self._bitacora_repositorio.registrar(
                RegistroAcceso(
                    sujeto=token_hash[:10],
                    accion="validar_enlace",
                    ip=ip,
                    agente_usuario=agente_usuario,
                    exitoso=False,
                    detalle=f"Acceso denegado: enlace no vigente ({enlace.estado.value})",
                )
            )
            raise ValueError("enlace no disponible; pida al coordinador que lo reemita")

        self._bitacora_repositorio.registrar(
            RegistroAcceso(
                sujeto=token_hash[:10],
                accion="validar_enlace",
                ip=ip,
                agente_usuario=agente_usuario,
                exitoso=True,
                detalle=f"Acceso autorizado para práctica {enlace.practica_id}",
            )
        )
        return enlace

    def marcar_usado(self, token: str) -> None:
        token_hash = self.calcular_hash(token)
        enlace = self._enlace_repositorio.buscar_por_hash(token_hash)
        if enlace:
            enlace.marcar_usado()
            self._enlace_repositorio.guardar(enlace)

    @staticmethod
    def calcular_hash(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
