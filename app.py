import time

from threads import Monitor, Detector, Listener, AudioPlayer
from threading import Thread


class ESS(object):
    """
    EVE support system
    """

    def __init__(self, window_name, window_size):
        super().__init__()

        self.window_name = window_name
        self.window_size = window_size

        # listener process
        self.listener = Listener()
        self.listener.start()

        self.monitor = Monitor(window_name, window_size)
        self.detector = Detector("assets/models/eve_mining.pth")
        self.audio_player = AudioPlayer("assets/audios")

    def run(self):
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
    app = ESS('雷电模拟器-1', (1600, 900))
    app.run()
