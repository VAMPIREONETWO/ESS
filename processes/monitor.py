from . import time, Process, Queue, Event
import numpy as np
from PIL import Image
import win32gui
import win32ui
import win32con
import matplotlib.pyplot as plt


class Monitor(Process):
    def __init__(self, window_name, window_size, image_resource: Queue):
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
        self.image_resource = image_resource

        # signals
        self.close = Event()
        self.pause = Event()

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

        while not self.close.is_set():
            if not self.pause.is_set():
                # capture window content
                img = self.capture_window()

                # write to shared resources
                if not self.image_resource.full():
                    self.image_resource.put_nowait(img)
            else:
                if not self.image_resource.empty():
                    for _ in range(self.image_resource.qsize()):
                        self.image_resource.get_nowait()

            time.sleep(2)

        # release DC
        win32gui.DeleteObject(self.bitmap.GetHandle())
        self.save_dc.DeleteDC()
        self.mfc_dc.DeleteDC()
        win32gui.ReleaseDC(window, self.window_dc)

    def capture_window(self) -> np.ndarray:
        # copy window content to bitmap
        self.save_dc.BitBlt((0, 0), self.window_size, self.mfc_dc, (0, 0), win32con.SRCCOPY)

        # creat PIL image
        bmp_str = self.bitmap.GetBitmapBits(True)
        img = Image.frombuffer('RGB', self.window_size, bmp_str, 'raw',
                               'BGRX', 0, 1)
        return img
