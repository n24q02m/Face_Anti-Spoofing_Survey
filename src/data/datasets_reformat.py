import os
from pathlib import Path
from tqdm import tqdm

def get_all_images(directory):
    """Get all image files recursively from a directory."""
    image_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.heic')):
                image_files.append(os.path.join(root, file))
    return sorted(image_files)

def rename_files(image_files, start_index=1):
    """Rename files with sequential numbering."""
    for idx, old_path in enumerate(image_files, start_index):
        directory = os.path.dirname(old_path)
        extension = os.path.splitext(old_path)[1].lower()
        new_name = f"{idx:06d}{extension}"
        new_path = os.path.join(directory, new_name)
        
        try:
            os.rename(old_path, new_path)
        except Exception as e:
            print(f"Error renaming {old_path}: {str(e)}")

def process_simple_dataset(dataset_path):
    """Process datasets with simple live/spoof structure (CATI-FAS, LCC-FASD)."""
    print(f"\nProcessing {os.path.basename(dataset_path)}...")
    
    # Process live and spoof folders separately with different starting indices
    live_dir = os.path.join(dataset_path, 'live')
    spoof_dir = os.path.join(dataset_path, 'spoof')
    
    # Get images from live folder
    if os.path.exists(live_dir):
        live_images = get_all_images(live_dir)
        print(f"Found {len(live_images)} images in live")
        print("Renaming live files...")
        rename_files(live_images, start_index=1)  # Start from 000001
        
    # Get images from spoof folder 
    if os.path.exists(spoof_dir):
        spoof_images = get_all_images(spoof_dir)
        print(f"Found {len(spoof_images)} images in spoof")
        print("Renaming spoof files...")
        # Start spoof numbering after the last live number to avoid duplicates
        spoof_start_index = len(live_images) + 1 if os.path.exists(live_dir) else 1
        rename_files(spoof_images, start_index=spoof_start_index)

def process_nuaa_dataset(dataset_path):
    """Process NUAA dataset with nested structure."""
    print("\nProcessing NUAA dataset...")
    
    # Create main live/spoof directories if they don't exist
    live_dir = os.path.join(dataset_path, 'live')
    spoof_dir = os.path.join(dataset_path, 'spoof')
    os.makedirs(live_dir, exist_ok=True)
    os.makedirs(spoof_dir, exist_ok=True)
    
    # Collect and move all images
    all_images = []
    for subdir in ['live', 'spoof']:
        subdir_path = os.path.join(dataset_path, subdir)
        if os.path.exists(subdir_path):
            # Get all images recursively
            images = get_all_images(subdir_path)
            print(f"Found {len(images)} images in {subdir}")
            
            # Move images to main live/spoof directory
            target_dir = live_dir if subdir == 'live' else spoof_dir
            for img_path in tqdm(images, desc=f"Moving {subdir} images"):
                new_path = os.path.join(target_dir, os.path.basename(img_path))
                os.rename(img_path, new_path)
            
            all_images.extend([os.path.join(target_dir, os.path.basename(img)) for img in images])
    
    # Rename all files sequentially
    print("Renaming files...")
    rename_files(all_images)
    
    # Remove empty directories
    print("Cleaning up empty directories...")
    for root, dirs, files in os.walk(dataset_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path) and dir_path not in [live_dir, spoof_dir]:
                os.rmdir(dir_path)

def process_celeba_dataset(dataset_path):
    """Process CelebA-Spoof dataset."""
    print("\nProcessing CelebA-Spoof dataset...")
    
    # Create main live/spoof directories
    live_dir = os.path.join(dataset_path, 'live')
    spoof_dir = os.path.join(dataset_path, 'spoof')
    os.makedirs(live_dir, exist_ok=True)
    os.makedirs(spoof_dir, exist_ok=True)
    
    # Process both test and train directories
    for subset in ['test', 'train']:
        subset_path = os.path.join(dataset_path, subset)
        if not os.path.exists(subset_path):
            continue
            
        print(f"Processing {subset} subset...")
        
        # Find and move all live/spoof images and their txt files
        for root, _, files in os.walk(subset_path):
            if os.path.basename(root) in ['live', 'spoof']:
                target_dir = live_dir if os.path.basename(root) == 'live' else spoof_dir
                
                # Group files by base name (without extension)
                file_groups = {}
                for file in files:
                    base_name = os.path.splitext(file)[0]
                    if base_name not in file_groups:
                        file_groups[base_name] = []
                    file_groups[base_name].append(file)
                
                # Move each group of files
                for base_name, group_files in tqdm(file_groups.items(), 
                    desc=f"Moving {os.path.basename(root)} files from {subset}"):
                    
                    for file in group_files:
                        old_path = os.path.join(root, file)
                        new_path = os.path.join(target_dir, file)
                        if os.path.exists(new_path):
                            print(f"Warning: Skipping duplicate file {file}")
                            continue
                        os.rename(old_path, new_path)
    
    # Remove empty directories
    print("Cleaning up empty directories...")
    for root, dirs, files in os.walk(dataset_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path) and dir_path not in [live_dir, spoof_dir]:
                os.rmdir(dir_path)
                print(f"Removed empty directory: {dir_path}")

def main():
    # Define dataset paths
    datasets = {
        'CATI-FAS': './data/CATI_FAS_dataset',
        'LCC-FASD': './data/LCC_FASD_dataset',
        'NUAA': './data/NUAAA_dataset',
        'CelebA-Spoof': './data/CelebA_Spoof_dataset'
    }
    
    # Process each dataset
    for name, path in datasets.items():
        if not os.path.exists(path):
            print(f"\nSkipping {name} - directory not found")
            continue
            
        # if name in ['CATI-FAS', 'LCC-FASD']:
        #     process_simple_dataset(path)
        # elif name == 'NUAA':
        #     process_nuaa_dataset(path)
        # elif name == 'CelebA-Spoof':
        #     process_celeba_dataset(path)
            
        if name in ['CATI-FAS']:
            process_simple_dataset(path)
        elif name == 'CelebA-Spoof':
            process_celeba_dataset(path)
        
# if __name__ == '__main__':
#     main()
    
def fix_catifas_filenames():
    dataset_path = './data/CATI_FAS_dataset'
    for folder in ['live', 'spoof']:
        folder_path = os.path.join(dataset_path, folder)
        if not os.path.exists(folder_path):
            continue
            
        # Đầu tiên đổi tên file thành 7 chữ số để tránh conflict
        files = list(Path(folder_path).glob('*.*'))
        for file in tqdm(files, desc=f"Converting {folder} to 7 digits"):
            try:
                # Xử lý tên file có dạng "b (9983).jpg"
                old_name = file.name
                name_parts = file.stem.replace('b (', '').replace(')', '') # Bỏ "b (" và ")"
                number = int(name_parts) # Convert thành số
                
                # Tạo tên file mới với 7 chữ số
                extension = file.suffix
                new_name = f"{number:07d}{extension}"
                new_path = file.parent / new_name
                file.rename(new_path)
            except Exception as e:
                print(f"Error converting {old_name}: {str(e)}")
                
        # Sau đó đổi lại thành 6 chữ số theo yêu cầu
        files = list(Path(folder_path).glob('*.*'))
        start_idx = 1 if folder == 'live' else len(files) + 1
        
        for idx, file in enumerate(tqdm(files, desc=f"Renaming {folder} to 6 digits")):
            try:
                extension = file.suffix
                new_name = f"{(start_idx + idx):06d}{extension}"
                new_path = file.parent / new_name
                file.rename(new_path)
            except Exception as e:
                print(f"Error renaming {file.name}: {str(e)}")

def fix_celeba_filenames():
    dataset_path = './data/CelebA_Spoof_dataset'
    
    # Đếm số lượng file live để làm start_idx cho spoof
    live_path = os.path.join(dataset_path, 'live')
    live_count = 0
    if os.path.exists(live_path):
        live_count = len([f for f in Path(live_path).glob('*.*') if not f.name.endswith('_BB.txt')])
    
    for folder in ['live', 'spoof']:
        folder_path = os.path.join(dataset_path, folder)
        if not os.path.exists(folder_path):
            continue
            
        # Nhóm các file theo base name (không có đuôi mở rộng và _BB)
        file_groups = {}
        for file in Path(folder_path).iterdir():
            base = file.stem.split('_')[0]  # Tách phần _BB nếu có
            if base not in file_groups:
                file_groups[base] = []
            file_groups[base].append(file)
            
        # Đầu tiên đổi tên thành 7 chữ số  
        for i, (_, group) in enumerate(tqdm(file_groups.items(), desc=f"Converting {folder} to 7 digits")):
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
                    
        # Sau đó đổi lại thành 6 chữ số
        file_groups = {}
        for file in Path(folder_path).iterdir():
            base = file.stem.split('_')[0]
            if base not in file_groups:
                file_groups[base] = []
            file_groups[base].append(file)
            
        # start_idx nối tiếp từ live sang spoof
        start_idx = 1 if folder == 'live' else live_count + 1

        for i, (_, group) in enumerate(tqdm(file_groups.items(), desc=f"Renaming {folder} to 6 digits")):
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

# Thực thi
if __name__ == '__main__':
    print("Processing CATI-FAS dataset...")
    fix_catifas_filenames()
    
    print("\nProcessing CelebA-Spoof dataset...") 
    fix_celeba_filenames()