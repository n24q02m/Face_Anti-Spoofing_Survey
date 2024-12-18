import os
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener
from tqdm import tqdm
import multiprocessing as mp
from functools import partial

# Register HEIF/HEIC opener
register_heif_opener()

def convert_single_file(heic_path):
    """Convert single HEIC file to JPG"""
    try:
        # Open HEIC file
        img = Image.open(str(heic_path))
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Save as JPG with same name
        jpg_path = heic_path.with_suffix('.jpg')
        img.save(jpg_path, 'JPEG', quality=95)
        
        # Remove original HEIC file after successful conversion
        heic_path.unlink()
        return True
        
    except Exception as e:
        print(f"Error converting {heic_path}: {str(e)}")
        return False

def convert_heic_to_jpg(dataset_path):
    """Convert all HEIC images in dataset to JPG format"""
    print("\nConverting HEIC images to JPG...")
    dataset_path = Path(dataset_path)
    
    # Find all HEIC files
    heic_files = []
    for ext in ['.heic', '.HEIC']:
        heic_files.extend(list(dataset_path.rglob(f"*{ext}")))
    
    if not heic_files:
        print("No HEIC files found")
        return
        
    print(f"Found {len(heic_files)} HEIC files")
    
    # Use all available CPU cores
    num_processes = mp.cpu_count()
    print(f"Using {num_processes} processes")
    
    # Process files in parallel
    with mp.Pool(num_processes) as pool:
        results = list(tqdm(
            pool.imap(convert_single_file, heic_files),
            total=len(heic_files),
            desc="Converting"
        ))
    
    success = sum(results)
    print(f"Successfully converted {success}/{len(heic_files)} files")

def main():
    datasets = [
        './data/CATI_FAS_dataset'
    ]
    
    for dataset in datasets:
        if os.path.exists(dataset):
            print(f"\nProcessing {os.path.basename(dataset)}...")
            convert_heic_to_jpg(dataset)
        else:
            print(f"\nSkipping {dataset} - directory not found")

if __name__ == '__main__':
    main()