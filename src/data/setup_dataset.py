import os
import zipfile
import json
import gdown
from kaggle.api.kaggle_api_extended import KaggleApi

def download_files():
    folder_url = 'https://drive.google.com/drive/folders/1OW_1bawO79pRqdVEVmBzp8HSxdSwln_Z'
    destination = './data'
    if not os.path.exists(destination):
        os.makedirs(destination)
    print('Downloading files using gdown...')
    gdown.download_folder(url=folder_url, output=destination, quiet=False, use_cookies=False)
    # Verify that all 74 files are downloaded
    base_filename = 'CelebA_Spoof.zip.'
    file_numbers = ['{:03d}'.format(i) for i in range(1, 75)]
    expected_files = [f'{base_filename}{num}' for num in file_numbers]
    downloaded_files = os.listdir(destination)
    missing_files = set(expected_files) - set(downloaded_files)
    if not missing_files:
        print('All files downloaded successfully.')
    else:
        print(f'Some files are missing: {missing_files}')

def extract_files():
    source = './data'
    destination = './data/CelebA-Spoof'
    if not os.path.exists(destination):
        os.makedirs(destination)
    zip_files = [f for f in os.listdir(source) if f.startswith('CelebA_Spoof.zip.')]
    for zip_file in zip_files:
        zip_path = os.path.join(source, zip_file)
        print(f'Extracting {zip_file}...')
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(destination)

def upload_to_kaggle():
    dataset_dir = './data/CelebA-Spoof'
    metadata = {
        'title': 'CelebA-Spoof - Face Anti-Spoofing Dataset',
        'id': 'n24q02m/celeba-spoof-face-anti-spoofing-dataset',
        'licenses': [{'name': 'CC0-1.0'}]
    }
    metadata_path = os.path.join(dataset_dir, 'dataset-metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
    # Use Kaggle API in Python to create the dataset
    api = KaggleApi()
    api.authenticate()
    print('Creating dataset on Kaggle...')
    api.dataset_create_new(
        folder=dataset_dir,
        public=True,
        dir_mode='zip',
        quiet=False
    )

if __name__ == '__main__':
    download_files()
    extract_files()
    upload_to_kaggle()