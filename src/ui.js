// Simple React component for chatbot UI
import React, { useState } from 'react';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");

  const sendMessage = async () => {
    const response = await fetch("/api/chat", {  // Backend API to handle requests
      method: "POST",
      body: JSON.stringify({ message: userInput }),
      headers: { "Content-Type": "application/json" }
    });
    const data = await response.json();
    setMessages([...messages, { user: userInput, bot: data.reply }]);
    setUserInput("");
  };

  return (
    <div>
      <div className="chatbox">
        {messages.map((msg, index) => (
          <div key={index}>
            <strong>User:</strong> {msg.user}
            <br />
            <strong>Bot:</strong> {msg.bot}
            <hr />
          </div>
        ))}
      </div>
      <input 
        type="text" 
        value={userInput} 
        onChange={(e) => setUserInput(e.target.value)} 
        placeholder="Ask me something..." 
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default Chatbot;
