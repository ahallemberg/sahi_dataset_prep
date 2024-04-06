import json
import os
import time

class CocoToYolo:
    def __init__(
            self,
            input_coco_json_path: str,
        ) -> None:
        
        os.chdir(os.path.dirname(__file__))

        self.input_coco_json_path = os.path.abspath(input_coco_json_path)
        assert os.path.exists(self.input_coco_json_path), f"input_coco_json_path: {self.input_coco_json_path} does not exist"

    def __call__(self) -> None:
        self.process()

    def process(self) -> None:
        _start = time.time()
        with open(self.input_coco_json_path, "r") as f:
            coco_dataset = json.load(f)
        
        # create labels directory if it does not exists
        if not os.path.exists(os.path.join(os.path.dirname(self.input_coco_json_path), "labels")):
            os.makedirs(os.path.join(os.path.dirname(self.input_coco_json_path), "labels"))

        for image in coco_dataset["images"]:
            image_id = image["id"]
            image_file_name = image["file_name"]
            image_width = image["width"]
            image_height = image["height"]

            with open(os.path.join(os.path.dirname(self.input_coco_json_path), "labels", f"{image_file_name.split('.')[0]}.txt"), "w") as f:
                for annotation in coco_dataset["annotations"]:
                    if annotation["image_id"] == image_id:
                        x, y, w, h = annotation["bbox"]
                        x_center = x + w / 2
                        y_center = y + h / 2

                        x_center /= image_width
                        y_center /= image_height
                        w /= image_width
                        h /= image_height

                        f.write(f"{annotation['category_id']} {x_center} {y_center} {w} {h}\n")

        _end = time.time()
        print(f"Converting COCO to YOLO labels took: {_end - _start:.2f}s")
        
if __name__ == "__main__":
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__name__), "test", "sliced"))
    cocotoyolo = CocoToYolo(os.path.join(target_dir, ".temp.sliced_annotations.json"))