import os
import zipfile
import json
import gdown
from kaggle.api.kaggle_api_extended import KaggleApi
import shutil

def download_files():
    destination = './data/MSU-MFSD_dataset'
    gdrive_folder = "https://drive.google.com/drive/folders/1nJCPdJ7R67xOiklF1omkfz4yHeJwhQsz"
    
    if not os.path.exists(destination):
        os.makedirs(destination)

    print('Downloading folder using gdown...')
    try:
        output = gdown.download_folder(
            url=gdrive_folder,
            output=destination,
            resume=True
        )
        if output is None:
            print("\nDownload failed due to Google Drive limitations.")
            print("\nPlease follow these steps to download manually:")
            print(f"1. Visit the Google Drive folder: {gdrive_folder}")
            print("2. Download all files")
            print(f"3. Place the downloaded files in: {os.path.abspath(destination)}")
            print("\nAfter manual download, run this script again to continue with extraction.")
            return False
        
        # Verify downloaded files
        files = os.listdir(destination)
        expected_file_count = 17  # 16 RAR files + 1 txt file
        if len(files) != expected_file_count:
            print(f"Warning: Found {len(files)} files instead of expected {expected_file_count}")
            return False
        else:
            print(f'Successfully downloaded {len(files)} files')
            return True

    except Exception as e:
        print(f"Error during download process: {str(e)}")
        print(f"\nAlternatively, you can download the files manually from: {gdrive_folder}")
        return False

def extract_files():
    destination = './data/MSU-MFSD_dataset'
    
    # Find all split files ordered by extension
    split_files = sorted([f for f in os.listdir(destination) if f.startswith('MSU-MFSD-Publish.zip.')])
    
    if not split_files:
        print("No split files found")
        return False
        
    # Combine split files
    print("Combining split files...")
    output_path = os.path.join(destination, 'MSU-MFSD-Publish.zip')
    with open(output_path, 'wb') as output:
        for split_file in split_files:
            print(f'Processing {split_file}...')
            file_path = os.path.join(destination, split_file)
            with open(file_path, 'rb') as part:
                shutil.copyfileobj(part, output)
            # Remove split file after combining
            os.remove(file_path)
            print(f'Removed {split_file}')
    
    # Extract combined file
    print(f'Extracting combined file...')
    try:
        with zipfile.ZipFile(output_path, 'r') as zip_ref:
            zip_ref.extractall(destination)
        print("Extraction completed successfully")
        
        # Remove the combined file
        os.remove(output_path)
        print("Removed combined zip file")
        return True
    except zipfile.BadZipFile:
        print("Error: Combined file is not a valid ZIP file")
        return False

def upload_to_kaggle():
    dataset_dir = './data/MSU-MFSD_dataset'
    metadata = {
        'title': 'MSU-MFSD - Face Anti-Spoofing Dataset',
        'id': 'n24q02m/msu-mfsd-face-anti-spoofing-dataset',
        'licenses': [{'name': 'CC0-1.0'}]
    }
    metadata_path = os.path.join(dataset_dir, 'dataset-metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    api = KaggleApi()
    api.authenticate()
    print('Creating dataset on Kaggle...')
    api.dataset_create_new(
        folder=dataset_dir,
        dir_mode='zip',
        quiet=False
    )

if __name__ == '__main__':
    if download_files():
        extract_files()
        upload_to_kaggle()
    else:
        print("\nDownload incomplete. Please complete the manual download before proceeding.")