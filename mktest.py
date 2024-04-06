import os 
import random
import shutil

os.chdir(os.path.dirname(__file__))

image_dir = "./images"
labels_dir = "./labels"

target_image_count = 500
image_count = 0

images = os.listdir(image_dir)
random.shuffle(images)

i = 0
while image_count < target_image_count:
    image_file = images[i]
    i += 1
    label_path = os.path.join(labels_dir, f'{image_file.split(".")[0]}.txt')
    if not os.path.exists(label_path):
        print(f"Label file {label_path} for image {image_file} not found. Skipping...")
        continue
    print(f"Processing {image_file}...")
    print(os.path.join(image_dir, image_file))
    print(os.path.join(".", "test", "images", image_file))
    shutil.copy(os.path.join(image_dir, image_file), os.path.join(".", "test", "images", image_file))
    shutil.copy(label_path, os.path.join(".", "test", "labels", f'{image_file.split(".")[0]}.txt'))
    image_count += 1