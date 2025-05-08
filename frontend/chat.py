import mesop as me
import mesop.labs as mel
import requests

def on_load(e: me.LoadEvent):
    me.set_theme_mode("system")

@me.page(
    path="/",
    title="Nutritionix Chat Interface",
    on_load=on_load,
)
def page():
    mel.chat(
        transform,
        title="Nutritionix Chat Interface",
        bot_user="Nutritionix Bot"
    )

def transform(user_input: str, history: list[mel.ChatMessage]):
    """
    Synchronous generator for Mesop chat using requests.
    Encodes the user_input via `params=`, calls your FastAPI,
    and yields the assistant’s last message.
    """
    history_messages = []
    # Generate the chat history as a string dict
    if history is not None:
        for message in history:
            history_messages.append({"role": message.role, "message": message.content})
    
    print(user_input)
    print("##########")
    print(history_messages)
    
    # 1️⃣ Send GET exactly as your curl does, with params for safe encoding
    response = requests.post(
        "http://127.0.0.1:8002/",
        json={"query": user_input, "history": history_messages[:-1]},
        headers={"accept": "application/json", "content-type": "application/json"}
    )
    
    print(response)
    
    response.raise_for_status()

    # 2️⃣ Parse the JSON payload
    data = response.json()

    # 3️⃣ Extract the assistant’s last message
    reply = None
    if isinstance(data, dict) and "messages" in data:
        last = data["messages"][-1]
        if isinstance(last, (list, tuple)) and len(last) == 2:
            reply = last[1]
        elif isinstance(last, dict) and "content" in last:
            reply = last["content"]
    if reply is None:
        reply = str(data)

    # 4️⃣ Yield the reply so Mesop can render it
    yield reply
