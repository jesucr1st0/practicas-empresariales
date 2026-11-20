from dataclasses import dataclass
from datetime import datetime, timezone
from src.modulos.postulaciones.dominio.puertos.envio_correo import EnvioCorreo


@dataclass(frozen=True)
class CorreoEnviado:
    destinatario: str
    asunto: str
    cuerpo: str
    fecha: datetime


class AdaptadorCorreoConsola(EnvioCorreo):
    """Adaptador de correo que imprime en consola y guarda los envíos en memoria para verificación."""

    def __init__(self, silencioso: bool = False) -> None:
        self._silencioso = silencioso
        self.mensajes_enviados: list[CorreoEnviado] = []

    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> bool:
        correo = CorreoEnviado(
            destinatario=destinatario,
            asunto=asunto,
            cuerpo=cuerpo,
            fecha=datetime.now(timezone.utc),
        )
        self.mensajes_enviados.append(correo)

        if not self._silencioso:
            print(f"[CORREO A {destinatario}] Asunto: {asunto} | Cuerpo: {cuerpo}")

        return True

    def contar_por_destinatario(self, destinatario: str) -> int:
        return sum(1 for m in self.mensajes_enviados if m.destinatario == destinatario)
