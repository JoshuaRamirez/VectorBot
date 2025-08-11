#!/usr/bin/env python3
"""Build script to create executable from the RAG CLI."""

import importlib.util
import subprocess
import sys
from pathlib import Path

def build_executable():
    """Build executable using PyInstaller."""
    
    # Install PyInstaller if not available
    if importlib.util.find_spec("PyInstaller") is None:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=False)
    
    # Create a simple entry point script
    entry_script = Path("rag_main.py")
    entry_script.write_text("""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import and run the main CLI
from rag.cli import main

if __name__ == "__main__":
    sys.exit(main())
""")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "rag",
        "--add-data", "src/rag;rag",
        "--add-data", "configs;configs",
        "--add-data", ".env.example;.",
        "--hidden-import", "llama_index.core",
        "--hidden-import", "llama_index.llms.ollama", 
        "--hidden-import", "llama_index.embeddings.ollama",
        "--hidden-import", "ollama",
        "--hidden-import", "requests",
        "--hidden-import", "rich",
        "--hidden-import", "dotenv",
        "--paths", "src",
        "--clean",
        str(entry_script)
    ]
    
    print("Building executable...")
    print(f"Command: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        executable_path = Path("dist") / ("rag.exe" if sys.platform == "win32" else "rag")
        print(f"OK Executable built successfully: {executable_path}")
        print(f"Size: {executable_path.stat().st_size / (1024*1024):.1f} MB")
        print("\nTo distribute:")
        print(f"1. Copy {executable_path} to target system")
        print("2. Ensure Ollama is installed and running on target system")
        print("3. Run: ./rag doctor")
        
        # Clean up entry script
        entry_script.unlink(missing_ok=True)
    else:
        print("ERROR Build failed:")
        print(result.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(build_executable())