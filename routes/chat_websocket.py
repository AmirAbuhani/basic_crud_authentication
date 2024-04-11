# Communication model: WebSocket
from fastapi import APIRouter, WebSocket

router = APIRouter()


# connecting with "Simple WebSocket Client" extension.
# url: ws://localhost:8000/chat
@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if len(data) > 50:
                await websocket.send_text("Messages can be only up to 50 chars long")
                continue
            if not data[0].isupper():
                await websocket.send_text("Messages must start with uppercase")
                continue
            await websocket.send_text(f"Your message is: {data}")
    except Exception as e:
        print(e)
