from typing import Protocol


class EnvioCorreo(Protocol):
    def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> bool:
        ...
