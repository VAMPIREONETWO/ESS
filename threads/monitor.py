from . import Thread, time
import numpy as np
from mss import mss
from PIL import Image
from threads.resources import image_resource


class Monitor(Thread):
    def __init__(self, screen):
        """

        :param screen: e.g. {"top": 0, "left": 0, "width": 1980, "height": 1080}
        """
        super().__init__()
        self.screen = screen

        # signals
        self.close = False
        self.pause = False

        # cache
        self.images = []

    def run(self):
        while not self.close:
            if not self.pause:
                # catch screen
                with mss() as sct:
                    screenshot = sct.grab(self.screen)

                # transformation
                img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
                img_np = np.array(img)

                # cache images
                self.images.append(img_np)

                # write to shared resources
                if image_resource.check_available("w"):
                    image_resource.add(self.images)
                    self.images.clear()
            else:
                if len(self.images) > 0:
                    self.images.clear()
                image_resource.clear()

            time.sleep(0.01)
