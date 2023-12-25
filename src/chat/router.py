from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
import os
from .utils import manager

router = APIRouter(
    prefix="",
    tags=["Chat"]
)



templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)),'./templates'))

@router.get("/chat")
def get_chat_page(request: Request):
    http_protocol = request.headers.get("x-forwarded-proto", "http")
    ws_protocol = "wss" if http_protocol == "https" else "ws"
    server_url = request.url.netloc
    return templates.TemplateResponse("chat.html", {"request": request,
                                       "http_protocol": http_protocol,
                                       "ws_protocol": ws_protocol,
                                       "server_url": server_url})

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)