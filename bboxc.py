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
                print(f"Class: {cls}, x: {x}, y: {y}, w: {w}, h: {h}")
                print(f"Bounding box area: {w*h}")
                _dict[cls].append(w*h)

    area_0 = sum(_dict[0])/len(_dict[0]) * 100
    area_1 = sum(_dict[1])/len(_dict[1]) * 100
    print(f"{area_0:.2f}% of area covered by class 0")
    print(f"{area_1:.2f}% of area covered by class 1")
    print(f"{area_0 + area_1:.2f}% of area covered by bboxes")

target_dir = os.path.abspath(os.path.join(os.path.dirname(__name__), "test", "sliced", "labels"))

print(f"Number of non-empty files: {count_non_empty_files(target_dir)} of {file_count(target_dir)} files")
get_bbox_area(target_dir)