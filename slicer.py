import os
from sahi.slicing import slice_coco, slice_image
from tqdm import tqdm
import time

class Slicer:
    # Initializes the Slicer object with parameters for slicing operations and paths for input/output.
    def __init__(
            self, 
            slice_height: int,  # Height of each slice
            slice_width: int,  # Width of each slice
            overlap_height_ratio: float,  # Ratio of overlap between slices vertically
            overlap_width_ratio: float,  # Ratio of overlap between slices horizontally
            input_coco_json_path: str,  # Path to the input COCO annotation file
            output_coco_json_path: str,  # Path for saving the output COCO annotation file
            image_dir: str,  # Directory of images to be sliced
            output_image_dir: str,  # Directory for saving the sliced images,
            slice_portion: float = 1.0  # Portion of the dataset to use for slicing

        ) -> None: 
        os.chdir(os.path.dirname(__file__))  # Change the current working directory to the script's directory

        # Store the parameters as instance attributes
        self.slice_height = slice_height
        self.slice_width = slice_width  
        self.overlap_height_ratio = overlap_height_ratio
        self.overlap_width_ratio = overlap_width_ratio
        self.slice_portion = slice_portion

        self.input_coco_json_path = input_coco_json_path
        self.output_coco_json_path = output_coco_json_path
        self.image_dir = image_dir
        self.output_image_dir = output_image_dir

        # Assert that the specified paths exist
        assert os.path.exists(self.input_coco_json_path), f"input_coco_json_path: {self.input_coco_json_path} does not exist"
        assert os.path.exists(self.image_dir), f"image_dir: {self.image_dir} does not exist"

    # Callable method that initiates the creation of slices and the corresponding COCO annotations.
    def __call__(self) -> None: 
        self.create_slices()
        self.create_coco()

    # Processes each image in the directory, slicing it according to the specified dimensions and overlap ratios.
    def create_slices(self) -> None: 
        _start = time.time()
        for image_basename in tqdm(os.listdir(self.image_dir)[:int(len(os.listdir(self.image_dir)) * self.slice_portion)]):
            image_path = os.path.join(self.image_dir, image_basename)  # Construct the full image path
            print(image_path)  # Debugging print to show the current image path
            print(os.path.isfile(image_path))  # Debugging print to check if the path points to a file

            # Slice the image with the given parameters and save the results in the specified output directory
            slice_image_result = slice_image(
                image=image_path,
                output_file_name=image_basename.split('.')[0],  # Use the image name without the extension for output files
                output_dir=self.output_image_dir,
                verbose=True,  # Enable detailed logging
                slice_height=self.slice_height,
                slice_width=self.slice_width,
                overlap_height_ratio=self.overlap_height_ratio,
                overlap_width_ratio=self.overlap_width_ratio
            )           

            print(slice_image_result)  # Print the result of the slicing operation for debugging
        
        _end = time.time()
        print(f"Creating slices took: {_end - _start:.2f}s")


    # Generates a new COCO annotation file for the sliced images, preserving object annotations.
    def create_coco(self) -> None: 
        _start = time.time()
        slice_coco(
            image_dir=self.image_dir,  # The original directory of images
            coco_annotation_file_path=self.input_coco_json_path,  # Path to the original COCO annotations
            output_coco_annotation_file_name=self.output_coco_json_path,  # Path for the output COCO annotations
            output_dir=self.output_image_dir,  # Directory where the sliced images have been saved
            slice_height=self.slice_height,
            slice_width=self.slice_width,
            overlap_height_ratio=self.overlap_height_ratio,
            overlap_width_ratio=self.overlap_width_ratio
        )
        
        _end = time.time()
        print(f"Creating COCO lables took: {_end - _start:.2f}s")
