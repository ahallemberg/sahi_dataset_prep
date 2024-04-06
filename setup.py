import os
from glob import glob

def split():
    SHUFFLE = True

    os.chdir(os.path.dirname(__file__))

    image_dir = "./images"
    labels_dir = "./labels"

    train, val, test = 0.80, 0.15, 0.05

    if train+val+test != 1:
        raise ValueError("Train, validation and test split should sum to 1")

    images_path = glob(os.path.join(image_dir, "*.png"))
    image_count = len(images_path)

    if SHUFFLE:
        from random import shuffle
        shuffle(images_path)

    for index, image_path in enumerate(images_path):
        name = os.path.basename(image_path).split(".")[0]
        label_path = os.path.join(labels_dir, name + ".txt")

        if not os.path.exists(label_path):
            print(f"Label file {label_path} for image {image_path} not found. Skipping...")
            continue

        if index < image_count * train:
            # mv image and label to ./train folder. create folder if not exists
            os.makedirs("train", exist_ok=True)
            # now create subfolders for images and labels
            os.makedirs(os.path.join("train", "images"), exist_ok=True)
            os.makedirs(os.path.join("train", "labels"), exist_ok=True)
            os.rename(image_path, os.path.join("train", "images", os.path.basename(image_path)))
            os.rename(label_path, os.path.join("train", "labels", os.path.basename(label_path)))

        elif index < image_count * (train + val):
            # mv image and label to ./val folder. create folder if not exists
            os.makedirs("val", exist_ok=True)
            # now create subfolders for images and labels
            os.makedirs(os.path.join("val", "images"), exist_ok=True)
            os.makedirs(os.path.join("val", "labels"), exist_ok=True)
            os.rename(image_path, os.path.join("val", "images", os.path.basename(image_path)))
            os.rename(label_path, os.path.join("val", "labels", os.path.basename(label_path)))
        else:
            # mv image and label to ./test folder. create folder if not exists
            os.makedirs("test", exist_ok=True)
            # now create subfolders for images and labels
            os.makedirs(os.path.join("test", "images"), exist_ok=True)
            os.makedirs(os.path.join("test", "labels"), exist_ok=True)
            os.rename(image_path, os.path.join("test", "images", os.path.basename(image_path)))
            os.rename(label_path, os.path.join("test", "labels", os.path.basename(label_path)))

def revert():
    os.chdir(os.path.dirname(__file__))

    # move all images and labels back to root folder
    for folder in ["train", "val", "test"]:
        for subfolder in ["images", "labels"]:
            for file in glob(os.path.join(folder, subfolder, "*")):
                # mv image to ./images folder and labels to ./labels folder
                os.rename(file, os.path.join(".", subfolder, os.path.basename(file)))



if __name__ == "__main__":
    revert()
