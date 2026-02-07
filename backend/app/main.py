"""
Main FastAPI application.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import time
from pathlib import Path

from app.models import (
    UploadResponse,
    QueryRequest,
    QueryResponse,
    ErrorResponse,
    SystemStats,
    FileType,
    DocumentMetadata
)
from app.config import Settings, get_settings
from app.services.document_services import DocumentService
# from app.services.embedding_service import EmbeddingService
# from app.services.rag_service import RAGService

# FastAPI App
app = FastAPI(
    title="Study Buddy API",
    description="RAG based study assistant",
    version="0.0.1"
)

# Allows frontend to call the api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# These functions create instances of our services
# FastAPI will call them automatically when needed

def get_document_service() -> DocumentService:
    return DocumentService()

# def get_embedding_service() -> EmbeddingService:
#     return EmbeddingService()

# def get_rag_service() -> RAGService:
#     return RAGService()

# Route Handlers
@app.post(
    "/upload",
    response_model=UploadResponse,
    summary="Upload a document",
    description="Upload a PDF, TXT, or DOCX file for processing"
)
async def upload_document(
    file: UploadFile = File(...),
    doc_service: DocumentService = Depends(get_document_service)
    # emb_service: EmbeddingService = Depends(get_embedding_service)
    # rag_service: RAGService = Depends(get_rag_service)
):
    """
    Upload and process a document.
    
    The function signature tells FastAPI:
    - Expect a file upload
    - Inject the services we need
    - Return an UploadResponse
    """
    try:
        # Validate file type
        file_extension = Path(file.filename).suffix[1:].lower()

        if file_extension not in Settings.allowed_file_type:
            raise HTTPException(
                status_code=400,
                detail=f"File type .{file_extension} not supported"
            )
        
        file_type = FileType(file_extension)

        # Read file content
        content = await file.read()

        # Check file size
        file_size = len(content)
        max_size = Settings.max_file_size_mb * 1024 * 1024

        if file_size > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File is curerntly {file_size}. Max size: {Settings.max_file_size_mb}MB."
            )
        
        # Save file
        file_path = await doc_service.save_file(file.filename, content)

        # Extract text
        text = doc_service.text_extraction(file_path, file_type)

        # Create metadata
        document_id = file_path.stem # filename without extension
        metadata = DocumentMetadata(
            filename=file.filename,
            file_type=file_type,
            file_size_bytes=file_size
        )

        # Create chunks
        chunks = doc_service.create_chunks(text, document_id, metadata)

        # Generate embeddings
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        # Catch all other errors
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )