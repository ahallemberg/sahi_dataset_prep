import json
import os
from PIL import Image
import time

class YoloToCoco: 
    def __init__(
            self,
            input_dir: str,
            output_dir: str,
            categories: list[dict[str, str|int]],
            output_file_name: str = "annotations.json",
            label_portion: float = 1
        ) -> None: 
        os.chdir(os.path.dirname(__file__))
        self.__processed = False
        self.input_dir = os.path.abspath(input_dir)
        self.output_dir = os.path.abspath(output_dir)
        self.output_file_name = output_file_name
        self.label_portion = label_portion

        assert os.path.exists(self.input_dir), f"input_dir: {self.input_dir} does not exist"
        assert os.path.exists(self.output_dir), f"output_dir: {self.output_dir} does not exist"

        # COCO dataset dictionary. Images and annotations will be added to this dictionary
        self.coco_dataset = {
            "info": {},
            "licenses": [],
            "categories": categories,
            "images": [],
            "annotations": []
        }

    def __call__(self) -> None:
        self.process()
        self.save()

    def single_process(self, image_basename: str) -> None:
            image = Image.open(os.path.join(self.input_dir, "images", image_basename))
            width, height = image.size
            
            id = int(image_basename.split('.')[0].removeprefix("Image"))

            # Add the image to the COCO dataset
            image_dict = {
                "id": id,
                "width": width,
                "height": height,
                "file_name": image_basename
            }
            
            self.coco_dataset["images"].append(image_dict)
            
            # Load the bounding box annotations for the image
            with open(os.path.join(self.input_dir, "labels", f'{image_basename.split(".")[0]}.txt')) as f:
                annotations = f.readlines()
            
            # Loop through the annotations and add them to the COCO dataset
            for ann in annotations:
                cls, x, y, w, h = map(float, ann.strip().split())
                x_min, y_min = int((x - w / 2) * width), int((y - h / 2) * height)
                x_max, y_max = int((x + w / 2) * width), int((y + h / 2) * height)
                ann_dict = {
                    "id": len(self.coco_dataset["annotations"]),
                    "image_id": id,
                    "category_id": int(cls),
                    "bbox": [x_min, y_min, x_max - x_min, y_max - y_min],
                    "area": (x_max - x_min) * (y_max - y_min),
                    "iscrowd": 0
                }
                self.coco_dataset["annotations"].append(ann_dict)

            print(f"Added image {id} to the COCO dataset")
            self.__processed = True


    def process(self) -> None: 
        _start = time.time()
        for image_basename in os.listdir(os.path.join(self.input_dir, "images"))[:int(len(os.listdir(os.path.join(self.input_dir, "images"))) * self.label_portion)]:
            self.single_process(image_basename)
        _end = time.time()
        print(f"Coverting YOLO labels to COCO took: {_end - _start:.2f}s")

    def save(self) -> None: 
        assert self.__processed, "You must process the data first"

        with open(os.path.join(self.output_dir, self.output_file_name), 'w') as f:
            json.dump(self.coco_dataset, f)
    
