from . import Thread, time
import numpy as np
from mss import mss
from PIL import Image
from threads.resources import image_resource
import win32gui
import win32ui
import win32con


class Monitor(Thread):
    def __init__(self, window_name, window_size):
        """

        :param screen: e.g. {"top": 0, "left": 0, "width": 1980, "height": 1080}
        """
        super(Monitor, self).__init__()
        self.bitmap = None
        self.save_dc = None
        self.mfc_dc = None
        self.window_dc = None
        self.window_name = window_name
        self.window_size = window_size

        # signals
        self.close = False
        self.pause = False

        # cache
        self.images = []

    def run(self):
        # DC (device context)
        window = win32gui.FindWindow(None, self.window_name)
        self.window_dc = win32gui.GetWindowDC(window)
        self.mfc_dc = win32ui.CreateDCFromHandle(self.window_dc)
        self.save_dc = self.mfc_dc.CreateCompatibleDC()

        # create bitmap
        self.bitmap = win32ui.CreateBitmap()
        self.bitmap.CreateCompatibleBitmap(self.mfc_dc, self.window_size[0], self.window_size[1])
        self.save_dc.SelectObject(self.bitmap)

        while not self.close:
            if not self.pause:
                # capture window content
                img = self.capture_window()

                # cache images
                self.images.append(img)

                # write to shared resources
                if image_resource.check_available("w"):
                    image_resource.add(self.images)
                    self.images.clear()
            else:
                if len(self.images) > 0:
                    self.images.clear()
                image_resource.clear()

            time.sleep(0.02)

    def capture_window(self) -> np.ndarray:
        # copy window content to bitmap
        self.save_dc.BitBlt((0, 0), self.window_size, self.mfc_dc, (0, 0), win32con.SRCCOPY)

        # creat PIL image
        bmp_str = self.bitmap.GetBitmapBits(True)
        img = Image.frombuffer('RGB', self.window_size, bmp_str, 'raw',
                               'BGRX', 0, 1)
        return img
