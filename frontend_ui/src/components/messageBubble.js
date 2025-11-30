function MessageBubble({ role, content }) {
  return (
    <div className={`message-wrapper ${role}`}>
      <div className={`message ${role}`}>
        {content}
      </div>
    </div>
  );
}
export default MessageBubble;
