from typing import List, Dict
from .retriever import DocumentRetriever
from .generator import TextGenerator

class RAGPipeline:
    def __init__(self, retriever: DocumentRetriever, generator: TextGenerator):
        """Initialize the RAG pipeline with a retriever and generator."""
        self.retriever = retriever
        self.generator = generator
        
    def process_query(self, query: str, k: int = 3) -> Dict:
        """Process a query through the RAG pipeline."""
        # Retrieve relevant documents
        retrieved_docs = self.retriever.retrieve(query, k=k)
        
        # Construct prompt with retrieved context
        context = "\n".join([doc['document'] for doc in retrieved_docs])
        prompt = f"""Context information is below.
            ---------------------
            {context}
            ---------------------
            Given the context information, please answer the following question:
            {query}

            Answer:
        """
        
        # Generate response
        response = self.generator.generate(prompt)
        
        return {
            'query': query,
            'retrieved_documents': retrieved_docs,
            'response': response
        } 