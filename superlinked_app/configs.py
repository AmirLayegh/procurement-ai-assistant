# procurement/configs.py
import os
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv(override=True)

DEFAULT_ENV_FILENAME = ".env"

class Settings(BaseSettings):
    
    text_embedder_name: str = "sentence-transformers/all-MiniLM-L12-v2" 
    chunk_size: int = 10
    openai_model: str = "gpt-4o" 
        
    openai_api_key: SecretStr
    qdrant_api_key: SecretStr
    qdrant_url: SecretStr 
    qdrant_collection_name: str = os.environ.get("QDRANT_COLLECTION_NAME")
    

    data_path: str = "./data/csv/products_enriched.csv"  
    use_qdrant_vector_db: bool = True
    
    model_config = SettingsConfigDict(
        env_file=DEFAULT_ENV_FILENAME, 
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore extra environment variables
    )
    
    @property
    def qdrant_client(self) -> dict:
        if self.qdrant_url and self.qdrant_api_key:
            return {
                "url": self.qdrant_url.get_secret_value(),  
                "api_key": self.qdrant_api_key.get_secret_value()  
            }
        else:
            raise ValueError("Qdrant URL and API key must be set")

def get_env_file_path() -> str:
    dirname = os.path.dirname(__file__)
    rel_path = os.path.join(dirname, DEFAULT_ENV_FILENAME)
    abs_path = os.path.abspath(rel_path)
    return abs_path

settings = Settings(_env_file=get_env_file_path())