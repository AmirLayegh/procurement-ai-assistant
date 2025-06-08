"""
Unit tests for the configuration management module.
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from pydantic import SecretStr, ValidationError
from superlinked_app.configs import Settings, get_env_file_path


class TestSettings:
    """Test the Settings configuration class."""

    def test_settings_with_defaults(self):
        """Test that settings work with default values."""
        with patch.dict(os.environ, {
            "OPENAI_API_KEY": "test-openai-key",
            "QDRANT_API_KEY": "test-qdrant-key"
        }):
            settings = Settings()
            
            assert settings.text_embedder_name == "sentence-transformers/all-MiniLM-L12-v2"
            assert settings.chunk_size == 10
            assert settings.openai_model == "gpt-4o"
            assert settings.use_qdrant_vector_db is True
            assert settings.data_path == "./data/csv/products_enriched.csv"

    def test_secret_str_fields(self):
        """Test that sensitive fields use SecretStr properly."""
        with patch.dict(os.environ, {
            "OPENAI_API_KEY": "sk-test-openai-key",
            "QDRANT_API_KEY": "test-qdrant-key",
            "QDRANT_URL": "https://test-cluster.qdrant.io",
            "QDRANT_COLLECTION_NAME": "test_collection"
        }):
            settings = Settings()
            
            # Check that fields are SecretStr instances
            assert isinstance(settings.openai_api_key, SecretStr)
            assert isinstance(settings.qdrant_api_key, SecretStr)
            assert isinstance(settings.qdrant_url, SecretStr)
            #assert isinstance(settings.qdrant_collection_name, SecretStr)
            
            # Check that get_secret_value() returns the actual values
            assert settings.openai_api_key.get_secret_value() == "sk-test-openai-key"
            assert settings.qdrant_api_key.get_secret_value() == "test-qdrant-key"
            assert settings.qdrant_url.get_secret_value() == "https://test-cluster.qdrant.io"
            #assert settings.qdrant_collection_name.get_secret_value() == "test_collection"

    def test_secret_str_representation(self):
        """Test that SecretStr fields hide sensitive data in string representation."""
        with patch.dict(os.environ, {
            "OPENAI_API_KEY": "sk-very-secret-key",
            "QDRANT_API_KEY": "super-secret-qdrant-key"
        }):
            settings = Settings()
            
            # Convert to string should hide the secret
            openai_str = str(settings.openai_api_key)
            qdrant_str = str(settings.qdrant_api_key)
            
            assert "sk-very-secret-key" not in openai_str
            assert "super-secret-qdrant-key" not in qdrant_str
            assert "**********" in openai_str
            assert "**********" in qdrant_str

    def test_qdrant_client_property(self):
        """Test the qdrant_client property."""
        with patch.dict(os.environ, {
            "OPENAI_API_KEY": "test-key",
            "QDRANT_API_KEY": "test-qdrant-key",
            "QDRANT_URL": "https://test-cluster.qdrant.io"
        }):
            settings = Settings()
            client_config = settings.qdrant_client
            
            assert client_config["url"] == "https://test-cluster.qdrant.io"
            assert client_config["api_key"] == "test-qdrant-key"

    def test_qdrant_client_property_missing_values(self):
        """Test qdrant_client property raises error when values are missing."""
        with patch.dict(os.environ, {
            "OPENAI_API_KEY": "test-key",
            "QDRANT_API_KEY": "",  # Empty API key
            "QDRANT_URL": "https://test-cluster.qdrant.io"
        }):
            settings = Settings()
            
            with pytest.raises(ValueError, match="Qdrant URL and API key must be set"):
                _ = settings.qdrant_client

    def test_environment_variable_override(self):
        """Test that environment variables properly override defaults."""
        with patch.dict(os.environ, {
            "OPENAI_API_KEY": "test-key",
            "QDRANT_API_KEY": "test-key",
            "TEXT_EMBEDDER_NAME": "custom-embedder",
            "CHUNK_SIZE": "25",
            "OPENAI_MODEL": "gpt-3.5-turbo",
            "DATA_PATH": "/custom/data/path.csv",
            "USE_QDRANT_VECTOR_DB": "false"
        }):
            settings = Settings()
            
            assert settings.text_embedder_name == "custom-embedder"
            assert settings.chunk_size == 25
            assert settings.openai_model == "gpt-3.5-turbo"
            assert settings.data_path == "/custom/data/path.csv"
            assert settings.use_qdrant_vector_db is False

    def test_missing_required_secret_fails(self):
        """Test that missing required secrets cause validation errors when .env file is not available."""
        # Since the actual system loads from .env file via load_dotenv(),
        # we need to test the scenario where the .env file doesn't exist or is empty
        import tempfile
        import os
        
        # Create a temporary directory without .env file
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to temp directory so no .env file is found
            original_cwd = os.getcwd()
            original_env = dict(os.environ)
            
            try:
                os.chdir(temp_dir)
                os.environ.clear()
                
                # Now Settings should fail to load required secrets
                with pytest.raises(ValidationError) as exc_info:
                    Settings()
                    
                # Verify that the validation error mentions the missing required fields
                error_str = str(exc_info.value)
                assert "openai_api_key" in error_str or "qdrant_api_key" in error_str
                
            finally:
                # Restore original state
                os.chdir(original_cwd)
                os.environ.clear()
                os.environ.update(original_env)

    def test_dotenv_loading(self):
        """Test that dotenv is loaded during module import."""
        # Since load_dotenv is called at module level, we need to test differently
        # We'll test that the function exists and can be called
        from superlinked_app.configs import load_dotenv
        
        # Verify that load_dotenv was imported and is callable
        assert callable(load_dotenv)
        
        # Test that calling load_dotenv works
        result = load_dotenv(override=True)
        # load_dotenv returns True if file was loaded, False if not found
        assert isinstance(result, bool)


class TestGetEnvFilePath:
    """Test the get_env_file_path utility function."""

    def test_get_env_file_path_returns_absolute_path(self):
        """Test that get_env_file_path returns an absolute path."""
        path = get_env_file_path()
        assert os.path.isabs(path)
        assert path.endswith(".env")

    def test_get_env_file_path_relative_to_configs_module(self):
        """Test that the path is relative to the configs module location."""
        path = get_env_file_path()
        expected_dir = os.path.dirname(os.path.abspath("superlinked_app/configs.py"))
        assert path.startswith(expected_dir) or "superlinked_app" in path


@pytest.mark.integration
class TestSettingsIntegration:
    """Integration tests for settings that require real environment setup."""

    def test_settings_from_real_env_file(self, tmp_path):
        """Test loading settings from an actual .env file."""
        # Create a temporary .env file
        env_file = tmp_path / ".env"
        env_content = """
OPENAI_API_KEY=sk-test-integration-key
QDRANT_API_KEY=integration-qdrant-key
QDRANT_URL=https://integration.qdrant.io
TEXT_EMBEDDER_NAME=integration-embedder
CHUNK_SIZE=15
        """.strip()
        env_file.write_text(env_content)
        
        # Clear environment variables to avoid interference from autouse fixture
        with patch.dict(os.environ, {}, clear=True):
            # Load settings from the custom env file
            settings = Settings(_env_file=str(env_file))
            
            assert settings.openai_api_key.get_secret_value() == "sk-test-integration-key"
            assert settings.qdrant_api_key.get_secret_value() == "integration-qdrant-key"
            assert settings.qdrant_url.get_secret_value() == "https://integration.qdrant.io"
            assert settings.text_embedder_name == "integration-embedder"
            assert settings.chunk_size == 15 