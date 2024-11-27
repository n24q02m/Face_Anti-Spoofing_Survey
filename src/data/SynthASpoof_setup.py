import os
import zipfile
import json
import gdown
from kaggle.api.kaggle_api_extended import KaggleApi

def download_files():
    destination = './data/SynthASpoof_dataset'
    gdrive_url = "https://drive.google.com/file/d/12s7V6wcY1F-BNlKA1aIVVulz-vj8lcoB/view"
    zip_file = 'SynthASpoof_dataset.zip'
    
    if not os.path.exists(destination):
        os.makedirs(destination)

    print('Downloading file using gdown...')
    try:
        output = os.path.join(destination, zip_file)
        if not os.path.exists(output):
            success = gdown.download(
                url=gdrive_url,
                output=output,
                fuzzy=True,
                resume=True
            )
            if not success:
                print("\nDownload failed due to Google Drive limitations.")
                print("\nPlease follow these steps to download manually:")
                print(f"1. Visit the Google Drive link: {gdrive_url}")
                print("2. Download the zip file")
                print(f"3. Place the downloaded file in: {os.path.abspath(destination)}")
                print("\nAfter manual download, run this script again to continue with extraction.")
                return False
        
        # Verify downloaded file
        if os.path.exists(output) and os.path.getsize(output) > 0:
            print('Successfully downloaded file')
            return True
        else:
            print("Warning: File download incomplete or corrupted")
            return False

    except Exception as e:
        print(f"Error during download process: {str(e)}")
        print(f"\nAlternatively, you can download the file manually from: {gdrive_url}")
        return False

def extract_files():
    destination = './data/SynthASpoof_dataset'
    zip_file = os.path.join(destination, 'SynthASpoof_dataset.zip')
    
    print(f'Extracting {zip_file}...')
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(destination)
        print('Extraction completed successfully')
    except Exception as e:
        print(f"Error during extraction: {str(e)}")
        return False
    return True

def upload_to_kaggle():
    dataset_dir = './data/SynthASpoof_dataset'
    metadata = {
        'title': 'SynthASpoof - Face Anti-Spoofing Dataset',
        'id': 'n24q02m/synthaspoof-face-anti-spoofing-dataset',
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