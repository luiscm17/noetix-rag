import type { Document } from '../types/document';

export interface IDocumentService {
  getAll(): Promise<{ documents: Document[] }>;
  getById(id: string): Promise<{ document: Document }>;
  upload(file: File): Promise<{ message: string; document_id: number }>;
}

export class DocumentService implements IDocumentService {
  private baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  
  private getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = this.getToken();
    const headers: HeadersInit = {
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...options.headers,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw { response: { status: response.status, data: error } };
    }

    return response.json();
  }

  async getAll(): Promise<{ documents: Document[] }> {
    return this.request<{ documents: Document[] }>('/api/documents/');
  }

  async getById(id: string): Promise<{ document: Document }> {
    return this.request<{ document: Document }>(`/api/documents/${id}`);
  }

  async upload(file: File): Promise<{ message: string; document_id: number }> {
    const token = this.getToken();
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseURL}/api/documents/upload`, {
      method: 'POST',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
      throw { response: { status: response.status, data: error } };
    }

    return response.json();
  }
}
