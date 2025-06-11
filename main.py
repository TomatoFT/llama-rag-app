from src.retriever import DocumentRetriever
from src.generator import TextGenerator
from src.rag_pipeline import RAGPipeline
import PyPDF2
from typing import List

def extract_text_from_pdf(pdf_path: str) -> List[str]:
    """Extract text from PDF file and split into chunks."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    
    # Split text into chunks of approximately 512 characters
    chunks = []
    current_chunk = ""
    for sentence in text.split('. '):
        if len(current_chunk) + len(sentence) < 512:
            current_chunk += sentence + '. '
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def main():
    # Initialize components
    retriever = DocumentRetriever()
    generator = TextGenerator()
    
    # Extract text from PDF
    pdf_path = 'rag_data.pdf'  # Update this path to your PDF file
    try:
        documents = extract_text_from_pdf(pdf_path)
        print(f"Extracted {len(documents)} chunks from PDF")
    except FileNotFoundError:
        print(f"PDF file not found at {pdf_path}")
        return
    
    # Add documents to the retriever
    retriever.add_documents(documents)
    
    # Create RAG pipeline
    pipeline = RAGPipeline(retriever, generator)
    
    # Example queries
    queries = [
        "What is the main topic of the document?",
        "What are the key points discussed?",
        "Can you summarize the document?"
    ]
    
    # Process queries
    for query in queries:
        print(f"\nQuery: {query}")
        result = pipeline.process_query(query)
        print(f"Response: {result['response']}")
        print("\nRetrieved documents:")
        for doc in result['retrieved_documents']:
            print(f"- {doc['document'][:200]}... (Score: {doc['score']:.2f})")

if __name__ == "__main__":
    main() 