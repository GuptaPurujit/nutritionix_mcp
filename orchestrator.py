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
model = LLM().get_openai_llm()

prompt = """You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Mention the tool_name you used in the final answer (if used)

Thought:{agent_scratchpad}"""

async def invoke_agent(query: str, history: List[dict]):
    messages = []

    if history is not None:
        for message in history:
            role = "human" if message["role"] == "user" else "system"
            messages.append((role, message["message"]))

    prompt_template = ChatPromptTemplate.from_messages(messages)
    print(prompt_template)
    async with MultiServerMCPClient(server_configs) as client:
        agent = create_react_agent(model=model, tools=client.get_tools(), prompt=prompt)
        # Create list of messages from prompt template and append query
        messages = prompt_template.format_messages()
        response = await agent.ainvoke({"messages": messages})
        return response

if __name__ == "__main__":
    r = asyncio.run(invoke_agent("what's the calorie content of 1 large banana?", None))
    print(r)
