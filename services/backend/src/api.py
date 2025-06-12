from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from pathlib import Path
import shutil
from .retriever import DocumentRetriever
from .generator import TextGenerator
from .rag_pipeline import RAGPipeline
import PyPDF2
from typing import List

# Get the absolute path to the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="LLaMA RAG API",
    description="API for document processing and querying using LLaMA and RAG",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize components
retriever = DocumentRetriever()
generator = TextGenerator()
pipeline = None

class Query(BaseModel):
    text: str
    k: Optional[int] = 3

class QueryResponse(BaseModel):
    query: str
    response: str
    retrieved_documents: List[dict]

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

@app.post("/upload", summary="Upload a PDF document")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF document for processing."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Create uploads directory if it doesn't exist
    upload_dir = BASE_DIR / "uploads"
    upload_dir.mkdir(exist_ok=True)
    
    # Save the uploaded file
    file_path = upload_dir / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Process the PDF
        documents = extract_text_from_pdf(str(file_path))
        
        # Update the retriever with new documents
        global pipeline
        retriever.add_documents(documents)
        pipeline = RAGPipeline(retriever, generator)
        
        return {
            "message": "Document processed successfully",
            "chunks": len(documents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the uploaded file
        if file_path.exists():
            file_path.unlink()

@app.post("/query", response_model=QueryResponse, summary="Query the document")
async def query_document(query: Query):
    """Query the processed document."""
    if pipeline is None:
        raise HTTPException(
            status_code=400,
            detail="No document has been processed yet. Please upload a document first."
        )
    
    try:
        result = pipeline.process_query(query.text, k=query.k)
        return QueryResponse(
            query=result['query'],
            response=result['response'],
            retrieved_documents=result['retrieved_documents']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", summary="Health check")
async def health_check():
    """Check if the API is running and ready."""
    return {
        "status": "healthy",
        "model_loaded": pipeline is not None
    } 