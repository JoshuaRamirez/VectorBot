"""Query module for answering questions using the vector index."""
from typing import Optional

from llama_index.core import StorageContext, load_index_from_storage
from rich.console import Console

from .config import load_config
from .ingest import setup_llm_settings

console = Console()


def ask(
    question: str,
    similarity_top_k: Optional[int] = None,
    show_sources: bool = False,
    verbose: bool = False,
    env_name: Optional[str] = None,
) -> str:
    """Query the index with a question and return the answer."""
    config = load_config(env_name)
    index_dir = config["INDEX_DIR"]
    
    if similarity_top_k is None:
        similarity_top_k = config["SIMILARITY_TOP_K"]
    
    # Check if index exists
    if not index_dir.exists() or not (index_dir / "docstore.json").exists():
        raise RuntimeError(
            f"No index found at {index_dir}. Run 'rag ingest' first to build the index."
        )
    
    # Setup LLM settings
    setup_llm_settings(config)
    
    # Load index
    if verbose:
        console.print(f"[blue]Loading index from {index_dir}...[/blue]")
    
    storage_context = StorageContext.from_defaults(persist_dir=str(index_dir))
    index = load_index_from_storage(storage_context)
    
    # Create query engine
    query_engine = index.as_query_engine(
        similarity_top_k=similarity_top_k,
        streaming=False,
    )
    
    # Execute query
    if verbose:
        console.print(f"[blue]Querying with top_k={similarity_top_k}...[/blue]")
    
    response = query_engine.query(question)
    
    # Process response
    answer = str(response).strip()
    
    if not answer or answer == "Empty Response":
        answer = "No relevant information found in the indexed documents."
    
    # Show sources if requested
    if show_sources and hasattr(response, "source_nodes"):
        source_info = []
        for node in response.source_nodes:
            if hasattr(node, "metadata"):
                filename = node.metadata.get("file_name", "Unknown")
                score = node.score if hasattr(node, "score") else 0
                source_info.append(f"  - {filename} (score: {score:.3f})")
        
        if source_info:
            answer += "\n\n[dim]Sources:[/dim]\n" + "\n".join(source_info)
    
    return answer


def query(
    question: str,
    similarity_top_k: Optional[int] = None,
    show_sources: bool = False,
    verbose: bool = False,
    env_name: Optional[str] = None,
) -> None:
    """Run a query and print the result."""
    try:
        answer = ask(question, similarity_top_k, show_sources, verbose, env_name)
        console.print(f"\n[bold]Answer:[/bold] {answer}")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise