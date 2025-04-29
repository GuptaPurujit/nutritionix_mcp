# mcp_client.py

import os
import sys
import re
import logging
import asyncio
from contextlib import AsyncExitStack

from dotenv import load_dotenv

# MCP Python SDK imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

# LangChain - Ollama import
from langchain_ollama import OllamaLLM

load_dotenv()

# ──────────────────────────────────────────────────────────────────────────────
# Logger setup
# ──────────────────────────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# ──────────────────────────────────────────────────────────────────────────────
# MCPClient Definition
# ──────────────────────────────────────────────────────────────────────────────
class MCPClient:
    def __init__(self):
        self.session = None
        self.exit_stack = AsyncExitStack()
        # Initialize Ollama model (swap via LLM_MODEL env var)
        model_name = os.getenv("LLM_MODEL", "llama3")
        base_url   = os.getenv("OLLAMA_BASE_URL", None)
        self.llm   = OllamaLLM(model=model_name, base_url=base_url)  # :contentReference[oaicite:2]{index=2}

    async def connect_to_stdio_server(self, script_path: str):
        """Spawn and connect to a stdio-based MCP server."""
        cmd = sys.executable if script_path.endswith(".py") else "npx"
        params = StdioServerParameters(command=cmd, args=[script_path], env=None)
        logger.info(f"Spawning MCP server via: {cmd} {script_path}")
        reader, writer = await self.exit_stack.enter_async_context(stdio_client(params))
        self.session = await self.exit_stack.enter_async_context(ClientSession(reader, writer))
        await self.session.initialize()
        resp = await self.session.list_tools()
        logger.info("Tools via STDIO: " + ", ".join(t.name for t in resp.tools))

    async def connect_to_sse_server(self, url: str):
        """Connect to an HTTP-SSE-based MCP server."""
        logger.info(f"Connecting to SSE MCP at {url}")
        reader, writer = await (await self.exit_stack.enter_async_context(sse_client(url=url))).__aenter__()
        self.session  = await self.exit_stack.enter_async_context(ClientSession(reader, writer))
        await self.session.initialize()
        resp = await self.session.list_tools()
        logger.info("Tools via SSE: " + ", ".join(t.name for t in resp.tools))

    async def connect(self, target: str):
        """Auto-detect stdio vs. SSE based on URL pattern."""
        if re.match(r"^https?://", target):
            await self.connect_to_sse_server(target)
        else:
            await self.connect_to_stdio_server(target)

    async def process_query(self, query: str, history: list = None):
        """Send query through LLM, handle any tool_use events, and return final text."""
        if not self.session:
            raise RuntimeError("Not connected to MCP server")
        messages = history.copy() if history else []
        messages.append({"role": "user", "content": query})

        # Provide tool schemas to Ollama
        tools_resp = await self.session.list_tools()
        tools = [
            {"name": t.name, "description": t.description,
             "input_schema": dict(t.inputSchema) if t.inputSchema else {}}
            for t in tools_resp.tools
        ]

        # Call OllamaLLM (function-calling mode implicit) :contentReference[oaicite:3]{index=3}
        result = self.llm.invoke({"messages": messages, "tools": tools})

        final_text = []
        for chunk in result.content:  # streaming-capable
            if chunk.type == "text":
                final_text.append(chunk.text)
            elif chunk.type == "tool_use":
                logger.info(f"Invoking tool {chunk.name} with {chunk.input}")
                tool_res = await self.session.call_tool(chunk.name, chunk.input)
                final_text.append(f"[{chunk.name} → {tool_res.content}]")
                messages.append({"role": "tool", "content": tool_res.content})

        return "\n".join(final_text), messages
