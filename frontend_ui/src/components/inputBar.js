import  { useState } from "react";

function InputBar({ onSend }) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleSend();
  };

  return (
    <div className="input-container">
      <input
        className="input-box"
        placeholder="Send a message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyPress}
      />
      <button className="send-button" onClick={handleSend}>
        Send
      </button>
    </div>
  );
}

export default InputBar;
