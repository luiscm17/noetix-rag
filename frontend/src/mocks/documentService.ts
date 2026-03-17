import type { Document } from '../types/document';
import { MOCK_DOCUMENTS } from './data';

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export class MockDocumentService {
  async getAll(): Promise<{ documents: Document[] }> {
    await delay(600);
    return { documents: MOCK_DOCUMENTS as Document[] };
  }

  async getById(id: string): Promise<{ document: Document }> {
    await delay(400);
    const doc = MOCK_DOCUMENTS.find(d => d.document_id.toString() === id);
    if (!doc) {
      throw { response: { status: 404, data: { detail: 'Document not found' } } };
    }
    return { document: doc as Document };
  }

  async upload(_file: File): Promise<{ message: string; document_id: number }> {
    void _file;
    await delay(1500);
    return {
      message: 'Document uploaded successfully',
      document_id: Date.now()
    };
  }
}
