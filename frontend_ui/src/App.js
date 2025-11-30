
import "./App.css";
import ChatWindow from "./components/chatWindow";
import InputBar from "./components/inputBar";
import useChatLogic from "./hooks/useChatLogic";

function App() {
  const { messages, loading, sendMessage } = useChatLogic();

  return (
    <div className="app">
      <ChatWindow messages={messages} loading={loading} />
      <InputBar onSend={sendMessage} />
    </div>
  );
}

export default App;
