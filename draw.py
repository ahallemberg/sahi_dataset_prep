import os 
from PIL import Image, ImageDraw

def draw_bbox_pil(im: Image, bboxes: list, color: str, width=5):
    draw = ImageDraw.Draw(im)
    for bbox in bboxes:  
        draw.rectangle(bbox, outline=color, width=width)

    im.show()
    
def get_bbox(line: str, img_width: int, img_height: int) -> tuple:
        line = line.split(" ")
        x_center, y_center, width, height = float(line[1]), float(line[2]), float(line[3]), float(line[4])
        x_min = x_center - (width / 2)
        y_min = y_center - (height / 2)
        x_max = x_center + (width / 2)
        y_max = y_center + (height / 2)
        return (x_min*img_width, y_min*img_height, x_max*img_width, y_max*img_height)
        

def main(target_dir: str, basename:str) :
    os.chdir(os.path.dirname(__file__))

    image_path = os.path.join(target_dir, "images", basename)
    label_path = os.path.join(target_dir, "labels", basename.split(".")[0]+".txt")
    im = Image.open(image_path)
    img_width, img_height = im.size
    
    bboxes = []
    
    with open(label_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            bboxes.append(get_bbox(line, img_width, img_height))

    print(bboxes)
    draw_bbox_pil(im, bboxes, "#ff0000", width=2)

    
if __name__ == "__main__":
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__name__), "test", "sliced"))
    imgs = os.listdir(os.path.join(target_dir, "images"))
    main(target_dir, "Image8835_0_0_1273_1273.png")
  
