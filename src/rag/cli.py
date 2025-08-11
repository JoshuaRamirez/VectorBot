"""Command-line interface for Vector Bot."""

import argparse
import sys
from typing import Any, List, Optional

from rich.console import Console

from .ingest import ingest
from .ollama_check import doctor
from .query import query
from .version import __version__

console = Console()


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="vector-bot",
        description="Vector Bot: Local RAG pipeline using LlamaIndex with Ollama",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--env",
        help="Environment configuration to use (development, production, docker)",
        default=None,
    )
    parser.add_argument(
        "--config-info",
        action="store_true",
        help="Show configuration information and exit",
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        required=False,
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
        # Handle config info request
        if args.config_info:
            from pathlib import Path
            from .config import load_config, get_executable_dir
            
            config = load_config(args.env)
            executable_dir = get_executable_dir()
            
            console.print("[bold]Configuration Information:[/bold]")
            console.print(f"Executable directory: {executable_dir}")
            console.print(f"Environment: {args.env or 'auto-detected'}")
            console.print("\n[bold]Current configuration:[/bold]")
            
            for key, value in config.items():
                if isinstance(value, Path):
                    console.print(f"  {key}: {value} ({'exists' if value.exists() else 'will be created'})")
                else:
                    console.print(f"  {key}: {value}")
            
            return 0
        
        # Ensure command is provided if not using config-info
        if not args.command and not args.config_info:
            parser.print_help()
            return 1
        
        # Execute commands with environment config
        if args.command == "doctor":
            doctor(verbose=args.verbose, env_name=args.env)
        elif args.command == "ingest":
            ingest(verbose=args.verbose, env_name=args.env)
        elif args.command == "query":
            query(
                question=args.question,
                similarity_top_k=args.k,
                show_sources=args.show_sources,
                verbose=args.verbose,
                env_name=args.env,
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