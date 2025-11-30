import MessageList from "./MessageList";

function ChatWindow({ messages, loading }) {
  return (
    <div className="chat-container">
      <MessageList messages={messages} />
      {loading && <div className="typing">Assistant is typing...</div>}
    </div>
  );
}

export default ChatWindow;
