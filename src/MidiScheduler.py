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
            event (_type_): _description_
        """
        msg = [event.status, event.note, event.velocity]
        self.midi_out.send_message(msg)

    def schedule_events(self):
        """Schedule all NoteEvents for playback with appropriate timing."""
        if not self.events:
            return
        
        current_event = self.events.popleft()
        self.play_event(current_event)

        if self.events:
            next_event = self.events[0]
            threading.Timer(next_event.dt, self.schedule_events).start()

    def clear_events(self):
        """Clear all the scheduled MIDI events."""
        self.events.clear()
