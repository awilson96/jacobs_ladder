class InOutQueue:
    def __init__(self, size: int):
        """Create an in out queue of a specified size

        Args:
            size (int): the size of the number of records you wish to hold at one time
        """
        self.queue = []
        self.size = size

    def enqueue(self, elem):
        """Enqueue a new item by popping off the oldest item

        Args:
            elem (Any): any element you wish to enqueue
        """
        self.queue.append(elem)
        if len(self.queue) > self.size:
            self.queue.pop(0)  # Remove the oldest element at index 0

    def get_queue(self):
        """Get the current queue

        Returns:
            list[Any]: A list of objects representing the queue
        """
        return self.queue