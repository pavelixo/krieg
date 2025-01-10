from krieg.core.types import Scope, ASGIReceiveCallable, ASGISendCallable


class WebSocket:
    async def handle(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable):
        pass
