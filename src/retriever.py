import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import os

class DocumentRetriever:
    def __init__(self, model_name: str = "thenlper/gte-base"):
        """Initialize the document retriever with a sentence transformer model."""
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        
    def add_documents(self, documents: List[str]):
        """Add documents to the index."""
        self.documents = documents
        # Generate embeddings for all documents
        embeddings = self.model.encode(documents)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
        
    def retrieve(self, query: str, k: int = 3) -> List[Dict]:
        """Retrieve the top k most relevant documents for a query."""
        if not self.index:
            raise ValueError("No documents have been added to the index.")
            
        # Generate query embedding
        query_embedding = self.model.encode([query])
        
        # Search the index
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Return results
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            results.append({
                'document': self.documents[idx],
                'score': float(1 / (1 + distance))  # Convert distance to similarity score
            })
            
        return results 