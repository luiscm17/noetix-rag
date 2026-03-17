import { create } from 'zustand';
import type { ChatMessage } from '../types/chat';
import { getChatService } from '../services/factory';

interface ChatState {
  messages: ChatMessage[];
  sessionId: string | null;
  loading: boolean;
  error: string | null;
  sendMessage: (message: string) => Promise<void>;
  clearSession: () => void;
}

export const useChatStore = create<ChatState>()((set, get) => ({
  messages: [],
  sessionId: null,
  loading: false,
  error: null,

  sendMessage: async (content: string) => {
    const { sessionId, messages } = get();
    
    const userMsg: ChatMessage = { id: Date.now().toString(), role: 'user', content };
    set({ messages: [...messages, userMsg], loading: true, error: null });

    try {
      const chatService = getChatService();
      const response = await chatService.sendMessage(content, sessionId);
      
      const aiMsg: ChatMessage = { 
        id: (Date.now() + 1).toString(), 
        role: 'assistant', 
        content: response.response 
      };

      set({ 
        messages: [...get().messages, aiMsg], 
        sessionId: response.session_id || sessionId,
        loading: false 
      });
    } catch (err: unknown) {
      const e = err as { response?: { data?: { detail?: string } } };
      set({ error: e.response?.data?.detail || 'Failed to send message', loading: false });
    }
  },

  clearSession: () => {
    set({ messages: [], sessionId: null, error: null });
  }
}));
