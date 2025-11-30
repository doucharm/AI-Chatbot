import { useEffect, useRef } from "react";
import MessageList from "./messageList";

function ChatWindow({ messages, loading }) {
  const chatEndRef = useRef(null);

  useEffect(() => {
    // Auto-scroll to bottom when messages update
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-container">
      <MessageList messages={messages} />
      <div ref={chatEndRef} />
      {loading && <div className="typing">Assistant is typing...</div>}
    </div>
  );
}
export default ChatWindow;
