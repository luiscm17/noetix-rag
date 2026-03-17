export interface ChatMessage {
  id: string; // client-side generated for rendering
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  message: string;
  session_id?: string | null;
}

export interface ChatResponse {
  response: string;
  session_id?: string;
}
