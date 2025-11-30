import MessageBubble from "./messageBubble";

function MessageList({ messages }) {
  return (
    <>
      {messages.map((msg, i) => (
        <MessageBubble key={i} role={msg.role} content={msg.content} />
      ))}
    </>
  );
}

export default MessageList;
