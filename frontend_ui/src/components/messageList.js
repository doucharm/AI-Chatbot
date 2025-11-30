import MessageBubble from "./messageBubble";

function MessageList({ messages }) {
  return (
    <div className="message-list">
      {messages.map((msg, i) => (
        <MessageBubble key={i} role={msg.role} content={msg.content} />
      ))}
    </div>
  );
}

export default MessageList;
