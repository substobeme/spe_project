import face_recognition
import os
import pickle
import numpy as np
from collections import Counter
from datetime import datetime
import time
import sys

def train():
    known_encodings = []
    known_names = []

    data_dir = "/app/data"
    output_dir = "/app/models"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    total_images = 0

    print("[INFO] Starting training process...")
    
    # Check if data directory exists and has subdirectories
    if not os.path.exists(data_dir):
        print(f"[ERROR] Data directory {data_dir} does not exist!")
        return False
        
    # Get the list of person directories
    person_dirs = []
    for label in os.listdir(data_dir):
        person_dir = os.path.join(data_dir, label)
        if os.path.isdir(person_dir):
            person_dirs.append((label, person_dir))
    
    if not person_dirs:
        print(f"[ERROR] No person directories found in {data_dir}!")
        print("[INFO] Please create subdirectories for each person (e.g., data/1/, data/2/)")
        return False

    # Process each person directory
    for label, person_dir in person_dirs:
        print(f"[INFO] Processing label '{label}'...")
        
        image_files = [f for f in os.listdir(person_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not image_files:
            print(f"[WARNING] No image files found in {person_dir}")
            continue
            
        for img_name in image_files:
            path = os.path.join(person_dir, img_name)
            try:
                print(f"[DEBUG] Processing image {img_name}")
                image = face_recognition.load_image_file(path)
                encs = face_recognition.face_encodings(image)
                if encs:
                    known_encodings.append(encs[0])
                    known_names.append(label)
                    total_images += 1
                    print(f"[DEBUG] Encoded image {img_name}")
                else:
                    print(f"[WARNING] No faces found in image {img_name}")
            except Exception as e:
                print(f"[ERROR] Failed to process image {img_name}: {e}")

    if total_images == 0:
        print("[ERROR] No faces found in the dataset. Exiting training.")
        return False

    # Save encodings and names
    encodings_path = os.path.join(output_dir, "encodings.pkl")
    with open(encodings_path, "wb") as f:
        pickle.dump({"encodings": known_encodings, "names": known_names}, f)
    print(f"[INFO] Saved {encodings_path} with {total_images} images.")

    # Print summary statistics
    print(f"[INFO] Training complete on {total_images} images across {len(set(known_names))} classes.")
    class_counts = Counter(known_names)
    for label, count in class_counts.items():
        print(f"[INFO] Class '{label}': {count} images")
        
    return True

if __name__ == "__main__":
    success = train()
    if not success:
        sys.exit(1)
