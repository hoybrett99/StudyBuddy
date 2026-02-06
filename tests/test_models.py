# tests/test_models.py

import pytest
from datetime import datetime
from backend.app.models import (
    FileType,
    DocumentMetaData,
    QueryRequest,
    UploadResponse,
    ErrorResponse,
    Source,
    QueryResponse
)
from pydantic import ValidationError

# ============================================================================
# Test Enums
# ============================================================================
def test_file_type_enum():
    """Test that FileType enum has correct values"""
    assert FileType.PDF == "pdf"
    assert FileType.TXT == "txt"
    assert FileType.DOCX == "docx"

# ============================================================================
# Test DocumentMetaData
# ============================================================================
def test_document_metadata_creation():
    """Test creating a valid DocumentMetaData"""
    doc = DocumentMetaData(
        filename="test.pdf",
        file_type=FileType.PDF,
        file_size_bytes=1024
    )
    
    assert doc.filename == "test.pdf"
    assert doc.file_type == FileType.PDF
    assert doc.file_size_bytes == 1024
    assert doc.total_chunks == 0  # Default value
    assert isinstance(doc.upload_date, datetime)  # Auto-generated

def test_document_metadata_missing_required_field():
    """Test that missing required fields raise errors"""
    with pytest.raises(ValidationError):
        DocumentMetaData(
            filename="test.pdf"
            # Missing file_type and file_size_bytes
        )

# ============================================================================
# Test QueryRequest Validation
# ============================================================================
def test_query_request_valid():
    """Test creating a valid query"""
    query = QueryRequest(question="What is AI?")
    
    assert query.question == "What is AI?"
    assert query.num_contexts == 4  # Default value
    assert query.document_ids is None  # Default

def test_query_request_strips_whitespace():
    """Test that custom validator strips whitespace"""
    query = QueryRequest(question="  What is AI?  ")
    assert query.question == "What is AI?"  # Whitespace stripped

def test_query_request_empty_question():
    """Test that empty questions raise error"""
    with pytest.raises(ValidationError) as exc_info:
        QueryRequest(question="")
    
    assert "Question cannot be empty" in str(exc_info.value)

def test_query_request_whitespace_only():
    """Test that whitespace-only questions raise error"""
    with pytest.raises(ValidationError) as exc_info:
        QueryRequest(question="   ")
    
    assert "Question cannot be empty" in str(exc_info.value)

def test_query_request_too_long():
    """Test max_length validation"""
    with pytest.raises(ValidationError):
        QueryRequest(question="a" * 501)  # Exceeds max_length=500

def test_query_request_num_contexts_bounds():
    """Test that num_contexts respects min/max bounds"""
    # Valid
    query1 = QueryRequest(question="Test?", num_contexts=1)
    assert query1.num_contexts == 1
    
    query2 = QueryRequest(question="Test?", num_contexts=10)
    assert query2.num_contexts == 10
    
    # Invalid - too low
    with pytest.raises(ValidationError):
        QueryRequest(question="Test?", num_contexts=0)
    
    # Invalid - too high
    with pytest.raises(ValidationError):
        QueryRequest(question="Test?", num_contexts=11)

def test_query_request_with_document_ids():
    """Test optional document_ids field"""
    query = QueryRequest(
        question="What is AI?",
        document_ids=["doc1", "doc2", "doc3"]
    )
    
    assert len(query.document_ids) == 3
    assert "doc1" in query.document_ids

# ============================================================================
# Test UploadResponse
# ============================================================================
def test_upload_response_creation():
    """Test creating an upload response"""
    response = UploadResponse(
        success=True,
        message="File uploaded",
        filename="test.pdf",
        chunks_created=10,
        document_id="doc_123"
    )
    
    assert response.success is True
    assert response.chunks_created == 10

# ============================================================================
# Test Source
# ============================================================================
def test_source_relevance_score_bounds():
    """Test that relevance_score is between 0 and 1"""
    # Valid
    source1 = Source(
        document_name="test.pdf",
        chunk_id="chunk_1",
        relevance_score=0.85
    )
    assert source1.relevance_score == 0.85
    
    # Invalid - too low
    with pytest.raises(ValidationError):
        Source(
            document_name="test.pdf",
            chunk_id="chunk_1",
            relevance_score=-0.1
        )
    
    # Invalid - too high
    with pytest.raises(ValidationError):
        Source(
            document_name="test.pdf",
            chunk_id="chunk_1",
            relevance_score=1.5
        )

# ============================================================================
# Test QueryResponse
# ============================================================================
def test_query_response_with_sources():
    """Test creating a query response with sources"""
    sources = [
        Source(
            document_name="biology.pdf",
            chunk_id="chunk_5",
            relevance_score=0.92
        ),
        Source(
            document_name="physics.pdf",
            chunk_id="chunk_3",
            relevance_score=0.78
        )
    ]
    
    response = QueryResponse(
        answer="Photosynthesis is...",
        sources=sources,
        query_time_seconds=1.23
    )
    
    assert response.answer == "Photosynthesis is..."
    assert len(response.sources) == 2
    assert response.sources[0].relevance_score == 0.92

# ============================================================================
# Test ErrorResponse
# ============================================================================
def test_error_response_basic():
    """Test creating an error response"""
    error = ErrorResponse(
        message="File not found",
        error_type="NotFoundError"
    )
    
    assert error.error is True  # Default value
    assert error.message == "File not found"
    assert error.details is None

def test_error_response_with_details():
    """Test error response with details"""
    error = ErrorResponse(
        message="Validation failed",
        error_type="ValidationError",
        details={
            "field": "question",
            "issue": "too short"
        }
    )
    
    assert error.details["field"] == "question"

# ============================================================================
# Test JSON serialization
# ============================================================================
def test_model_to_json():
    """Test that models can be converted to JSON"""
    query = QueryRequest(question="What is AI?")
    json_data = query.model_dump()  # Pydantic v2
    # or query.dict() for Pydantic v1
    
    assert json_data["question"] == "What is AI?"
    assert json_data["num_contexts"] == 4

def test_model_from_json():
    """Test creating models from dictionaries"""
    data = {
        "question": "What is AI?",
        "num_contexts": 5
    }
    
    query = QueryRequest(**data)
    assert query.question == "What is AI?"
    assert query.num_contexts == 5