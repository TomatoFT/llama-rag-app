from typing import List, Dict
from .retriever import DocumentRetriever
from .generator import TextGenerator

class RAGPipeline:
    def __init__(self, retriever: DocumentRetriever, generator: TextGenerator):
        """Initialize the RAG pipeline with a retriever and generator."""
        self.retriever = retriever
        self.generator = generator
        
    def process_query(self, query: str, k: int = 2) -> Dict:
        """Process a query using the RAG pipeline."""
        # Retrieve relevant documents
        retrieved_docs = self.retriever.retrieve(query, k=k)
        
        # Prepare context from retrieved documents
        context = "\n".join([doc['document'] for doc in retrieved_docs])
        
        # Create prompt with optimized format
        prompt = f"""<s>[INST] You are a helpful AI assistant. Use the following context to answer the question. If you cannot find the answer in the context, say so.

Context:
{context}

Question: {query}

Answer: [/INST]"""
        
        # Generate response
        response = self.generator.generate(prompt)
        
        return {
            'query': query,
            'response': response,
            'retrieved_documents': retrieved_docs
        } 