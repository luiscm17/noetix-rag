import { create } from 'zustand';
import type { Document } from '../types/document';
import { getDocumentService } from '../services/factory';

interface DocState {
  documents: Document[];
  loading: boolean;
  error: string | null;
  fetchDocuments: () => Promise<void>;
  uploadDocument: (file: File) => Promise<void>;
}

export const useDocStore = create<DocState>()((set) => ({
  documents: [],
  loading: false,
  error: null,
  
  fetchDocuments: async () => {
    set({ loading: true, error: null });
    try {
      const documentService = getDocumentService();
      const response = await documentService.getAll();
      set({ documents: response.documents, loading: false });
    } catch (err: unknown) {
      const e = err as { response?: { data?: { detail?: string } } };
      set({ error: e.response?.data?.detail || 'Failed to fetch documents', loading: false });
    }
  },

  uploadDocument: async (file: File) => {
    set({ loading: true, error: null });
    try {
      const documentService = getDocumentService();
      await documentService.upload(file);
      const response = await documentService.getAll();
      set({ documents: response.documents, loading: false });
    } catch (err: unknown) {
      const e = err as { response?: { data?: { detail?: string } } };
      set({ error: e.response?.data?.detail || 'Failed to upload document', loading: false });
      throw err;
    }
  }
}));
