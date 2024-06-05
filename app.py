import time

from threads import Monitor, Detector, Listener, AudioPlayer
from threading import Thread


class ESS(Thread):
    """
    EVE support system
    """
    def __init__(self, screen):
        super().__init__()

        self.listener = Listener()
        self.screen = screen

        self.monitor = None
        self.detector = None
        self.audio_player = None

    def initialise(self):
        self.monitor = Monitor(self.screen)
        self.detector = Detector("data/eve_mine.pth")
        self.audio_player = AudioPlayer("data/audios")

    def run(self):
        self.initialise()
        self.listener.start()
        self.monitor.start()
        self.detector.start()
        self.audio_player.start()
        while True:
            if self.listener.e:
                self.exit()
                break
            elif self.listener.p:
                self.pause()
            elif self.listener.r:
                self.listener.r = False
                self.restart()

            time.sleep(0.01)

    def pause(self):
        self.monitor.pause = True
        self.detector.pause = True
        self.audio_player.pause = True

    def restart(self):
        self.monitor.pause = False
        self.detector.pause = False
        self.audio_player.pause = False

    def exit(self):
        self.monitor.close = True
        self.detector.close = True
        self.audio_player.close = True


if __name__ == '__main__':
    app = ESS({"top": 0, "left": 0, "width": 1980, "height": 1080})
    app.start()
    app.join()
