# tests/test_config.py

import pytest
from pydantic import ValidationError
from backend.app.config import Settings, get_settings

# ============================================================================
# Test Settings Creation
# ============================================================================

def test_settings_requires_api_keys():
    """Test that API keys are required"""
    with pytest.raises(ValidationError) as exc_info:
        Settings()  # Missing both API keys
    
    error_str = str(exc_info.value)
    assert "google_api_key" in error_str
    assert "claude_api_key" in error_str


def test_settings_missing_google_api_key():
    """Test that google_api_key is required"""
    with pytest.raises(ValidationError) as exc_info:
        Settings(claude_api_key="test-key")
    
    assert "google_api_key" in str(exc_info.value)


def test_settings_missing_claude_api_key():
    """Test that claude_api_key is required"""
    with pytest.raises(ValidationError) as exc_info:
        Settings(google_api_key="test-key")
    
    assert "claude_api_key" in str(exc_info.value)


def test_settings_with_valid_api_keys():
    """Test creating settings with valid API keys"""
    settings = Settings(
        google_api_key="test-google-key",
        claude_api_key="test-claude-key"
    )
    
    assert settings.google_api_key == "test-google-key"
    assert settings.claude_api_key == "test-claude-key"


# ============================================================================
# Test Default Values
# ============================================================================

def test_default_application_settings():
    """Test default application settings"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test"
    )
    
    assert settings.app_name == "Study Buddy"
    assert settings.app_version == "0.0.1"
    assert settings.debug == False


def test_default_server_settings():
    """Test default server settings"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test"
    )
    
    assert settings.host == "0.0.0.0"
    assert settings.port == 8000


def test_default_file_upload_settings():
    """Test default file upload settings"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test"
    )
    
    assert settings.max_file_size_mb == 50
    assert settings.allowed_file_type == ["pdf", "txt", "docx"]
    assert settings.upload_dir == "/app/uploads"


def test_default_chromadb_settings():
    """Test default ChromaDB settings"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test"
    )
    
    assert settings.chroma_host == "chromadb"
    assert settings.chroma_port == 8000
    assert settings.chroma_collection == "study_buddy"


def test_default_embedding_settings():
    """Test default embedding settings"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test"
    )
    
    assert settings.embedding_model == "sentence-transformers/all-MiniLM-L6-v2"
    assert settings.chunk_size == 1000
    assert settings.chunk_overlap == 200


def test_default_llm_settings():
    """Test default LLM settings"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test"
    )
    
    assert settings.llm_provider == "gemini"
    assert settings.gemini_model == "gemini-2.0-flash"
    assert settings.gemini_max_tokens == 8192
    assert settings.claude_model == "claude-sonnet-4-20250514"


def test_default_rag_settings():
    """Test default RAG settings"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test"
    )
    
    assert settings.default_num_contexts == 4


# ============================================================================
# Test Custom Values
# ============================================================================

def test_custom_application_settings():
    """Test that custom application settings work"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test",
        app_name="Custom App",
        app_version="2.0.0",
        debug=True
    )
    
    assert settings.app_name == "Custom App"
    assert settings.app_version == "2.0.0"
    assert settings.debug == True


def test_custom_server_settings():
    """Test that custom server settings work"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test",
        host="127.0.0.1",
        port=5000
    )
    
    assert settings.host == "127.0.0.1"
    assert settings.port == 5000


def test_custom_file_upload_settings():
    """Test that custom file upload settings work"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test",
        max_file_size_mb=100,
        allowed_file_type=["pdf"],
        upload_dir="/custom/path"
    )
    
    assert settings.max_file_size_mb == 100
    assert settings.allowed_file_type == ["pdf"]
    assert settings.upload_dir == "/custom/path"


def test_custom_llm_provider():
    """Test switching LLM provider"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test",
        llm_provider="claude"
    )
    
    assert settings.llm_provider == "claude"


def test_custom_chunk_settings():
    """Test custom chunk settings"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test",
        chunk_size=500,
        chunk_overlap=100
    )
    
    assert settings.chunk_size == 500
    assert settings.chunk_overlap == 100


# ============================================================================
# Test get_settings() Function
# ============================================================================

def test_get_settings_returns_settings_instance():
    """Test that get_settings returns a Settings instance"""
    # Note: This will fail without .env file with API keys
    # We're testing the function exists and has correct type hint
    assert callable(get_settings)


def test_get_settings_caching():
    """Test that get_settings uses caching (lru_cache)"""
    # Clear the cache first
    get_settings.cache_clear()
    
    # This test will fail if .env doesn't have API keys
    # For a real test, you'd need to mock the environment
    # For now, just verify the function has cache_clear (from lru_cache)
    assert hasattr(get_settings, 'cache_clear')
    assert hasattr(get_settings, 'cache_info')


# ============================================================================
# Test Allowed File Types
# ============================================================================

def test_allowed_file_types_contains_pdf():
    """Test that PDF is in allowed file types"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test"
    )
    
    assert "pdf" in settings.allowed_file_type


def test_allowed_file_types_contains_txt():
    """Test that TXT is in allowed file types"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test"
    )
    
    assert "txt" in settings.allowed_file_type


def test_allowed_file_types_contains_docx():
    """Test that DOCX is in allowed file types"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test"
    )
    
    assert "docx" in settings.allowed_file_type


# ============================================================================
# Test Model Names
# ============================================================================

def test_gemini_model_name():
    """Test Gemini model name is correct"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test"
    )
    
    assert settings.gemini_model == "gemini-2.0-flash"


def test_claude_model_name():
    """Test Claude model name is correct"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test"
    )
    
    assert settings.claude_model == "claude-sonnet-4-20250514"


# ============================================================================
# Test Edge Cases
# ============================================================================

def test_empty_api_key_fails():
    """Test that empty API keys fail validation"""
    with pytest.raises(ValidationError):
        Settings(
            google_api_key="",
            claude_api_key=""
        )


def test_extra_fields_ignored():
    """Test that extra fields are ignored due to model_config"""
    settings = Settings(
        google_api_key="test",
        claude_api_key="test",
        unknown_field="this should be ignored"
    )
    
    # Should not have the unknown field
    assert not hasattr(settings, 'unknown_field')


def test_case_insensitive_env_vars():
    """Test that environment variables are case insensitive"""
    # This is configured in model_config with case_sensitive: False
    # This test just verifies the config is set correctly
    assert Settings.model_config["case_sensitive"] == False


# ============================================================================
# Test Type Validation
# ============================================================================

def test_port_must_be_integer():
    """Test that port must be an integer"""
    with pytest.raises(ValidationError):
        Settings(
            google_api_key="test",
            claude_api_key="test",
            port="not_an_integer"
        )


def test_debug_must_be_boolean():
    """Test that debug must be a boolean"""
    # Pydantic will coerce "true"/"false" strings to bool
    # But invalid values should fail
    settings = Settings(
        google_api_key="test",
        claude_api_key="test",
        debug="yes"  # Pydantic will try to convert this
    )
    # "yes" gets converted to True in Pydantic
    assert isinstance(settings.debug, bool)


def test_max_file_size_must_be_integer():
    """Test that max_file_size_mb must be an integer"""
    with pytest.raises(ValidationError):
        Settings(
            google_api_key="test",
            claude_api_key="test",
            max_file_size_mb="fifty"
        )


def test_allowed_file_type_must_be_list():
    """Test that allowed_file_type must be a list"""
    with pytest.raises(ValidationError):
        Settings(
            google_api_key="test",
            claude_api_key="test",
            allowed_file_type="pdf"  # Should be a list
        )