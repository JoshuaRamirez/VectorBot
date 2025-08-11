#!/usr/bin/env python3
"""Smoke test script to verify Vector Bot works without disk access."""

import argparse
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from rich.console import Console

from rag.config import load_config
from rag.ollama_check import check_server, choose_chat_model, ensure_embed_model, list_local_models

console = Console()


def run_smoke_test(env_name=None):
    """Run a simple smoke test with in-memory documents."""
    console.print("[bold]Vector Bot Smoke Test[/bold]\n")
    
    # Load config
    if env_name:
        console.print(f"[dim]Using environment: {env_name}[/dim]\n")
    config = load_config(env_name)
    base_url = config["OLLAMA_BASE_URL"]
    
    # Check Ollama server
    console.print("Checking Ollama server...")
    if not check_server(base_url):
        console.print("[red]✗ Ollama server not running[/red]")
        console.print("Start it with: ollama serve")
        sys.exit(1)
    console.print("[green]OK Ollama server is running[/green]")
    
    # Get models
    models = list_local_models(base_url)
    if not models:
        console.print("[red]ERROR No models installed[/red]")
        sys.exit(1)
    
    # Choose chat model
    chat_model = choose_chat_model(config["OLLAMA_CHAT_MODEL"], models)
    if not chat_model:
        console.print("[red]ERROR No suitable chat model found[/red]")
        sys.exit(1)
    console.print(f"[green]OK Using chat model: {chat_model}[/green]")
    
    # Check embedding model
    embed_model = config["OLLAMA_EMBED_MODEL"]
    embed_ok, embed_msg = ensure_embed_model(base_url, embed_model)
    if not embed_ok:
        console.print(f"[red]ERROR {embed_msg}[/red]")
        sys.exit(1)
    console.print(f"[green]OK Using embedding model: {embed_model}[/green]")
    
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
    
    # Create test documents
    console.print("\n[blue]Creating in-memory test documents...[/blue]")
    docs = [
        Document(
            text="""
            Project Approval Process:
            The approval steps for new projects are as follows:
            1. Initial proposal submission by project lead
            2. Technical review by the architecture team
            3. Budget approval from finance department
            4. Final sign-off from executive committee
            5. Project kickoff meeting with all stakeholders
            
            Each step typically takes 3-5 business days to complete.
            """,
            metadata={"source": "process_guide.txt"},
        ),
        Document(
            text="""
            Technical Requirements:
            All new projects must meet these technical standards:
            - Code must pass automated testing with 80% coverage
            - Security review must be completed
            - Documentation must be provided
            - Performance benchmarks must be met
            """,
            metadata={"source": "tech_requirements.txt"},
        ),
    ]
    
    # Build index
    console.print("[blue]Building in-memory vector index...[/blue]")
    index = VectorStoreIndex.from_documents(docs)
    
    # Create query engine
    query_engine = index.as_query_engine(similarity_top_k=2)
    
    # Test query
    test_question = "What are the approval steps?"
    console.print(f"\n[bold]Test Question:[/bold] {test_question}")
    
    try:
        response = query_engine.query(test_question)
        answer = str(response).strip()
        
        if answer and answer != "Empty Response":
            console.print(f"[bold]Answer:[/bold] {answer}")
            console.print("\n[green]SUCCESS Smoke test passed![/green]")
            return 0
        else:
            console.print("[red]ERROR No answer generated[/red]")
            return 1
    except Exception as e:
        console.print(f"[red]ERROR Query failed: {e}[/red]")
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vector Bot Smoke Test")
    parser.add_argument(
        "--env",
        help="Environment configuration to use (development, production, docker)",
        default=None,
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show verbose output",
    )
    
    args = parser.parse_args()
    
    # Set verbose mode if requested
    if args.verbose:
        os.environ["RAG_VERBOSE"] = "true"
    
    sys.exit(run_smoke_test(args.env))