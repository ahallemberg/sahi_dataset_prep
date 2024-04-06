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
                _dict[cls].append(w*h)

    n_bbox_cls_0 = len(_dict[0])
    n_bbox_cls_1 = len(_dict[1])
    n_bbox_cls = n_bbox_cls_0 + n_bbox_cls_1                

    avg_bbox_area_cls_0 = round(sum(_dict[0])/len(_dict[0])*100,2)
    avg_bbox_area_cls_1 = round(sum(_dict[1])/len(_dict[1])*100,2)

    total_area_cls_0 = round(sum(_dict[0])/len(os.listdir(directory))*100,2)
    total_area_cls_1 = round(sum(_dict[1])/len(os.listdir(directory))*100,2)
    total_area_cls = round(total_area_cls_0 + total_area_cls_1,2)

    print("-"*20)
    print(f"Number of bounding boxes of class 0: {n_bbox_cls_0}")
    print(f"Number of bounding boxes of class 1: {n_bbox_cls_1}")
    print(f"Total number of bounding boxes: {n_bbox_cls}")
    print("-"*20)
    print(f"Average bbox area of class 0: {avg_bbox_area_cls_0}%")
    print(f"Average bbox area of class 1: {avg_bbox_area_cls_1}%")
    print("-"*20)
    print(f"Total area covered by class 0: {total_area_cls_0}%")
    print(f"Total area covered by class 1: {total_area_cls_1}%")
    print(f"Total area covered by both classes: {total_area_cls}%")
    print("-"*20)

target_dir = "/home/askhb/ascend/suas2023_detection_dataset/test/resized/labels"

get_bbox_area(target_dir)
print(f"Number of non-empty files: {count_non_empty_files(target_dir)} of {file_count(target_dir)} files")
