import os
import cv2
import numpy as np 
from pathlib import Path
from tqdm import tqdm
import torch
import torchvision
from facenet_pytorch import MTCNN
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIF/HEIC opener
register_heif_opener()

# Initialize MTCNN model for face detection 
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(
    image_size=224,
    margin=0,
    min_face_size=20,
    thresholds=[0.6, 0.7, 0.7],
    factor=0.709,
    device=device,
    keep_all=False  # Only detect most prominent face
)

# Dataset paths
DATASETS = {
    'CATI-FAS': './data/CATI_FAS_dataset', 
    'LCC-FASD': './data/LCC_FASD_dataset',
    'NUAAA': './data/NUAAA_dataset'
}


def process_image(img_path, dataset_name):
    """Process single image and generate BB file"""
    try:        
        # Read image
        img = cv2.imread(str(img_path))
        if img is None:
            return False
            
        # Rest of processing remains same
        real_h, real_w = img.shape[:2]
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        boxes, probs = mtcnn.detect(img_rgb)
        
        if boxes is None or len(boxes) == 0:
            print(f"No face detected in {img_path}")
            return False
            
        box = boxes[0]
        prob = probs[0]
        
        x1, y1, x2, y2 = box
        w = x2 - x1
        h = y2 - y1
        
        x = int(x1 * 224 / real_w)
        y = int(y1 * 224 / real_h)
        w = int(w * 224 / real_w)
        h = int(h * 224 / real_h)
        
        bb_path = img_path.parent / f"{img_path.stem}_BB.txt"
        with open(bb_path, 'w') as f:
            f.write(f"{x} {y} {w} {h} {prob:.7f}")
            
        return True
        
    except Exception as e:
        print(f"Error processing {img_path}: {str(e)}")
        return False


def process_dataset(dataset_path, dataset_name):
    """Process entire dataset"""
    print(f"\nProcessing {dataset_name}...")
    
    # Find all images recursively
    image_files = []
    dataset_path = Path(dataset_path)
    for ext in ['.jpg', '.png',]:
        image_files.extend(list(dataset_path.rglob(f"*{ext}")))
    
    print(f"Found {len(image_files)} images")
    
    # Process each image 
    success = 0
    for img_path in tqdm(image_files, desc="Detecting faces"):
        if process_image(img_path, dataset_name):
            success += 1
            
    print(f"Successfully processed {success}/{len(image_files)} images")
    return success

def main():
    print("Starting face detection...")
    print(f"Using device: {device}")
    
    total_processed = 0
    
    # Process each dataset
    for name, path in DATASETS.items():
        if os.path.exists(path):
            total_processed += process_dataset(path, name)
        else:
            print(f"\nSkipping {name} - directory not found")
            
    print(f"\nTotal images processed: {total_processed}")

if __name__ == "__main__":
    main()