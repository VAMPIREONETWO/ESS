from . import Thread, time
from threads.resources import error_resource
import os
import pygame

audio_map = {"nospace": "nospace.mp3",
             "nomine": "nomine.mp3",
             "empty": "empty.mp3"}
err_kinds = list(audio_map.keys())


class AudioPlayer(Thread):
    def __init__(self, root):
        super().__init__()
        self.root = root
        pygame.mixer.init()

        # signals
        self.close = False
        self.pause = False

        # cache
        self.errors = []

    def run(self):
        while not self.close:
            if not self.pause:
                # read errors from error resource
                if error_resource.check_available("r"):
                    self.errors.extend(error_resource.get())

                # find main error
                counts = []
                for err in err_kinds:
                    counts.append(self.errors.count(err))
                if max(counts) > 0:
                    idx = counts.index(max(counts))
                    self.play(audio_map[err_kinds[idx]])
                    print(err_kinds[idx])

                # clear cache
                self.errors.clear()
            else:
                if len(self.errors) > 0:
                    self.errors.clear()
            time.sleep(1)

    def play(self, file):
        pygame.mixer.music.load(os.path.join(self.root, file))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
