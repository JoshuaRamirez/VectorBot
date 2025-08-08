"""Command-line interface for the RAG application."""

import argparse
import sys
from typing import Optional

from rich.console import Console

from .ingest import ingest
from .ollama_check import doctor
from .query import query
from .version import __version__

console = Console()


def main(argv: Optional[list] = None) -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="rag",
        description="Local RAG pipeline using LlamaIndex with Ollama",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        required=True,
    )
    
    # Doctor command
    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Check Ollama server health and available models",
    )
    doctor_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output",
    )
    
    # Ingest command
    ingest_parser = subparsers.add_parser(
        "ingest",
        help="Ingest documents and build/update the vector index",
    )
    ingest_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed progress",
    )
    
    # Query command
    query_parser = subparsers.add_parser(
        "query",
        help="Query the index with a question",
    )
    query_parser.add_argument(
        "question",
        help="The question to ask",
    )
    query_parser.add_argument(
        "--k",
        type=int,
        default=None,
        help="Number of similar chunks to retrieve",
    )
    query_parser.add_argument(
        "--show-sources",
        action="store_true",
        help="Show source documents used for the answer",
    )
    query_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output",
    )
    
    # Parse arguments
    args = parser.parse_args(argv)
    
    try:
        if args.command == "doctor":
            doctor(verbose=args.verbose)
        elif args.command == "ingest":
            ingest(verbose=args.verbose)
        elif args.command == "query":
            query(
                question=args.question,
                similarity_top_k=args.k,
                show_sources=args.show_sources,
                verbose=args.verbose,
            )
        return 0
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        return 130
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1


if __name__ == "__main__":
    sys.exit(main())