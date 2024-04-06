import os

def count_non_empty_files(directory):
    return sum(os.path.getsize(os.path.join(directory, file)) > 0 for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file)))

def file_count(directory):
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

def get_bbox_area(directory):
    _dict = {
        0: [],
        1: []
    }

    for file in os.listdir(directory):
        with open(os.path.join(directory, file), "r") as f:
            lines = f.readlines()
            for line in lines:
                cls, x, y, w, h = map(float, line.strip().split())
                cls = int(cls)
                #print(f"Class: {cls}, x: {x}, y: {y}, w: {w}, h: {h}")
                #print(f"Bounding box area: {w*h}")
                _dict[cls].append(w*h)
    print("-"*20)
    print(f"Number of bounding boxes of class 0: {len(_dict[0])}")
    print(f"Number of bounding boxes of class 1: {len(_dict[1])}")
    print(f"Total number of bounding boxes: {len(_dict[0]) + len(_dict[1])}")
    print("-"*20)
    print(f"Average bbox area of class 0: {sum(_dict[0])/len(_dict[0])}%")
    print(f"Average bbox area of class 1: {sum(_dict[1])/len(_dict[1])}%")
    print("-"*20)
    print(f"{sum(_dict[0])/len(os.listdir(directory))}% of total area covered by class 0")
    print(f"{sum(_dict[1])/len(os.listdir(directory))}% of total area covered by class 1")
    print(f"{(sum(_dict[0]) + sum(_dict[1])) / len(os.listdir(directory))}% total area covered by both classes")
    print("-"*20)

target_dir = "/home/askhb/ascend/suas2023_detection_dataset/test/sliced/labels"

get_bbox_area(target_dir)
print(f"Number of non-empty files: {count_non_empty_files(target_dir)} of {file_count(target_dir)} files")
