from pathlib import Path
import shutil

def setup_directories():
    # Get the base directory
    base_dir = Path(__file__).resolve().parent
    
    # Create uploads directory
    uploads_dir = base_dir / "uploads"
    uploads_dir.mkdir(exist_ok=True)
    
    print("Directory structure is set up correctly!")
    print(f"Uploads directory: {uploads_dir}")
    return True

if __name__ == "__main__":
    setup_directories() 