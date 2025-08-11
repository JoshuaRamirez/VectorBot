"""Document ingestion module for building and persisting vector index."""

from pathlib import Path
from typing import List, Optional

from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from rich.console import Console

from .config import load_config
from .ollama_check import check_server, choose_chat_model, ensure_embed_model, list_local_models

console = Console()


def setup_llm_settings(config: dict) -> None:
    """Configure LlamaIndex settings with Ollama models."""
    base_url = config["OLLAMA_BASE_URL"]
    
    # Check server
    if not check_server(base_url):
        raise RuntimeError(f"Ollama server not running at {base_url}")
    
    # Get available models
    models = list_local_models(base_url)
    if not models:
        raise RuntimeError("No models installed. Run: ollama pull llama3.1")
    
    # Choose chat model
    chat_model = choose_chat_model(config["OLLAMA_CHAT_MODEL"], models)
    if not chat_model:
        raise RuntimeError("No suitable chat model found. Install one with: ollama pull llama3.1")
    
    # Check embedding model
    embed_model = config["OLLAMA_EMBED_MODEL"]
    embed_ok, embed_msg = ensure_embed_model(base_url, embed_model)
    if not embed_ok:
        console.print(f"[yellow]{embed_msg}[/yellow]")
        raise RuntimeError(embed_msg)
    
    # Configure Settings
    Settings.llm = Ollama(
        model=chat_model,
        base_url=base_url,
        temperature=0,
        request_timeout=config.get("REQUEST_TIMEOUT", 60.0),
    )
    
    Settings.embed_model = OllamaEmbedding(
        model_name=embed_model,
        base_url=base_url,
        embed_batch_size=config.get("EMBED_BATCH_SIZE", 10),
    )
    
    console.print(f"[green]Using chat model: {chat_model}[/green]")
    console.print(f"[green]Using embedding model: {embed_model}[/green]")


def load_documents(docs_dir: Path) -> List:
    """Load documents from the specified directory."""
    if not docs_dir.exists():
        docs_dir.mkdir(parents=True, exist_ok=True)
        console.print(f"[yellow]Created docs directory: {docs_dir}[/yellow]")
        return []
    
    # Define file extensions to load
    extensions = [".txt", ".md", ".pdf", ".json", ".csv"]
    
    # Check for documents
    doc_files: list[Path] = []
    for ext in extensions:
        doc_files.extend(docs_dir.glob(f"*{ext}"))
        doc_files.extend(docs_dir.glob(f"**/*{ext}"))
    
    if not doc_files:
        console.print(f"[yellow]No documents found in {docs_dir}[/yellow]")
        return []
    
    # Filter out large files (>20MB)
    valid_files: list[Path] = []
    for file in doc_files:
        size_mb = file.stat().st_size / (1024 * 1024)
        if size_mb > 20:
            console.print(f"[yellow]Skipping large file (>{size_mb:.1f}MB): {file.name}[/yellow]")
        else:
            valid_files.append(file)
    
    if not valid_files:
        console.print("[yellow]No valid documents to index[/yellow]")
        return []
    
    console.print(f"[blue]Loading {len(valid_files)} documents...[/blue]")
    
    # Load documents
    reader = SimpleDirectoryReader(
        input_dir=str(docs_dir),
        recursive=True,
        exclude_hidden=True,
        required_exts=extensions,
    )
    
    documents = reader.load_data()
    console.print(f"[green]Loaded {len(documents)} document chunks[/green]")
    
    return documents


def ingest(verbose: bool = False, env_name: Optional[str] = None) -> None:
    """Run document ingestion to build or update the vector index."""
    config = load_config(env_name)
    docs_dir = config["DOCS_DIR"]
    index_dir = config["INDEX_DIR"]
    
    console.print("[bold]Document Ingestion[/bold]")
    
    # Setup LLM settings
    setup_llm_settings(config)
    
    # Check if index already exists
    if index_dir.exists() and (index_dir / "docstore.json").exists():
        console.print(f"[blue]Loading existing index from {index_dir}[/blue]")
        try:
            storage_context = StorageContext.from_defaults(persist_dir=str(index_dir))
            index = load_index_from_storage(storage_context)
            console.print("[green]OK Existing index loaded successfully[/green]")
            return
        except Exception as e:
            console.print(f"[yellow]Could not load existing index: {e}[/yellow]")
            console.print("[blue]Creating new index...[/blue]")
    
    # Load documents
    documents = load_documents(docs_dir)
    if not documents:
        raise RuntimeError(f"No documents found in {docs_dir}")
    
    # Build index
    console.print("[blue]Building vector index...[/blue]")
    index = VectorStoreIndex.from_documents(
        documents,
        show_progress=verbose,
    )
    
    # Persist index
    index_dir.mkdir(parents=True, exist_ok=True)
    index.storage_context.persist(persist_dir=str(index_dir))
    console.print(f"[green]OK Index saved to {index_dir}[/green]")
    console.print(f"[green]OK Indexed {len(documents)} chunks[/green]")