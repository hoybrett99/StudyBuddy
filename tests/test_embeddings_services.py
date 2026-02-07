# tests/test_embedding_service.py

import pytest
import numpy as np
from backend.app.services.embedding_services import EmbeddingService
from backend.app.models import DocumentChunk, DocumentMetaData, FileType
from typing import List

# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def embedding_service():
    """Create an EmbeddingService instance for testing"""
    return EmbeddingService()


@pytest.fixture
def sample_texts():
    """Sample texts for testing"""
    return [
        "Photosynthesis is the process by which plants make food",
        "The mitochondria is the powerhouse of the cell",
        "Python is a programming language"
    ]


@pytest.fixture
def sample_chunks():
    """Sample DocumentChunk objects without embeddings"""
    metadata = DocumentMetaData(
        filename="test.pdf",
        file_type=FileType.PDF,
        file_size_bytes=1024
    )
    
    return [
        DocumentChunk(
            chunk_id="doc_1_chunk_0",
            document_id="doc_1",
            text="Biology is the study of life",
            chunk_index=0,
            start_char=0,
            end_char=29,
            metadata=metadata
        ),
        DocumentChunk(
            chunk_id="doc_1_chunk_1",
            document_id="doc_1",
            text="Cells are the basic unit of life",
            chunk_index=1,
            start_char=29,
            end_char=62,
            metadata=metadata
        )
    ]


# ============================================================================
# Test Initialization
# ============================================================================

def test_embedding_service_initialization(embedding_service):
    """Test that EmbeddingService initializes correctly"""
    assert embedding_service is not None
    assert embedding_service.model is not None
    assert embedding_service.settings is not None


def test_embedding_dimension(embedding_service):
    """Test that embedding dimension is correct"""
    assert embedding_service.embedding_dim == 384


def test_model_loaded(embedding_service):
    """Test that the model is loaded"""
    assert embedding_service.model is not None
    assert hasattr(embedding_service.model, 'encode')


# ============================================================================
# Test embed_text (Single Text)
# ============================================================================

def test_embed_text_returns_list(embedding_service):
    """Test that embed_text returns a list"""
    text = "This is a test sentence"
    embedding = embedding_service.embed_text(text)
    
    assert isinstance(embedding, list)


def test_embed_text_correct_dimension(embedding_service):
    """Test that embedding has correct dimension"""
    text = "This is a test sentence"
    embedding = embedding_service.embed_text(text)
    
    assert len(embedding) == 384


def test_embed_text_returns_floats(embedding_service):
    """Test that embedding contains floats"""
    text = "This is a test sentence"
    embedding = embedding_service.embed_text(text)
    
    assert all(isinstance(x, float) for x in embedding)


def test_embed_text_normalized(embedding_service):
    """Test that embeddings are normalized (length ~1.0)"""
    text = "This is a test sentence"
    embedding = embedding_service.embed_text(text)
    
    # Calculate vector length
    length = np.linalg.norm(embedding)
    
    # Should be close to 1.0 (normalized)
    assert abs(length - 1.0) < 0.01


def test_embed_text_different_inputs(embedding_service):
    """Test that different texts produce different embeddings"""
    text1 = "The cat sat on the mat"
    text2 = "Python is a programming language"
    
    embedding1 = embedding_service.embed_text(text1)
    embedding2 = embedding_service.embed_text(text2)
    
    # Embeddings should be different
    assert embedding1 != embedding2


def test_embed_text_consistent(embedding_service):
    """Test that same text produces same embedding"""
    text = "This is a test sentence"
    
    embedding1 = embedding_service.embed_text(text)
    embedding2 = embedding_service.embed_text(text)
    
    # Should be identical
    assert embedding1 == embedding2


def test_embed_text_empty_string(embedding_service):
    """Test embedding an empty string"""
    embedding = embedding_service.embed_text("")
    
    # Should still return 384-dimensional vector
    assert len(embedding) == 384
    assert isinstance(embedding, list)


def test_embed_text_long_text(embedding_service):
    """Test embedding a long text"""
    text = "This is a sentence. " * 100  # 2000+ characters
    embedding = embedding_service.embed_text(text)
    
    assert len(embedding) == 384


# ============================================================================
# Test embed_texts (Batch Processing)
# ============================================================================

def test_embed_texts_returns_list_of_lists(embedding_service, sample_texts):
    """Test that embed_texts returns list of lists"""
    embeddings = embedding_service.embed_texts(sample_texts)
    
    assert isinstance(embeddings, list)
    assert all(isinstance(emb, list) for emb in embeddings)


def test_embed_texts_correct_count(embedding_service, sample_texts):
    """Test that embed_texts returns correct number of embeddings"""
    embeddings = embedding_service.embed_texts(sample_texts)
    
    assert len(embeddings) == len(sample_texts)


def test_embed_texts_correct_dimensions(embedding_service, sample_texts):
    """Test that all embeddings have correct dimension"""
    embeddings = embedding_service.embed_texts(sample_texts)
    
    for embedding in embeddings:
        assert len(embedding) == 384


def test_embed_texts_empty_list(embedding_service):
    """Test embedding empty list"""
    embeddings = embedding_service.embed_texts([])
    
    assert embeddings == []


def test_embed_texts_single_text(embedding_service):
    """Test embedding single text in a list"""
    texts = ["Single text"]
    embeddings = embedding_service.embed_texts(texts)
    
    assert len(embeddings) == 1
    assert len(embeddings[0]) == 384


def test_embed_texts_many_texts(embedding_service):
    """Test embedding many texts (tests batching)"""
    texts = [f"This is test sentence number {i}" for i in range(100)]
    embeddings = embedding_service.embed_texts(texts)
    
    assert len(embeddings) == 100
    assert all(len(emb) == 384 for emb in embeddings)


def test_embed_texts_normalized(embedding_service, sample_texts):
    """Test that batch embeddings are normalized"""
    embeddings = embedding_service.embed_texts(sample_texts)
    
    for embedding in embeddings:
        length = np.linalg.norm(embedding)
        assert abs(length - 1.0) < 0.01


# ============================================================================
# Test embed_chunks
# ============================================================================

@pytest.mark.asyncio
async def test_embed_chunks_returns_chunks(embedding_service, sample_chunks):
    """Test that embed_chunks returns DocumentChunk objects"""
    result = await embedding_service.embed_chunks(sample_chunks)
    
    assert isinstance(result, list)
    assert all(isinstance(chunk, DocumentChunk) for chunk in result)


@pytest.mark.asyncio
async def test_embed_chunks_adds_embeddings(embedding_service, sample_chunks):
    """Test that embeddings are added to chunks"""
    # Before: embeddings should be None
    assert all(chunk.embedding is None for chunk in sample_chunks)
    
    # After: embeddings should be present
    result = await embedding_service.embed_chunks(sample_chunks)
    
    assert all(chunk.embedding is not None for chunk in result)
    assert all(len(chunk.embedding) == 384 for chunk in result)


@pytest.mark.asyncio
async def test_embed_chunks_preserves_text(embedding_service, sample_chunks):
    """Test that original text is preserved"""
    original_texts = [chunk.text for chunk in sample_chunks]
    
    result = await embedding_service.embed_chunks(sample_chunks)
    
    result_texts = [chunk.text for chunk in result]
    assert original_texts == result_texts


@pytest.mark.asyncio
async def test_embed_chunks_preserves_metadata(embedding_service, sample_chunks):
    """Test that metadata is preserved"""
    original_ids = [chunk.chunk_id for chunk in sample_chunks]
    
    result = await embedding_service.embed_chunks(sample_chunks)
    
    result_ids = [chunk.chunk_id for chunk in result]
    assert original_ids == result_ids


@pytest.mark.asyncio
async def test_embed_chunks_empty_list(embedding_service):
    """Test embedding empty chunk list"""
    result = await embedding_service.embed_chunks([])
    
    assert result == []


@pytest.mark.asyncio
async def test_embed_chunks_modifies_in_place(embedding_service, sample_chunks):
    """Test that chunks are modified in place"""
    # Get reference to original chunks
    original_chunk = sample_chunks[0]
    
    # Embed chunks
    result = await embedding_service.embed_chunks(sample_chunks)
    
    # Original chunk should now have embedding
    assert original_chunk.embedding is not None
    assert original_chunk is result[0]


# ============================================================================
# Test calculate_similarity
# ============================================================================

def test_calculate_similarity_identical_texts(embedding_service):
    """Test similarity of identical texts"""
    text = "This is a test"
    similarity = embedding_service.calculate_similarity(text, text)
    
    # Should be very close to 1.0
    assert similarity > 0.99


def test_calculate_similarity_similar_texts(embedding_service):
    """Test similarity of similar texts"""
    text1 = "The cat sat on the mat"
    text2 = "A cat is sitting on a mat"
    
    similarity = embedding_service.calculate_similarity(text1, text2)
    
    # Should be relatively high (> 0.5)
    assert similarity > 0.5


def test_calculate_similarity_different_texts(embedding_service):
    """Test similarity of very different texts"""
    text1 = "Biology is the study of life"
    text2 = "Python is a programming language"
    
    similarity = embedding_service.calculate_similarity(text1, text2)
    
    # Should be relatively low (< 0.3)
    assert similarity < 0.3


def test_calculate_similarity_returns_float(embedding_service):
    """Test that similarity returns a float"""
    similarity = embedding_service.calculate_similarity("test", "test")
    
    assert isinstance(similarity, float)


def test_calculate_similarity_range(embedding_service, sample_texts):
    """Test that similarity is between 0 and 1"""
    # Test various pairs
    for i in range(len(sample_texts)):
        for j in range(len(sample_texts)):
            similarity = embedding_service.calculate_similarity(
                sample_texts[i], 
                sample_texts[j]
            )
            # Allow small floating point errors (similarity might be 1.0000000637)
            assert -0.01 <= similarity <= 1.01, f"Similarity {similarity} out of range"



def test_calculate_similarity_symmetric(embedding_service):
    """Test that similarity is symmetric"""
    text1 = "First text"
    text2 = "Second text"
    
    sim1 = embedding_service.calculate_similarity(text1, text2)
    sim2 = embedding_service.calculate_similarity(text2, text1)
    
    # Should be equal (or very close due to floating point)
    assert abs(sim1 - sim2) < 0.0001


# ============================================================================
# Test Edge Cases
# ============================================================================

def test_embed_special_characters(embedding_service):
    """Test embedding text with special characters"""
    text = "Test @#$% special !@# characters"
    embedding = embedding_service.embed_text(text)
    
    assert len(embedding) == 384


def test_embed_unicode(embedding_service):
    """Test embedding text with unicode characters"""
    text = "Hello 世界 🌍"
    embedding = embedding_service.embed_text(text)
    
    assert len(embedding) == 384


def test_embed_numbers(embedding_service):
    """Test embedding text with numbers"""
    text = "The year is 2024 and I have 5 apples"
    embedding = embedding_service.embed_text(text)
    
    assert len(embedding) == 384


def test_embed_mixed_case(embedding_service):
    """Test that case affects embeddings (or doesn't - model normalizes case)"""
    text1 = "hello world"
    text2 = "HELLO WORLD"
    
    embedding1 = embedding_service.embed_text(text1)
    embedding2 = embedding_service.embed_text(text2)
    
    # Calculate similarity
    similarity = np.dot(embedding1, embedding2)
    
    # The model may normalize case, so they could be identical or very similar
    assert similarity > 0.95  # Very similar (or identical)
    
    # If they're not identical, verify they're at least very close
    if embedding1 == embedding2:
        # Model normalized the case - this is fine!
        assert True
    else:
        # They're different but very similar
        assert similarity > 0.99


# ============================================================================
# Integration Tests
# ============================================================================

@pytest.mark.asyncio
async def test_full_workflow(embedding_service):
    """Test complete workflow: chunks → embeddings → similarity"""
    # Create chunks
    metadata = DocumentMetaData(
        filename="test.pdf",
        file_type=FileType.PDF,
        file_size_bytes=1024
    )
    
    chunks = [
        DocumentChunk(
            chunk_id="chunk_0",
            document_id="doc_1",
            text="Plants use photosynthesis to make energy",
            chunk_index=0,
            start_char=0,
            end_char=41,
            metadata=metadata
        ),
        DocumentChunk(
            chunk_id="chunk_1",
            document_id="doc_1",
            text="Animals eat food for energy",
            chunk_index=1,
            start_char=41,
            end_char=68,
            metadata=metadata
        )
    ]
    
    # Add embeddings
    chunks_with_embeddings = await embedding_service.embed_chunks(chunks)
    
    # Verify embeddings added
    assert all(chunk.embedding is not None for chunk in chunks_with_embeddings)
    
    # Calculate similarity between chunks
    similarity = embedding_service.calculate_similarity(
        chunks_with_embeddings[0].text,
        chunks_with_embeddings[1].text
    )
    
    # Should be somewhat similar (both about energy)
    assert similarity > 0.3


def test_batch_vs_single_consistency(embedding_service):
    """Test that batch processing gives same results as single processing"""
    texts = ["Text one", "Text two", "Text three"]
    
    # Batch processing
    batch_embeddings = embedding_service.embed_texts(texts)
    
    # Single processing
    single_embeddings = [embedding_service.embed_text(text) for text in texts]
    
    # Should be identical
    for batch, single in zip(batch_embeddings, single_embeddings):
        # Check if arrays are close (account for floating point precision)
        assert np.allclose(batch, single, rtol=1e-5)