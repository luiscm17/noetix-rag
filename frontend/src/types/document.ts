export interface Document {
  document_id: number;
  user_id: number;
  title: string;
  file_path: string;
  page_count: number;
  created_at: string;
  updated_at: string;
  tags: string[] | null;
  status: 'pending' | 'processing' | 'processed' | 'error';
}

export interface DocumentListResponse {
  documents: Document[];
}

export interface SingleDocumentResponse {
  document: Document;
}

export interface UploadResponse {
  message: string;
  document_id: number;
}
