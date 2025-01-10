from krieg.core.application import Application
from krieg.core.decorators import get, post
from krieg.core.requests import Request
from krieg.core.responses import Response

app = Application()

@get("/hello")
async def hello_world(request: Request) -> Response:
    return Response(body=b"Hello, World!")

@post("/data")
async def handle_post(request: Request) -> Response:
    body = await request.body()
    return Response(body=body)

app.add_route(hello_world.method, hello_world.path, hello_world)
app.add_route(handle_post.method, handle_post.path, handle_post)
