import threading
from collections import deque
from dataclasses import dataclass
import rtmidi

from .DataClasses import NoteEvent

class MidiScheduler:
    def __init__(self, midi_out_port: rtmidi.MidiOut):
        """Initialize the MidiScheduler with an output port and an empty deque for event storage.

        Args:
            midi_out_port (rtmidi.MidiOut()): The RtMidi output object for sending messages.
        """
        self.midi_out = midi_out_port
        self.events = deque()

    def add_event(self, note_event: NoteEvent):
        """Add a new NoteEvent to the end of the deque.

        Args:
            note_event (NoteEvent): A NoteEvent object to be added.
        """
        self.events.append(note_event)

    def add_events(self, note_events: list[NoteEvent]):
        """Add multiple NoteEvents to the end of the deque.

        Args:
            note_events (list[NoteEvent]): A list of NoteEvent objects to be added.
        """
        self.events.extend(note_events)

    def play_event(self, event: NoteEvent):
        """Play a single NoteEvent and schedule the next one.

        Args:
            event (NoteEvent): The NoteEvent to play.
        """
        msg = [event.status, event.note, event.velocity]
        self.midi_out.send_message(msg)

    def schedule_events(self, initial_delay: int = 0):
        """Schedule all NoteEvents for playback with appropriate timing.

        Args:
            initial_delay (int): The delay in milliseconds before playing the first note.
        """
        if not self.events:
            return
        
        if initial_delay > 0:
            threading.Timer(initial_delay / 1000, self.play_events).start()
        else:
            self.play_events()

    def play_events(self):
        """Play the first event and schedule the subsequent events."""
        current_event = self.events.popleft()
        self.play_event(current_event)

        if self.events:
            next_event = self.events[0]
            threading.Timer(next_event.dt / 1000, self.schedule_events).start()

    def clear_events(self):
        """Clear all the scheduled MIDI events."""
        self.events.clear()
