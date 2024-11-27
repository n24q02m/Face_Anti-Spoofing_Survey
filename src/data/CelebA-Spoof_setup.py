import os
import zipfile
import json
import gdown
from kaggle.api.kaggle_api_extended import KaggleApi
import shutil

def download_files():
    url_list_file = './data/CelebA-Spoof_url-list.txt'
    destination = './data/CelebA-Spoof_dataset'
    gdrive_folder = "https://drive.google.com/drive/folders/1OW_1bawO79pRqdVEVmBzp8HSxdSwln_Z"
    
    if not os.path.exists(destination):
        os.makedirs(destination)

    print('Downloading files individually using gdown...')
    try:
        with open(url_list_file, 'r') as f:
            urls = [line.strip() for line in f.readlines()]
        for idx, url in enumerate(urls):
            output = os.path.join(destination, f'CelebA_Spoof.zip.{idx+1:03d}')
            if not os.path.exists(output):
                print(f'Downloading file {idx+1}/{len(urls)}...')
                try:
                    gdown.download(url=url, output=output, fuzzy=True, resume=True)
                except Exception as download_error:
                    print("\nDownload failed due to Google Drive limitations.")
                    print("\nPlease follow these steps to download manually:")
                    print(f"1. Visit the Google Drive folder: {gdrive_folder}")
                    print("2. Download all CelebA_Spoof.zip.* files")
                    print(f"3. Place the downloaded files in: {os.path.abspath(destination)}")
                    print("\nAfter manual download, run this script again to continue with extraction.")
                    return False

        # Verify downloaded files
        zip_files = [f for f in os.listdir(destination) if f.startswith('CelebA_Spoof.zip.')]
        if len(zip_files) != 74:
            print(f'Warning: Found {len(zip_files)} files instead of expected 74')
        else:
            print('Successfully downloaded all 74 files')
            return True
            
    except Exception as e:
        print(f"Error during download process: {str(e)}")
        print(f"\nAlternatively, you can download the files manually from: {gdrive_folder}")
        return False

def extract_files():
    destination = './data/CelebA-Spoof_dataset'
    base_dir = destination
    
    # Find all split files ordered by extension
    split_files = sorted([f for f in os.listdir(destination) if f.startswith('CelebA_Spoof.zip.')])
    
    if not split_files:
        print("No split files found")
        return
        
    # Combine split files
    print("Combining split files...")
    output_path = os.path.join(destination, 'CelebA_Spoof.zip')
    with open(output_path, 'wb') as output:
        for split_file in split_files:
            print(f'Processing {split_file}...')
            file_path = os.path.join(destination, split_file)
            with open(file_path, 'rb') as part:
                shutil.copyfileobj(part, output)
    
    # Extract combined file
    print(f'Extracting combined file...')
    try:
        with zipfile.ZipFile(output_path, 'r') as zip_ref:
            zip_ref.extractall(base_dir)
        print("Extraction completed successfully")
        
        # Optionally remove the combined file to save space
        # os.remove(output_path)
    except zipfile.BadZipFile:
        print("Error: Combined file is not a valid ZIP file")

def upload_to_kaggle():
    dataset_dir = './data/CelebA-Spoof_dataset'
    metadata = {
        'title': 'CelebA-Spoof - Face Anti-Spoofing Dataset',
        'id': 'n24q02m/celeba-spoof-face-anti-spoofing-dataset',
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