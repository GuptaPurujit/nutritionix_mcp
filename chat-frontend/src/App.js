import React, { useState, useEffect, useRef } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput]     = useState("");
  const locale                = navigator.language || "en-US";
  const ws                    = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:8000/ws/chat");
    ws.current.onmessage = ({ data }) => {
      const msg = JSON.parse(data);
      if (msg.type === "summary") {
        setMessages((m) => [...m, { sender: "bot", payload: msg.payload }]);
      }
    };
    return () => ws.current.close();
  }, []);

  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages((m) => [...m, { sender: "user", text: input }]);
    ws.current.send(JSON.stringify({ message: input, region: locale.split("-")[1] || "US" }));
    setInput("");
  };

  return (
    <div style={{ padding: 20 }}>
      <div style={{ height: "60vh", overflowY: "auto", border: "1px solid #ccc", padding: 10 }}>
        {messages.map((m,i) => (
          <div key={i} style={{ margin: 10 }}>
            {m.sender === "user"
              ? <strong>You: {m.text}</strong>
              : <pre>{JSON.stringify(m.payload, null, 2)}</pre>}
          </div>
        ))}
      </div>
      <input
        style={{ width: "80%", padding: 8 }}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === "Enter" && sendMessage()}
      />
      <button onClick={sendMessage} style={{ padding: 8, marginLeft: 10 }}>
        Send
      </button>
    </div>
  );
}

export default App;
