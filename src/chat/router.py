from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter(
    prefix="",
    tags=["Chat"]
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_db: bool):
        # if add_to_db:
        #     await self.add_messages_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)



manager = ConnectionManager()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)),'./templates'))

@router.get("/chat")
def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

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