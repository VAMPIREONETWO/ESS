import numpy as np
from matplotlib import pyplot as plt

from . import time, Process, Queue, Event
import torch
from torchvision.transforms import ToTensor

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')


class Detector(Process):
    def __init__(self, model_path, image_resource: Queue, error_resource: Queue):
        super(Detector, self).__init__()

        self.image_resource = image_resource
        self.error_resource = error_resource

        # model
        self.model_path = model_path
        self.model = None

        # signals
        self.close = Event()
        self.pause = Event()

    def run(self):
        self.load_model()
        # i = 0
        while not self.close.is_set():
            if not self.pause.is_set():

                # read images from image resource
                if not self.image_resource.empty():
                    image = self.image_resource.get()

                    # if i < 10:
                    #     plt.imshow(image)
                    #     plt.show()
                    #     i += 1
                    self.predict(image)

            else:
                if not self.error_resource.empty():
                    for _ in range(self.error_resource.qsize()):
                        self.error_resource.get_nowait()
            time.sleep(1)

    def load_model(self):
        self.model = torch.load(self.model_path)
        self.model.to(device)
        self.model.eval()

    def predict(self, image):
        # predict objects
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
                if label == 1:
                    attack = True
                elif label == 2:
                    self.error_resource.put_nowait('nospace')
                elif label == 3:
                    self.error_resource.put_nowait('noore')
        if not attack:
            self.error_resource.put_nowait('empty')
