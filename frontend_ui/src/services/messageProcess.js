import { API_URL, MODEL, TEMPERATURE, MAX_TOKENS, STREAM, AUTH_TOKEN } from "./requestConfig";

export async function sendChatRequest(messages) {
  const headers = { "Content-Type": "application/json" };
  if (AUTH_TOKEN) {
    headers.Authorization = `Bearer ${AUTH_TOKEN}`;
  }
  const response = await fetch(API_URL, {
    method: "POST",
    headers,
    body: JSON.stringify({
      model: MODEL,
      messages,
      temperature: TEMPERATURE,
      max_tokens: MAX_TOKENS,
      stream: STREAM,
    }),
  });

  if (!response.ok) {
    throw new Error(`LM Studio API error: ${response.status}`);
  }

  return response.json();
}
