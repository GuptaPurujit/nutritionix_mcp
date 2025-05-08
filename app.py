from typing import List, Any

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from orchestrator import invoke_agent

class Query(BaseModel):
    query: str
    history: List[dict]

app = FastAPI()

@app.post("/")
async def run_query(query: Query):
    return await invoke_agent(query.query, query.history)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8002)