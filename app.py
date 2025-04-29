# app.py

import os
import asyncio

# ──────────────────────────────────────────────────────────────────────────────
# ON WINDOWS: switch to SelectorEventLoopPolicy so subprocess_exec is implemented
# Must happen before any import that uses asyncio.subprocess.*
# ──────────────────────────────────────────────────────────────────────────────
# ── Windows-only: enable ProactorEventLoop for subprocess support
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


# ──────────────────────────────────────────────────────────────────────────────
# FastAPI & WebSocket setup
# ──────────────────────────────────────────────────────────────────────────────
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from orchestrator import run_meal_logging  # safe now that loop policy is set

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    region: str = "IN"

@app.post("/chat")
async def chat_http(req: ChatRequest):
    return await run_meal_logging(req.message, req.region)

@app.websocket("/ws/chat")
async def chat_ws(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            result = await run_meal_logging(data["message"], data.get("region","IN"))
            await ws.send_json({"type":"summary","payload":result})
    except WebSocketDisconnect:
        pass
