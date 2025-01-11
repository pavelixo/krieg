from krieg.core.application import Application
from krieg.core.websocket import WebSocket
from krieg.core.responses import Response
from krieg.core.requests import Request

app = Application()

@app.get("/json")
def read_root(request: Request) -> Response:
    return Response(
        body=b'{"message":"Hello, World"}',
        status=200,
        headers={
            "Content-Type": "application/json"
        }
    )

@app.websocket("/chat")
async def websocket_chat(ws: WebSocket):
    while True:
        message = await ws.receive_text()  # Recebe a mensagem de texto
        await ws.send_text(f"Mensagem recebida: {message}")  # Envia a mensagem de volta
