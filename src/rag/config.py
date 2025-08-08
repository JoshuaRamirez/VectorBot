"""Configuration management for the RAG application."""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from rich.console import Console

console = Console()


def get_executable_dir() -> Path:
    """Get the directory where the executable/script is located."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        return Path(sys.executable).parent
    else:
        # Running as Python script
        return Path(__file__).parent.parent.parent


def load_environment_config(env_name: Optional[str] = None) -> None:
    """Load environment-specific configuration."""
    executable_dir = get_executable_dir()
    
    # Priority order for loading .env files:
    env_files = []
    
    if env_name:
        # 1. Specific environment config
        env_files.append(executable_dir / f"configs/{env_name}.env")
        env_files.append(Path(f"configs/{env_name}.env"))
        env_files.append(Path(f".env.{env_name}"))
    
    # 2. Environment-specific from RAG_ENV variable
    rag_env = os.getenv("RAG_ENV")
    if rag_env:
        env_files.extend([
            executable_dir / f"configs/{rag_env}.env",
            Path(f"configs/{rag_env}.env"),
            Path(f".env.{rag_env}")
        ])
    
    # 3. Local .env file
    env_files.extend([
        executable_dir / ".env",
        Path(".env")
    ])
    
    # 4. Default development config
    env_files.extend([
        executable_dir / "configs/development.env",
        Path("configs/development.env")
    ])
    
    # Load the first existing file
    for env_file in env_files:
        if env_file.exists():
            # Use override=False to preserve existing environment variables
            load_dotenv(env_file, override=False)
            if os.getenv("RAG_VERBOSE") == "true":
                console.print(f"[dim]Loaded config from: {env_file}[/dim]")
            break


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration values."""
    errors = []
    
    # Validate required directories exist or can be created
    for dir_key in ["DOCS_DIR", "INDEX_DIR"]:
        dir_path = config[dir_key]
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"{dir_key}: Cannot create directory {dir_path}: {e}")
    
    # Validate URL format
    url = config["OLLAMA_BASE_URL"]
    if not url.startswith(("http://", "https://")):
        errors.append(f"OLLAMA_BASE_URL must start with http:// or https://, got: {url}")
    
    # Validate numeric values
    try:
        int(config["SIMILARITY_TOP_K"])
    except ValueError:
        errors.append(f"SIMILARITY_TOP_K must be an integer, got: {config['SIMILARITY_TOP_K']}")
    
    if errors:
        console.print("[red]Configuration validation errors:[/red]")
        for error in errors:
            console.print(f"  [red]- {error}[/red]")
        return False
    
    return True


def load_config(env_name: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from environment variables and .env files."""
    # Load environment-specific config
    load_environment_config(env_name)
    
    # Get executable directory for resolving relative paths
    executable_dir = get_executable_dir()
    
    def resolve_path(path_str: str, base_dir: Path = None) -> Path:
        """Resolve a path relative to executable directory."""
        path = Path(path_str)
        if path.is_absolute():
            return path
        
        # Always resolve relative to executable directory
        return (executable_dir / path).resolve()
    
    # Build configuration
    config = {
        "DOCS_DIR": resolve_path(os.getenv("DOCS_DIR", "./docs")),
        "INDEX_DIR": resolve_path(os.getenv("INDEX_DIR", "./index_storage")),
        "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        "OLLAMA_CHAT_MODEL": os.getenv("OLLAMA_CHAT_MODEL"),
        "OLLAMA_EMBED_MODEL": os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text"),
        "SIMILARITY_TOP_K": int(os.getenv("SIMILARITY_TOP_K", "4")),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
        "ENABLE_VERBOSE_OUTPUT": os.getenv("ENABLE_VERBOSE_OUTPUT", "false").lower() == "true",
        "REQUEST_TIMEOUT": float(os.getenv("REQUEST_TIMEOUT", "60.0")),
        "EMBED_BATCH_SIZE": int(os.getenv("EMBED_BATCH_SIZE", "10")),
    }
    
    # Validate configuration
    if not validate_config(config):
        raise ValueError("Configuration validation failed")
    
    return config


def get_config_value(key: str, default: Optional[str] = None, env_name: Optional[str] = None) -> Optional[str]:
    """Get a specific configuration value."""
    config = load_config(env_name)
    return config.get(key, default)