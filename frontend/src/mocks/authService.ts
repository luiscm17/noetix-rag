import type { LoginResponse } from '../types/auth';
import { MOCK_USER } from './data';

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export class MockAuthService {
  async login(email: string, _password: string): Promise<LoginResponse> {
    await delay(800);
    
    if (!email || !_password) {
      throw { response: { status: 401, data: { detail: 'Invalid credentials' } } };
    }
    
    return {
      access_token: 'mock_token_' + Date.now(),
      token_type: 'bearer',
      user: { ...MOCK_USER, email, username: email.split('@')[0] }
    };
  }

  async register(email: string, username: string, _password: string): Promise<LoginResponse> {
    void _password;
    await delay(1000);
    
    return {
      access_token: 'mock_token_' + Date.now(),
      token_type: 'bearer',
      user: { ...MOCK_USER, email, username }
    };
  }

  async logout(): Promise<void> {
    await delay(300);
  }
}
