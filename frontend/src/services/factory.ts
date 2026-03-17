import type { IAuthService } from '../services/authService';
import type { IDocumentService } from '../services/documentService';
import type { IChatService } from '../services/chatService';

import { AuthService } from '../services/authService';
import { DocumentService } from '../services/documentService';
import { ChatService } from '../services/chatService';

import { MockAuthService } from '../mocks/authService';
import { MockDocumentService } from '../mocks/documentService';
import { MockChatService } from '../mocks/chatService';

const USE_MOCKS = import.meta.env.VITE_USE_MOCK === 'true';

export interface ServiceFactory {
  auth: IAuthService;
  document: IDocumentService;
  chat: IChatService;
}

function createAuthService(): IAuthService {
  return USE_MOCKS ? new MockAuthService() : new AuthService();
}

function createDocumentService(): IDocumentService {
  return USE_MOCKS ? new MockDocumentService() : new DocumentService();
}

function createChatService(): IChatService {
  return USE_MOCKS ? new MockChatService() : new ChatService();
}

export const services: ServiceFactory = {
  auth: createAuthService(),
  document: createDocumentService(),
  chat: createChatService(),
};

export function getAuthService(): IAuthService {
  return services.auth;
}

export function getDocumentService(): IDocumentService {
  return services.document;
}

export function getChatService(): IChatService {
  return services.chat;
}
