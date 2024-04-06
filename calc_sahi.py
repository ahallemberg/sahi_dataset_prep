# Constants for sensor dimensions and object size in some unit
SENSOR_WIDTH = 4656 
SENSOR_HEIGHT = 3496

OBJECT_SIZE_Y = 142.27105978261
OBJECT_SIZE_X = 172.91856677524

N_SLICES = 20

# Constants for slicing dimensions and inference dimensions
INFERENCE_HEIGHT = 640
INFERENCE_WIDTH = 640

def sahi_calculate_slice_regions(image_height, image_width):
    # Calculate slice regions for an image given its dimensions
    
    # Calculations for moving step in both dimensions
    step_height = INFERENCE_HEIGHT - int(INFERENCE_HEIGHT * overlap_height_ratio_)
    step_width = INFERENCE_WIDTH - int(INFERENCE_WIDTH * overlap_width_ratio_)

    # Estimate number of slices to initialize the list with adequate size
    regions = []
    index = 0

    # Generate regions to slice
    for y in range(0, image_height, step_height):
        for x in range(0, image_width, step_width):
            width = INFERENCE_WIDTH
            height = INFERENCE_HEIGHT
            temp_x = x
            temp_y = y

            # Adjust slice dimensions if they exceed image boundaries
            if x + width > image_width:
                temp_x -= (x + width) - image_width
            if y + height > image_height:
                temp_y -= (y + height) - image_height

            regions.append(((temp_x, temp_y, width, height), index))
            index += 1

    return regions

def sahi_approximated_num_slices(number_of_slices, original_height, original_width, overlap_pixels) -> tuple[int, int, int]:
    # Approximate the number of slices and dimensions based on desired overlap and number of slices
    
    # Setting global variables for overlap ratios
    global overlap_width_ratio_
    global overlap_height_ratio_

    overlap_width_ratio_ = overlap_pixels / INFERENCE_WIDTH
    overlap_height_ratio_ = overlap_pixels / INFERENCE_HEIGHT

    # Ratio of height to width of the original image
    height_to_width = original_height / original_width

    # Initialize variables to find the closest match to desired number of slices
    closest_number_of_slices = -1000
    input_height = 0
    input_width = 0

    # Iterate through possible widths to find the closest match
    for width in range(INFERENCE_WIDTH, 8000):
        candidate_height = int(height_to_width * width)
        candidate_slices = len(sahi_calculate_slice_regions(candidate_height, width))
        candidate_diff = abs(number_of_slices - candidate_slices)
        current_diff = abs(number_of_slices - closest_number_of_slices)
        
        # Update closest match if a better one is found
        if candidate_diff < current_diff or \
                (candidate_diff == current_diff and \
                 abs(candidate_height - original_height) <= abs(input_height - original_height)):

            closest_number_of_slices = candidate_slices
            input_height = candidate_height
            input_width = width

    # Calculate new slice dimensions based on ratio adjustments
    height_ratio = original_height / input_height
    width_ratio = original_width / input_width
    new_slice_height = round(INFERENCE_HEIGHT * height_ratio)
    new_slice_width = round(INFERENCE_WIDTH * width_ratio)

    return closest_number_of_slices, new_slice_height, new_slice_width

if __name__ == "__main__":
    n_slices, sh, sw = sahi_approximated_num_slices(N_SLICES, SENSOR_HEIGHT, SENSOR_WIDTH, max(OBJECT_SIZE_Y, OBJECT_SIZE_X))

    print(f"For the wanted number of {n_slices} slices, slice_height: {sh}, slice_width: {sw}")
    print(f"The overlap_ratio should be: {max(OBJECT_SIZE_Y/sh, OBJECT_SIZE_X/sw)}")
    print(f"That gives a downscale on inference 640x640 slices of {sw/INFERENCE_WIDTH}x{sh/INFERENCE_HEIGHT}")
