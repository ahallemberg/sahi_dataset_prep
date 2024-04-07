import os
from yolotococo import YoloToCoco
from cocotoyolo import CocoToYolo
from slicer import Slicer 

input_dir = "/home/askhb/ascend/suas2023_detection_dataset/test/resized"
output_dir = "/home/askhb/ascend/suas2023_detection_dataset/test/sliced"
categories=[{"id": 0, "name": "emergent"}, {"id": 1, "name": "standard"}]

slice_height = 1273
slice_width = 1273
overlap_ratio = 0.1358354805775648

def main(
        input_dir: str, 
        output_dir:str, 
        categories: list[dict[str, str|int]], 
        slice_height: int, 
        slice_width: int, 
        overlap_height_ratio: float, 
        overlap_width_ratio: float
    ) -> None:
 
    output_file_name = ".temp.annotations.json"

    print("Converting YOLO labels to COCO")
    yolo_to_coco = YoloToCoco(
        input_dir=input_dir,
        output_dir=output_dir,
        categories=categories,
        output_file_name=output_file_name,
        label_portion=0.2
    )
    yolo_to_coco()
    print("Conversion complete")

    input_coco_json_path = os.path.join(output_dir, output_file_name)
    output_coco_json_path = os.path.join(output_dir, ".temp.sliced_annotations")
    image_dir = os.path.join(input_dir,  "images")

    # create sliceed_images directory if it does not exists
    if not os.path.exists(os.path.join(output_dir, "images")):
        os.makedirs(os.path.join(output_dir, "images"))

    output_image_dir = os.path.join(output_dir, "images")

    print("Slicing images and generating COCO annotations...")
    slicer = Slicer(
        slice_height=slice_height,
        slice_width=slice_width,
        overlap_height_ratio=overlap_height_ratio,
        overlap_width_ratio=overlap_width_ratio,
        input_coco_json_path=input_coco_json_path,
        output_coco_json_path=output_coco_json_path,
        image_dir=image_dir,
        output_image_dir=output_image_dir,
        slice_portion=0.2
    )
    slicer()
    print("Slicing complete")

    # remove file .temp.annotations.json
    os.remove(input_coco_json_path)

    full_output_coco_json_path = output_coco_json_path + "_coco.json"

    print("Converting COCO annotations to YOLO format...")
    cocoToYolo = CocoToYolo(full_output_coco_json_path)
    cocoToYolo()
    print("Conversion complete")

    # remove file .temp.sliced_annotations_coco.json
    os.remove(full_output_coco_json_path)

    print("Done")


if __name__ == "__main__": 
    main(input_dir, output_dir, categories, slice_height, slice_width, overlap_ratio, overlap_ratio)
