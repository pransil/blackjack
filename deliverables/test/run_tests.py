#!/usr/bin/env python3
"""
Simple test runner with timestamped output files.
Runs pytest and saves results with timestamp: test_results_YYYY-MM-DD-HH:MM.txt
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

def run_tests():
    """Run pytest with timestamped output file."""
    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M")
    
    # Create reports directory if it doesn't exist
    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Generate output filename with timestamp
    output_file = reports_dir / f"test_results_{timestamp}.txt"
    
    # Run pytest with verbose output
    cmd = [sys.executable, "-m", "pytest", "test/", "-v"]
    
    print(f"Running tests and saving results to: {output_file}")
    
    try:
        # Run tests and capture output
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=Path(__file__).parent.parent
        )
        
        # Write output to timestamped file
        output_file.write_text(result.stdout + result.stderr)
        
        # Print output to console
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        print(f"\nTest results saved to: {output_file}")
        return result.returncode
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())