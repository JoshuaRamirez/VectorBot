"""Configuration management for the RAG application."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def load_config() -> dict:
    """Load configuration from environment variables and .env file."""
    load_dotenv()
    
    config = {
        "DOCS_DIR": Path(os.getenv("DOCS_DIR", "./docs")).resolve(),
        "INDEX_DIR": Path(os.getenv("INDEX_DIR", "./index_storage")).resolve(),
        "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        "OLLAMA_CHAT_MODEL": os.getenv("OLLAMA_CHAT_MODEL"),
        "OLLAMA_EMBED_MODEL": os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text"),
        "SIMILARITY_TOP_K": int(os.getenv("SIMILARITY_TOP_K", "4")),
    }
    
    return config


def get_config_value(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get a specific configuration value."""
    config = load_config()
    return config.get(key, default)