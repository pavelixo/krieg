from krieg.core.responses import Response
from krieg.core.requests import Request
from krieg.core.types import Scope, ASGIReceiveCallable, ASGISendCallable

class HTTP:
    async def handle(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable):
        request = Request(scope, receive)
        body = await request.body()
        response = Response(body=body)
        await response.send(send)
