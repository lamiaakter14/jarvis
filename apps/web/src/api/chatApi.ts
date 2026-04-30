const API_BASE = '/api';

export interface ChatResponse {
  intent: string;
  mode: string;
  response: string;
  confidence: number;
  meta: Record<string, any>;
}

export async function sendMessage(message: string): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  if (!response.ok) throw new Error(`Chat API error: ${response.status}`);
  return response.json();
}
