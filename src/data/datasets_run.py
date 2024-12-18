import os
import importlib
import sys

def run_module(module_name):
    """Run a Python module by importing and executing it"""
    try:
        module = importlib.import_module(module_name)
        print(f"\nExecuting {module_name}...")
        if hasattr(module, 'main'):
            module.main()
    except Exception as e:
        print(f"Error executing {module_name}: {str(e)}")
        sys.exit(1)

def main():
    # Ensure we're in the project root directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    # Run each step in sequence
    steps = [
        'src.data.heic2jpg',           # Convert HEIC to JPG
        'src.data.datasets_dt',        # Run face detection
        'src.data.filter_null',        # Remove undetected faces and rename
        'src.data.datasets_upload'     # Upload to Kaggle
    ]
    
    for step in steps:
        run_module(step)
        print(f"\nCompleted {step}")
        
    print("\nAll steps completed successfully!")

if __name__ == '__main__':
    main()