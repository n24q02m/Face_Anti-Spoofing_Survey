import os
import zipfile
import json
import gdown
from kaggle.api.kaggle_api_extended import KaggleApi

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
        if len(files) == 0:
            print("Warning: No files were downloaded")
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
    base_dir = destination
    zip_files = [f for f in os.listdir(destination) if f.endswith('.zip')]
    
    for zip_file in zip_files:
        zip_path = os.path.join(destination, zip_file)
        print(f'Extracting {zip_file}...')
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(base_dir)

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