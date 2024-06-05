from . import Thread
from pynput import keyboard


class Listener(Thread):

    def __init__(self):
        super().__init__()
        self.p = False
        self.e = False
        self.r = False
        self.listener = keyboard.GlobalHotKeys({'<ctrl>+<alt>+p': self.pause,
                                                '<ctrl>+<alt>+e': self.exit,
                                                '<ctrl>+<alt>+r': self.restart})

    def run(self):
        self.listener.run()

    def pause(self):
        self.p = True

    def exit(self):
        self.e = True
        self.listener.stop()

    def restart(self):
        self.r = True
        self.p = False
