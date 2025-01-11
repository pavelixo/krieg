from typing import Callable
from krieg.core.types import Scope, ASGIReceiveCallable, ASGISendCallable


class WebSocket:
    def __init__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable):
        self.scope = scope
        self.receive = receive
        self.send = send

    async def accept(self):
        """Aceita a conexão WebSocket."""
        await self.send({
            "type": "websocket.accept"
        })

    async def receive_text(self):
        """Recebe uma mensagem de texto através do WebSocket."""
        message = await self.receive()
        return message.get("text", "")

    async def send_text(self, message: str):
        """Envia uma mensagem de texto através do WebSocket."""
        await self.send({
            "type": "websocket.send",
            "text": message
        })
