import { BACKEND_API_URL, MODEL, MAX_TOKENS, STREAM, AUTH_TOKEN } from "./requestConfig";

export async function sendChatRequest(messages, temperature = 0.7) {
  const headers = { "Content-Type": "application/json" };
  if (AUTH_TOKEN) headers.Authorization = `Bearer ${AUTH_TOKEN}`;

  const response = await fetch(BACKEND_API_URL, {
    method: "POST",
    headers,
    body: JSON.stringify({ model: MODEL, messages, temperature, max_tokens: MAX_TOKENS, stream: STREAM }),
  });

  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
}

