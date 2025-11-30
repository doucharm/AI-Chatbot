import { useState, useRef } from "react";
import { sendChatRequest } from "../services/messageProcess";

const GREETING = "Hello! How can I help you today?";

export default function useChatLogic() {
  const [messages, setMessages] = useState([{ role: "assistant", content: GREETING }]);
  const [loading, setLoading] = useState(false);
  const [temperature, setTemperature] = useState(0.7);
  const [responseTime, setResponseTime] = useState(null);
  const [tokenUsage, setTokenUsage] = useState(null);
  const messagesRef = useRef([{ role: "assistant", content: GREETING }]);

  const sendMessage = async (input) => {
    if (!input.trim()) return;

    setLoading(true);
    const newMessages = [...messagesRef.current, { role: "user", content: input }];
    messagesRef.current = newMessages;
    setMessages(newMessages);

    try {
      const messagesToSend = newMessages.length === 2 && newMessages[0].content === GREETING ? newMessages.slice(1) : newMessages;
      
      const startTime = Date.now();
      const data = await sendChatRequest(messagesToSend, temperature);
      const endTime = Date.now();
      
      setResponseTime(endTime - startTime);
      setTokenUsage({
        prompt_tokens: data.usage?.prompt_tokens || 0,
        completion_tokens: data.usage?.completion_tokens || 0,
        total_tokens: data.usage?.total_tokens || 0,
      });

      const reply = data.choices?.[0]?.message?.content || "No response";
      const updatedMessages = [...newMessages, { role: "assistant", content: reply }];
      messagesRef.current = updatedMessages;
      setMessages(updatedMessages);
    } catch (err) {
      setMessages(prev => [...prev, { role: "assistant", content: "Error connecting to server" }]);
    } finally {
      setLoading(false);
    }
  };

  return { messages, loading, sendMessage, temperature, setTemperature, responseTime, tokenUsage };
}

