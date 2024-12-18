import os
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener
from tqdm import tqdm

# Register HEIF/HEIC opener
register_heif_opener()

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
    
    # Convert each file
    for heic_path in tqdm(heic_files, desc="Converting"):
        try:
            # Open HEIC file
            img = Image.open(str(heic_path))
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            # Save as JPG with same name
            jpg_path = heic_path.with_suffix('.jpg')
            img.save(jpg_path, 'JPG', quality=95)
            
            # Remove original HEIC file after successful conversion
            heic_path.unlink()
            
        except Exception as e:
            print(f"Error converting {heic_path}: {str(e)}")

if __name__ == '__main__':
    datasets = [
        './data/CATI_FAS_dataset'
    ]
    
    for dataset in datasets:
        if os.path.exists(dataset):
            print(f"\nProcessing {os.path.basename(dataset)}...")
            convert_heic_to_jpg(dataset)
        else:
            print(f"\nSkipping {dataset} - directory not found")