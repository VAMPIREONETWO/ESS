from . import time, Process,Queue,Event
import os

audio_map = {"nospace": "nospace.mp3",
             "noore": "noore.mp3",
             "empty": "empty.mp3"}
err_kinds = list(audio_map.keys())


class AudioPlayer(Process):
    def __init__(self, root, error_resource: Queue):
        super().__init__()
        self.root = root
        self.error_resource = error_resource

        # signals
        self.close = Event()
        self.pause = Event()

        # cache
        self.errors = []

    def run(self):
        import pygame
        pygame.mixer.init()
        while not self.close.is_set():
            if not self.pause.is_set():
                # read errors from error resource
                for _ in range(self.error_resource.qsize()):
                    self.errors.append(self.error_resource.get())

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
        import pygame
        pygame.mixer.music.load(os.path.join(self.root, file))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
