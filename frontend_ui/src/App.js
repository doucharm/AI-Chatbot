
import "./App.css";
import ChatWindow from "./components/chatWindow";
import InputBar from "./components/inputBar";
import ControlPanel from "./components/controlPanel";
import useChatLogic from "./hooks/useChatLogic";

function App() {
  const { messages, loading, sendMessage, temperature, setTemperature, responseTime, tokenUsage } = useChatLogic();

  return (
    <div className="app">
      <ControlPanel temperature={temperature} setTemperature={setTemperature} responseTime={responseTime} tokenUsage={tokenUsage} />
      <ChatWindow messages={messages} loading={loading} />
      <InputBar onSend={sendMessage} />
    </div>
  );
}

export default App;
