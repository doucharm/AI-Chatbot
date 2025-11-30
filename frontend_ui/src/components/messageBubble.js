function MessageBubble({ role, content }) {
  return <div className={`message ${role}`}>{content}</div>;
}
export default MessageBubble;
