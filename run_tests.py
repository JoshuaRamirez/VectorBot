#!/usr/bin/env python3
"""Test runner script for the Local Ollama RAG project."""

import sys
import subprocess
from pathlib import Path


def run_command(cmd, description):
    """Run a command and display results."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0


def main():
    """Main test runner."""
    project_root = Path(__file__).parent
    
    # Change to project directory
    import os
    os.chdir(project_root)
    
    success = True
    
    # Run unit tests
    if not run_command([
        sys.executable, "-m", "pytest", 
        "tests/unit/", 
        "-v", 
        "--tb=short"
    ], "Unit Tests"):
        success = False
    
    # Run integration tests (may be skipped if dependencies missing)
    if not run_command([
        sys.executable, "-m", "pytest", 
        "tests/integration/", 
        "-v", 
        "--tb=short"
    ], "Integration Tests"):
        print("\nNote: Integration tests may have been skipped due to missing dependencies")
    
    # Run tests with coverage if coverage is available
    try:
        subprocess.run([sys.executable, "-c", "import coverage"], 
                      check=True, capture_output=True)
        
        run_command([
            sys.executable, "-m", "pytest", 
            "tests/unit/",
            "--cov=rag",
            "--cov-report=term-missing",
            "--cov-report=html"
        ], "Unit Tests with Coverage")
        
        print("\nCoverage report generated in htmlcov/index.html")
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\nCoverage not available. Install with: pip install pytest-cov")
    
    # Summary
    print(f"\n{'='*60}")
    if success:
        print("✅ Test run completed successfully!")
    else:
        print("❌ Some tests failed. See output above for details.")
    print(f"{'='*60}")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())