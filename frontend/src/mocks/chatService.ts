import { getMockChatResponse } from './data';

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export class MockChatService {
  async sendMessage(message: string, sessionId?: string | null): Promise<{ response: string; session_id: string }> {
    await delay(1200 + Math.random() * 800);
    
    return {
      response: getMockChatResponse(message),
      session_id: sessionId || `mock_session_${Date.now()}`
    };
  }
}
