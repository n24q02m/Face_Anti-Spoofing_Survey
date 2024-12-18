import os
from pathlib import Path
from tqdm import tqdm

def get_image_files(folder_path):
    """Get all image files in folder"""
    image_files = []
    for ext in ['.jpg', '.png']:
        image_files.extend(list(Path(folder_path).glob(f'*{ext}')))
    return sorted(image_files)

def remove_undetected_faces(dataset_path):
    """Remove images without corresponding BB files"""
    print(f"\nRemoving images without face detection in {os.path.basename(dataset_path)}...")
    removed = 0
    
    for folder in ['live', 'spoof']:
        folder_path = Path(dataset_path) / folder
        if not folder_path.exists():
            continue
            
        image_files = get_image_files(folder_path)
        if not image_files:
            continue
            
        print(f"\nChecking {folder} folder...")
        for img_file in tqdm(image_files, desc="Checking files"):
            bb_file = folder_path / f"{img_file.stem}_BB.txt"
            if not bb_file.exists():
                img_file.unlink()
                removed += 1
                
    return removed

def rename_files(dataset_path):
    """Rename files to 7 digits then back to 6 digits"""
    print(f"\nRenaming files in {os.path.basename(dataset_path)}...")
    
    # Count live files for spoof start index
    live_path = Path(dataset_path) / 'live'
    live_count = 0
    if live_path.exists():
        live_count = len(get_image_files(live_path))
    
    for folder in ['live', 'spoof']:
        folder_path = Path(dataset_path) / folder
        if not folder_path.exists():
            continue
            
        # Get all files (images and BB files)
        file_groups = {}
        for file in folder_path.iterdir():
            base = file.stem.split('_')[0]
            if base not in file_groups:
                file_groups[base] = []
            file_groups[base].append(file)
            
        # First rename to 7 digits
        print(f"\nConverting {folder} to 7 digits...")
        for i, (_, group) in enumerate(tqdm(file_groups.items())):
            new_base = f"{(i+1):07d}"
            for file in group:
                try:
                    parts = file.stem.split('_')
                    extension = file.suffix
                    new_name = f"{new_base}{'_BB' if len(parts) > 1 else ''}{extension}"
                    new_path = file.parent / new_name
                    file.rename(new_path)
                except Exception as e:
                    print(f"Error converting {file.name}: {str(e)}")
        
        # Then rename back to 6 digits
        file_groups = {}
        for file in folder_path.iterdir():
            base = file.stem.split('_')[0]
            if base not in file_groups:
                file_groups[base] = []
            file_groups[base].append(file)
            
        # start_idx continues from live to spoof
        start_idx = 1 if folder == 'live' else live_count + 1
        
        print(f"\nRenaming {folder} to 6 digits...")
        for i, (_, group) in enumerate(tqdm(file_groups.items())):
            new_base = f"{(start_idx + i):06d}"
            for file in group:
                try:
                    parts = file.stem.split('_')
                    extension = file.suffix 
                    new_name = f"{new_base}{'_BB' if len(parts) > 1 else ''}{extension}"
                    new_path = file.parent / new_name
                    file.rename(new_path)
                except Exception as e:
                    print(f"Error renaming {file.name}: {str(e)}")

def main():
    datasets = [
        './data/CATI_FAS_dataset',
        './data/LCC_FASD_dataset', 
        './data/NUAAA_dataset',
        './data/CelebA_Spoof_dataset'
    ]
    
    for dataset in datasets:
        if os.path.exists(dataset):
            removed = remove_undetected_faces(dataset)
            if removed > 0:
                rename_files(dataset)
        else:
            print(f"\nSkipping {dataset} - directory not found")

if __name__ == '__main__':
    main()