import os, boto3
from typing import Dict, Any
from sqlalchemy import make_url
from llama_index.core.settings import Settings
from llama_index.core import StorageContext
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.postgres import PGVectorStore

def llm_config_from_env() -> Dict:
    from llama_index.core.constants import DEFAULT_TEMPERATURE

    model = os.getenv("MODEL")
    temperature = os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE)

    config = {
        "model": model,
        "temperature": float(temperature),
        "request_timeout": 30.0,
        "base_url": "http://ollama:11434",
    }
    return config

def embedding_config_from_env() -> Dict:
    model_name = os.getenv("EMBED")
    embed_batch_size = int(os.getenv("BATCH_SIZE", "10"))

    config = {
        "model_name": model_name,
        "embed_batch_size": embed_batch_size,
        "base_url": "http://ollama:11434",
    }
    return config

def vector_config_from_env() -> Dict:
    db_config = os.getenv("DB_CFG")
    embed_dim = os.getenv("VECTOR_SIZE")

    url = make_url(db_config)

    config = {
        "database": url.database,
        "host": url.host,
        "password": url.password,
        "port": url.port,
        "user": url.username,
        "table_name": "default",
        "embed_dim": embed_dim,
    }
    return config

def boto3_config_from_env() -> Dict:
    aws_access_key_id = os.getenv("S3_ACCESS_KEY")
    aws_secret_access_key = os.getenv("S3_SECRET_KEY")
    region_name = os.getenv("S3_REGION")
    endpoint_url = os.getenv("S3_ENDPOINT")

    config = {
        "service_name": "s3",
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "region_name": region_name,
        "endpoint_url": endpoint_url,
    }
    return config

def init_settings():
    llm_configs = llm_config_from_env()
    embed_configs = embedding_config_from_env()

    Settings.llm = Ollama(**llm_configs)
    Settings.embed_model = OllamaEmbedding(**embed_configs)
    Settings.chunk_size = int(os.getenv("CHUNK_SIZE", "1024"))
    Settings.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "20"))

def get_storage_context() -> Any:
    vector_configs = vector_config_from_env()
   
    vector_store = PGVectorStore.from_params(**vector_configs)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    return storage_context

def get_boto3_client() -> Any:
    boto3_configs = boto3_config_from_env()
    
    client = boto3.Session().client(**boto3_configs)

    return client


