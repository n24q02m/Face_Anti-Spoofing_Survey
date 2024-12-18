import os
import json
from pathlib import Path
from tqdm import tqdm
from kaggle.api.kaggle_api_extended import KaggleApi

# Dataset configurations 
DATASETS = {
    'CATI-FAS': {
        'path': './data/CATI_FAS_dataset',
        'id': 'n24q02m/cati-fas-face-anti-spoofing-dataset',
        'title': 'CATI-FAS - Face Anti-Spoofing Dataset'  
    },
    'LCC-FASD': {
        'path': './data/LCC_FASD_dataset',
        'id': 'n24q02m/lcc-fasd-face-anti-spoofing-dataset',
        'title': 'LCC-FASD - Face Anti-Spoofing Dataset'
    },
    'NUAAA': {
        'path': './data/NUAAA_dataset', 
        'id': 'n24q02m/nuaaa-face-anti-spoofing-dataset',
        'title': 'NUAA - Face Anti-Spoofing Dataset'
    },
    'CelebA-Spoof': {
      'path': './data/CelebA_Spoof_dataset',
      'id': 'n24q02m/celeba-spoof-face-anti-spoofing-dataset',
      'title': 'CelebA-Spoof - Face Anti-Spoofing Dataset',
    }
}

def verify_face_detection(dataset_path):
    """Verify that face detection has been completed for dataset"""
    # Check both live and spoof folders
    for folder in ['live', 'spoof']:
        folder_path = Path(dataset_path) / folder
        if not folder_path.exists():
            continue
            
        # Get all image files
        image_files = []
        for ext in ['.jpg', '.jpeg', '.png', '.heic']:
            image_files.extend(list(folder_path.glob(f'*{ext}')))
            
        # Check for corresponding BB files
        for img_file in image_files:
            bb_file = folder_path / f"{img_file.stem}_BB.txt"
            if not bb_file.exists():
                return False
                
    return True

def create_metadata(dataset_config):
    """Create dataset metadata file"""
    metadata = {
        'title': dataset_config['title'],
        'id': dataset_config['id'],
        'licenses': [{'name': 'CC0-1.0'}]
    }
    
    metadata_path = Path(dataset_config['path']) / 'dataset-metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
        
def upload_dataset(dataset_name, dataset_config):
    """Upload new version of dataset to Kaggle"""
    print(f"\nProcessing {dataset_name}...")
    
    # Verify face detection completed
    if not verify_face_detection(dataset_config['path']):
        print("Face detection results incomplete. Skipping upload.")
        return False
        
    try:
        # Create metadata file
        create_metadata(dataset_config)
        
        # Initialize Kaggle API
        api = KaggleApi()
        api.authenticate()
        
        # Create new version
        print(f"Uploading new version of {dataset_name} to Kaggle...")
        api.dataset_create_version(
            folder=dataset_config['path'],
            version_notes="Added face detection bounding boxes",
            dir_mode='zip',
            quiet=False
        )
        print(f"Successfully uploaded new version of {dataset_name}")
        return True
        
    except Exception as e:
        print(f"Error uploading {dataset_name}: {str(e)}")
        return False

def main():
    print("Starting dataset uploads...")
    success = 0
    
    # Process each dataset
    for name, config in DATASETS.items():
        if os.path.exists(config['path']):
            if upload_dataset(name, config):
                success += 1
        else:
            print(f"\nSkipping {name} - directory not found")
            
    print(f"\nSuccessfully uploaded {success}/{len(DATASETS)} datasets")

if __name__ == '__main__':
    main()