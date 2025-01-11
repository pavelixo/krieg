from krieg.core.types import Scope, ASGIReceiveCallable, ASGISendCallable


class WebSocket:
    def __init__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable):
        self.scope = scope
        self.receive = receive
        self.send = send

    async def accept(self):
        """Accepts the WebSocket connection."""
        await self.send({
            "type": "websocket.accept"
        })

    async def receive_text(self):
        """Receives a text message through the WebSocket."""
        message = await self.receive()
        return message.get("text", "")

    async def send_text(self, message: str):
        """Sends a text message through the WebSocket."""
        await self.send({
            "type": "websocket.send",
            "text": message
        })
