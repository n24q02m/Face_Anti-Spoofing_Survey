import os
from kaggle.api.kaggle_api_extended import KaggleApi


def download_dataset(dataset_slug, destination_dir):
    if not os.path.exists(destination_dir):
        print("Dataset not found. Downloading from Kaggle...")
        try:
            # Initialize Kaggle API
            api = KaggleApi()
            api.authenticate()
            api.dataset_download_files(
                dataset_slug,
                path=destination_dir,
                unzip=True,
                quiet=False,
            )
            print("Dataset downloaded successfully!")
        except Exception as e:
            print(f"Error downloading dataset: {str(e)}")
            print("\nPlease ensure you have:")
            print("1. Installed kaggle package: pip install kaggle")
            print("2. Created a Kaggle account")
            print("3. Generated an API token from https://www.kaggle.com/settings")
            print("4. Placed kaggle.json in ~/.kaggle/ directory")
            return False
    else:
        print("Dataset already exists locally")
    return True
