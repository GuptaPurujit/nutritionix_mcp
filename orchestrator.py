import json
import asyncio

from typing import List

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent

from llm import LLM

with open("config.json", "r") as file:
    server_configs = json.loads(file.read())
    

# create a model
model = LLM().get_llm()

template = """Answer user queries, and use tools like get_nutrients or search_food to answer questions if you are not sure. User might use hindi terms for food items so make sure you clarify if you are not sure on what the food item is, but don't ask always if not required.
"""

messages = [
    ("system", template)
]

async def invoke_agent(query: str, history = None):
    if history is not None:
        for message in history:
            messages.append(("system", message))
            
    messages.append(("human", query))

    prompt_template = ChatPromptTemplate.from_messages(messages)
    print(prompt_template)
    async with MultiServerMCPClient(server_configs) as client:
        agent = create_react_agent(model, client.get_tools())
        response = await agent.ainvoke({"messages": query})
        return response

if __name__ == "__main__":
    r = asyncio.run(invoke_agent("what's the calorie content of 1 large banana?", None))
    print(r)
