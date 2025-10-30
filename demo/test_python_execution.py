#!/usr/bin/env python3
"""
Test script to simulate what the Java controller does
"""
import subprocess
import sys
import os

def test_python_script():
    try:
        # Debug information
        print("=== DEBUG INFORMATION ===")
        print(f"Python executable: {sys.executable}")
        print(f"Python version: {sys.version}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Script file location: {__file__}")
        print(f"Script directory: {os.path.dirname(__file__)}")
        
        # Test different path approaches
        script_dir = os.path.dirname(__file__)
        absolute_path = os.path.join(script_dir, "src", "main", "java", "com", "example", "demo", "test.py")
        relative_path = "src/main/java/com/example/demo/test.py"
        
        print(f"\nAbsolute path: {absolute_path}")
        print(f"Absolute path exists: {os.path.exists(absolute_path)}")
        print(f"Relative path: {relative_path}")
        print(f"Relative path exists: {os.path.exists(relative_path)}")
        
        # Try to find the test.py file
        possible_paths = [
            absolute_path,
            relative_path,
            os.path.join(os.getcwd(), "src", "main", "java", "com", "example", "demo", "test.py"),
        ]
        
        working_path = None
        for path in possible_paths:
            if os.path.exists(path):
                working_path = path
                print(f"✓ Found working path: {path}")
                break
        
        if not working_path:
            print("✗ Could not find test.py file in any expected location!")
            print("Available files in current directory:")
            for item in os.listdir("."):
                print(f"  - {item}")
            return
        
        print("\n" + "=" * 50)
        print("RUNNING PYTHON SCRIPT:")
        
        # Run the Python script
        result = subprocess.run(
            ["python", working_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"Exit code: {result.returncode}")
        if result.returncode == 0:
            print("SUCCESS!")
            # Show just the summary
            if "Document Name:" in result.stdout:
                lines = result.stdout.split('\n')
                for line in lines[-5:]:  # Show last 5 lines
                    if line.strip():
                        print(line)
        else:
            print("ERROR:")
            print(f"stdout: {result.stdout}")
            print(f"stderr: {result.stderr}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_python_script()