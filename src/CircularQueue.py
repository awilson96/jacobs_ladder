import threading
import time

class CircularPriorityQueue:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()
        self.can_enqueue = threading.Condition(self.lock)
        self.last_dequeue_time = 0

    def dequeue(self):
        with self.lock:
            if not self.queue:
                print("Queue is empty! Cannot dequeue.")
                return None
            
            item = self.queue.pop(0)  # FIFO behavior
            self.last_dequeue_time = time.time() * 1000  # Milliseconds for precision
            print(f"Dequeued: {item} at {int(self.last_dequeue_time)} ms")
            
            # Notify any waiting enqueues that dequeue has completed
            self.can_enqueue.notify()
            return item

    def enqueue(self, item):
        with self.can_enqueue:
            # Wait if dequeue is in progress or another enqueue is pending
            while self.last_dequeue_time == 0 or len(self.queue) > 0:
                self.can_enqueue.wait()
            
            self.queue.append(item)
            enqueue_time = time.time() * 1000
            print(f"Enqueued: {item} at {int(enqueue_time)} ms")
            self.can_enqueue.notify()  # Signal next enqueue opportunity

    def enqueue_multiple(self, items):
        for item in items:
            self.enqueue(item)

# Example thread functions for enqueue and dequeue operations
def scheduled_dequeue(q, interval_ms):
    while True:
        time.sleep(interval_ms / 1000)  # Convert ms to seconds
        q.dequeue()

def controlled_enqueue(q, items, delay_ms):
    for item in items:
        time.sleep(delay_ms / 1000)  # Simulate delay between enqueues
        q.enqueue(item)

# Initialize queue and start threads
q = CircularPriorityQueue()

# Dequeue thread running at precise intervals
dequeue_thread = threading.Thread(target=scheduled_dequeue, args=(q, 28))

# Enqueue items with delays between them
enqueue_thread = threading.Thread(target=controlled_enqueue, args=(q, [1, 2, 3, 4, 5], 17))

dequeue_thread.start()
enqueue_thread.start()

dequeue_thread.join()
enqueue_thread.join()
