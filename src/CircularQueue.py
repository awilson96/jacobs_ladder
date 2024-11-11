import threading
from time import sleep
from collections import deque

from .DataClasses import NoteEvent

class CircularQueue:
    def __init__(self):
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.circular_queue = deque()
        self.interrupt = False

    def dequeue(self) -> NoteEvent:
        """Dequeue items from the circular queue, stopping all enqueues by using a software interrupt

        Returns:
            NoteEvent: a NoteEvent dataclass for scheduling
        """
        self.interrupt = True
        with self.lock:
            if not self.circular_queue:
                print("Queue is emtpy!")
                return None
            item = self.circular_queue.popleft()
            self.condition.notify()
            self.interrupt = False
            return item

    def _enqueue(self, note_events: list[NoteEvent]) -> int | None:
        """Create an interruptable append process that can be exitted anytime whenever the dequeue method is called.  Only appends items one at a time
        checking at each iteration of the loop to see if the dequeue method has been called and exitting the function if so returning an index if interrupted.
        Returns None if the process was successful withoout interruption.

        Args:
            note_events (list[NoteEvent]): A list of NoteEvent(s) to be appended to the end of the deque()

        Returns:
            int | None: returns an int if the process was interrupted with the index where the process left off, 
                        None if the operation was successful without interruption
        """
        with self.condition:
            if isinstance(note_events, list):
                for index, note_event in enumerate(note_events):
                    # Check continously to see if the operation has been interrupted
                    if not self.interrupt:
                        self.circular_queue.append(note_event)
                    else:
                        return index
                return None
            else:
                raise TypeError(f"Expected a list of NoteEvent(s), instead got {type(note_events)}")
       
                
    def enqueue(self, note_events: list[NoteEvent]) -> None:
        """Enqueue new NoteEvents to the end of the deque() in a thread safe manner prioritizing dequeue operations. Do not stop until all NoteEvents in the 
        note_events list have been successfully added.

        Args:
            note_events (list[NoteEvent]): a list of NoteEvent(s) to be added to the end of the circular queue.
        """
        remaining_notes = note_events
        while remaining_notes:
            index_thread_left_off_at = self._enqueue(note_events=remaining_notes)
            if index_thread_left_off_at:
                remaining_notes = remaining_notes[index_thread_left_off_at:]
            else:
                return

if __name__ == "__main__":
    circularQueue = CircularQueue()


