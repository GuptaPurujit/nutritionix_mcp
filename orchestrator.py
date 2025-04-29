# orchestrator.py

import os
import sys
import asyncio
import argparse

# ──────────────────────────────────────────────────────────────────────────────
# On Windows, ensure subprocess_exec is supported
# ──────────────────────────────────────────────────────────────────────────────
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from mcp_client import MCPClient
from dotenv import load_dotenv

load_dotenv()

# Singleton client instance
_CLIENT = None

async def get_client():
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = MCPClient()
        target = os.getenv("MCP_SERVER_TARGET", "server.py")
        await _CLIENT.connect(target)
    return _CLIENT

async def run_meal_logging(user_input: str, region: str = "US"):
    """
    Run a meal-logging prompt through Ollama + Nutritionix MCP tools.
    """
    client = await get_client()
    # Embed region context in the user prompt
    prompt = f"{user_input} (region: {region})"
    summary, _ = await client.process_query(prompt)
    return summary

if __name__ == "__main__":
    # Quick CLI test
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Meal description")
    parser.add_argument("--region", default="IN")
    args = parser.parse_args()
    result = asyncio.run(run_meal_logging(args.input, args.region))
    print(result)
