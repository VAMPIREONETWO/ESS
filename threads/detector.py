from . import Thread, time
from threads.resources import image_resource, error_resource
import torch
from torchvision.transforms import ToTensor

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')


class Detector(Thread):
    def __init__(self, model_path):
        super().__init__()

        # load model
        self.model = torch.load(model_path)
        self.model.to(device)
        self.model.eval()

        # signals
        self.close = False
        self.pause = False

        # caches
        self.images = []
        self.errors = []

    def run(self):
        while not self.close:
            if not self.pause:
                # read images from image resource
                if image_resource.check_available("r"):
                    self.images.extend(image_resource.get())

                # handle images
                if len(self.images) < 10:
                    for _ in range(len(self.images)):
                        self.predict()
                else:
                    for _ in range(10):
                        self.predict()

                # write errors to error resource
                if error_resource.check_available("w"):
                    error_resource.add(self.errors)
                    self.errors.clear()
            else:
                if len(self.images) > 0:
                    self.images.clear()
                if len(self.errors) > 0:
                    self.errors.clear()
                error_resource.clear()
            time.sleep(0.01)

    def predict(self):
        # predict objects
        image = self.images[0]
        self.images.remove(image)
        image = ToTensor()(image).to(device)
        with torch.no_grad():
            output = self.model([image])

        # judge error
        detections = output[0]
        labels = detections['labels']
        scores = detections['scores']
        attack = False
        for i in range(len(labels)):
            if scores[i] > 0.9:
                label = labels[i]
                if label == 2:
                    attack = True
                elif label == 3:
                    self.errors.append('nospace')
                elif label == 4:
                    self.errors.append('nomine')
        if not attack:
            self.errors.append('empty')
