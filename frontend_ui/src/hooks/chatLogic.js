import { useState } from "react";
import { sendChatRequest } from "../services/messageProcess";

export default function useChatLogic() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hello! How can I help you today?" },
  ]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (input) => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setLoading(true);

    try {
      const data = await sendChatRequest(newMessages);
      const reply = data.choices?.[0]?.message?.content || "No response";
      setMessages([...newMessages, { role: "assistant", content: reply }]);
    } catch (err) {
      setMessages([
        ...newMessages,
        { role: "assistant", content: "Error: Could not connect to LM Studio." },
      ]);
    } finally {
      setLoading(false);
    }
  };
  return { messages, loading, sendMessage };
}
