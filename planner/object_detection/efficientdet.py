from PIL import Image
from PIL import ImageDraw
from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pathlib import Path

def draw_objects(draw, objs, labels):
  """Draws the bounding box and label for each object."""
  for obj in objs:
    bbox = obj.bbox
    draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)],
                   outline='red')
    draw.text((bbox.xmin + 10, bbox.ymin + 10),
              '%s\n%.2f' % (labels.get(obj.id, obj.id), obj.score),
              fill='red')

class EfficientDet():
    def __init__(self):
        base_dir = Path(__file__).parent.absolute()
        labels_path = (base_dir / 'coco.txt').as_posix()
        model_path = (base_dir / 'models' / 'efficientdet_lite3_512_ptq_edgetpu.tflite').as_posix()

        self.threshold = 0.25
        self.labels = read_label_file(labels_path)
        self.interpreter = make_interpreter(model_path)
        self.interpreter.allocate_tensors()

    def detect(self, image, draw=False):
        pil_image = Image.fromarray(image)

        _, scale = common.set_resized_input(
            self.interpreter, pil_image.size, lambda size: pil_image.resize(size, Image.LANCZOS)
        )
        
        self.interpreter.invoke()
        objs_raw = detect.get_objects(self.interpreter, self.threshold, scale)

        objs = []
        for obj in objs_raw:
            objs.append({
                'label': self.labels.get(obj.id, obj.id),
                'score': obj.score,
                'bbox': {
                    'xmin': int(obj.bbox.xmin),
                    'ymin': int(obj.bbox.ymin),
                    'xmax': int(obj.bbox.xmax),
                    'ymax': int(obj.bbox.ymax)
                }     
            })
        
        if draw:
            pil_image = pil_image.convert('RGB')
            draw_objects(ImageDraw.Draw(pil_image), objs_raw, self.labels)
            pil_image.show()

        return objs