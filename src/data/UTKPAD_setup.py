import os
import tarfile
import json
import requests
from tqdm import tqdm
from kaggle.api.kaggle_api_extended import KaggleApi

def download_file(url, output_path):
    """Download a file from URL with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(output_path, 'wb') as file, tqdm(
        desc=os.path.basename(output_path),
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)

def download_files():
    destination = './data/UTKPAD_dataset'
    urls = [
        'https://zenodo.org/records/11234659/files/UTKPAD_iphone12_part1.tar.gz?download=1',
        'https://zenodo.org/records/11234659/files/UTKPAD_iphone12_part2.tar.gz?download=1',
        'https://zenodo.org/records/11234659/files/UTKPAD_iphone12_part3.tar.gz?download=1'
    ]
    
    if not os.path.exists(destination):
        os.makedirs(destination)

    print('Downloading files from Zenodo...')
    try:
        for idx, url in enumerate(urls, 1):
            output = os.path.join(destination, f'UTKPAD_iphone12_part{idx}.tar.gz')
            if not os.path.exists(output):
                print(f'Downloading file {idx}/3...')
                try:
                    download_file(url, output)
                except Exception as download_error:
                    print("\nDownload failed.")
                    print("\nPlease follow these steps to download manually:")
                    print("1. Visit Zenodo: https://zenodo.org/records/11234659")
                    print("2. Download all UTKPAD_iphone12_part*.tar.gz files")
                    print(f"3. Place the downloaded files in: {os.path.abspath(destination)}")
                    print("\nAfter manual download, run this script again to continue with extraction.")
                    return False

        # Verify downloaded files
        tar_files = [f for f in os.listdir(destination) if f.endswith('.tar.gz')]
        if len(tar_files) != 3:
            print(f'Warning: Found {len(tar_files)} files instead of expected 3')
            return False
        else:
            print('Successfully downloaded all 3 files')
            return True
            
    except Exception as e:
        print(f"Error during download process: {str(e)}")
        print("\nPlease try downloading the files manually from Zenodo")
        return False

def extract_files():
    destination = './data/UTKPAD_dataset'
    tar_files = [f for f in os.listdir(destination) if f.endswith('.tar.gz')]
    
    for tar_file in tar_files:
        tar_path = os.path.join(destination, tar_file)
        print(f'Extracting {tar_file}...')
        try:
            with tarfile.open(tar_path, 'r:gz') as tar:
                tar.extractall(path=destination)
        except Exception as e:
            print(f"Error extracting {tar_file}: {str(e)}")
            return False
    
    print('All files extracted successfully')
    return True

def upload_to_kaggle():
    dataset_dir = './data/UTKPAD_dataset'
    metadata = {
        'title': 'UTKPAD - Face Anti-Spoofing Dataset',
        'id': 'n24q02m/utkpad-face-anti-spoofing-dataset',
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