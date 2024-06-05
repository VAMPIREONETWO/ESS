import threading


class SharedResource(object):
    def __init__(self):
        self.resource = []
        self.counter = {"w": 0, "r": 0}
        self.signal = None
        self.lock = threading.RLock()

    def add(self, resource: list):
        self.resource.extend(resource)
        self.lock.release()

    def get(self):
        resource = self.resource.copy()
        self.resource.clear()
        self.lock.release()
        return resource

    def check_available(self, identity) -> bool:
        if self.signal is None:
            if self.lock.acquire(timeout=0.005):
                self.counter[identity] = 0
                return True
            else:
                self.counter[identity] += 1
                if self.counter[identity] == 5:
                    self.signal = identity
                    self.counter[identity] = 0
        else:
            if self.signal == identity:
                self.lock.acquire(timeout=0.005)
                self.signal = None
                return True
        return False

    def clear(self):
        if len(self.resource) > 0:
            self.lock.acquire()
            self.resource.clear()
            self.signal = None
            print("clear")
            self.lock.release()


image_resource = SharedResource()
error_resource = SharedResource()
