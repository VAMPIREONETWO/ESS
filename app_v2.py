import time
from processes import Monitor, Detector, AudioPlayer, Listener
from multiprocessing import Queue


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

        # resources
        self.image_resource = Queue(60)
        self.error_resource = Queue(60)

        # processes
        self.monitor = Monitor(window_name, window_size, self.image_resource)
        self.detector = Detector("assets/models/eve_mining.pth", self.image_resource, self.error_resource)
        self.audio_player = AudioPlayer("assets/audios", self.error_resource)

        self.start()

    def start(self):
        self.monitor.start()
        self.detector.start()
        self.audio_player.start()

    def run(self):
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
        self.monitor.pause.set()
        self.detector.pause.set()
        self.audio_player.pause.set()

    def restart(self):
        self.monitor.pause.clear()
        self.detector.pause.clear()
        self.audio_player.pause.clear()

    def exit(self):
        self.monitor.close.set()
        self.detector.close.set()
        self.audio_player.close.set()
        self.monitor.join()
        self.detector.join()
        self.audio_player.join()


if __name__ == '__main__':
    app = ESS('雷电模拟器-1', (1600, 900))
    app.run()
