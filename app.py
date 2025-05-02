from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from orchestrator import invoke_agent

class Query(BaseModel):
    query: str

app = FastAPI()

@app.get("/")
async def run_query(query: str = "", history = None):
    return await invoke_agent(query, history)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8002)