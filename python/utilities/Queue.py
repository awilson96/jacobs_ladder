class InOutQueue:
    def __init__(self, size):
        self.queue = []
        self.size = size

    def enqueue(self, elem):
        self.queue.append(elem)
        if len(self.queue) > self.size:
            self.queue.pop(0)  # Remove the oldest element at index 0

    def get_queue(self):
        return self.queue