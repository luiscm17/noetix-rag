import { create } from 'zustand';
import type { User, LoginResponse } from '../types/auth';
import { getAuthService } from '../services/factory';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuth: (data: LoginResponse) => void;
  logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()((set) => ({
  user: null,
  token: localStorage.getItem('access_token'),
  isAuthenticated: !!localStorage.getItem('access_token'),
  setAuth: (data) => {
    localStorage.setItem('access_token', data.access_token);
    set({
      user: data.user,
      token: data.access_token,
      isAuthenticated: true,
    });
  },
  logout: async () => {
    try {
      const authService = getAuthService();
      await authService.logout();
    } catch {
      // Ignore logout errors
    } finally {
      localStorage.removeItem('access_token');
      set({
        user: null,
        token: null,
        isAuthenticated: false,
      });
    }
  },
}));
