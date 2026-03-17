export interface IChatService {
  sendMessage(message: string, sessionId?: string | null): Promise<{ response: string; session_id: string }>;
}

export class ChatService implements IChatService {
  private baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  
  private getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  async sendMessage(message: string, sessionId?: string | null): Promise<{ response: string; session_id: string }> {
    const token = this.getToken();
    
    const response = await fetch(`${this.baseURL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({ 
        message,
        session_id: sessionId 
      }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Chat request failed' }));
      throw { response: { status: response.status, data: error } };
    }

    return response.json();
  }
}
