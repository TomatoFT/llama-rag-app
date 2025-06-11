export interface Query {
  text: string;
  k?: number;
}

export interface QueryResponse {
  query: string;
  response: string;
  retrieved_documents: Record<string, any>[];
}

export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}

export interface HTTPValidationError {
  detail: ValidationError[];
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  retrievedDocs?: Record<string, any>[];
}