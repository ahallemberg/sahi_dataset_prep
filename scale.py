import os 
import cv2
import shutil
import numpy as np 
import concurrent.futures
from tqdm import tqdm

TARGET_X = 4656
TARGET_Y = 3496

class Scale: 
    def __init__(self, target_x: int, target_y: int, input_dir: str) -> None: 
        self.target_x = target_x   
        self.target_y = target_y
        self.input_dir = input_dir
        self.input_image_dir = os.path.join(input_dir, "images")
        self.input_labels_dir = os.path.join(input_dir, "labels")

        assert os.path.exists(self.input_dir), f"input_dir: {self.input_dir} does not exist"
        assert os.path.exists(self.input_image_dir), f"input_image_dir: {self.input_image_dir} does not exist"
        assert os.path.exists(self.input_labels_dir), f"input_labels_dir: {self.input_labels_dir} does not exist"

        os.makedirs(os.path.join(input_dir, "resized", "images"), exist_ok=True)
        os.makedirs(os.path.join(input_dir, "resized", "labels"), exist_ok=True)

        self.output_image_dir = os.path.join(input_dir, "resized", "images")
        self.output_labels_dir = os.path.join(input_dir, "resized", "labels")

    def __call__(self) -> None: 
        self.process()

    def single_resize(self, image_basename: str) -> tuple[str, np.ndarray]|None: 
        label = os.path.join(self.input_labels_dir, image_basename.split(".")[0]+".txt")

        if not os.path.exists(label):
            print(f"Label file {label} for image {image_basename} not found. Skipping...")
            return None
        
        img = cv2.imread(os.path.join(self.input_image_dir, image_basename))
        img_resized = cv2.resize(img, dsize=(self.target_x,self.target_y),fx=self.target_x, fy=self.target_y, interpolation=cv2.INTER_CUBIC)
        return (image_basename, img_resized)

    def single_process(self, image_basename: str) -> None: 
        result = self.single_resize(image_basename)
        if result: 
            self.write(*result)

    def process(self, workers:int = os.cpu_count()) -> None: 
        print(f"Scaling using {workers} workers")
        image_basenames = os.listdir(self.input_image_dir)
        
        # Use ProcessPoolExecutor to run tasks in parallel
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
            # Map the single_process function to each image_basename
            for _ in tqdm(executor.map(self.single_process, image_basenames), total=len(image_basenames)):
                ...
            
    def write(self, image_basename: str, img: np.ndarray) -> None: 
        cv2.imwrite(os.path.join(self.output_image_dir, image_basename), img)

        label = os.path.join(self.input_labels_dir, image_basename.split(".")[0]+".txt")
        label_target = os.path.join(self.output_labels_dir, image_basename.split(".")[0]+".txt")

        shutil.copy(label, label_target) 

def main(): 
    os.chdir(os.path.dirname(__file__))
    input_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "test"))
    scale = Scale(
        target_x=TARGET_X,
        target_y=TARGET_Y,
        input_dir=input_dir
    )
    scale()
    

if __name__ == "__main__":
    main()
