import ReactMarkdown from 'react-markdown';

function MessageBubble({ role, content }) {
  return (
    <div className={`message-wrapper ${role}`}>
      <div className={`message ${role}`}>
        {/* ReactMarkdown parses the string and renders HTML */}
        <ReactMarkdown>{String(content)}</ReactMarkdown>
      </div>
    </div>
  );
}
export default MessageBubble;
