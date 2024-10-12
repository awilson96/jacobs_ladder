import threading
from collections import deque
import rtmidi

from .DataClasses import NoteEvent
from .Dictionaries import get_midi_notes

class MidiScheduler:
    
    def __init__(self, midi_out_port: str = "jacob"):
        """Initialize the MidiScheduler with an output port and an empty deque for event storage.

        Args:
            midi_out_port (rtmidi.MidiOut()): The RtMidi output object for sending messages.
        """
        self.midi_out = rtmidi.MidiOut()
        self.output_port = midi_out_port
        self.events = deque()
        self.NOTE_ON_STATUS = 144
        self.NOTE_OFF_STATUS = 128
        
        self.initialize_port()
        self.int_note = get_midi_notes()
        
    def initialize_port(self):
        """Initialize the port specified in __init__ by opening that port for Midi out operations

        Raises:
            RuntimeError: If the port cannot be found, this funtion raises an error
        """
        try:
            available_output_ports = [port.split(" ", 1)[0] for port in self.midi_out.get_ports()]
            index = available_output_ports.index(self.output_port)
            self.midi_out.open_port(index)

        except (ValueError, rtmidi._rtmidi.SystemError):
            raise RuntimeError(f"Failed to open output port '{index}'")

    def add_event(self, note_event: NoteEvent):
        """Add a new NoteEvent to the end of the deque.

        Args:
            note_event (NoteEvent): A NoteEvent object to be added.
        """
        self.events.append(note_event)
        
    def add_event_with_duration(self, note_event: NoteEvent, duration: int):
        self.add_event(note_event=note_event)
        note_off_event = NoteEvent(
            dt=duration, note=note_event.note, status=self.NOTE_OFF_STATUS, velocity=note_event.velocity
            )
        self.events.append(note_off_event)

    def add_events(self, note_events: list[NoteEvent]):
        """Add multiple NoteEvents to the end of the deque.

        Args:
            note_events (list[NoteEvent]): A list of NoteEvent objects to be added.
        """
        self.events.extend(note_events)
    
    def add_events_with_duration(self, note_events: list[NoteEvent], durations: list[int]):
        assert(len(note_events) == len(durations))
        for note_event in note_events:
            self.add_event(note_event=note_event)
        for note_event, duration in zip(note_events, durations):
            self.add_event(note_event=NoteEvent(dt=duration, note=note_event.note, status=self.NOTE_OFF_STATUS, velocity=note_event.velocity))

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

if __name__ == "__main__":
    midi_scheduler = MidiScheduler(midi_out_port="jacob")
    midi_scheduler.add_event(note_event=NoteEvent(dt=0, note=60, status=144, velocity=100))
    midi_scheduler.add_events(note_events=[NoteEvent(dt=0, note=64, status=144, velocity=100), NoteEvent(dt=0, note=67, status=144, velocity=100)])
    midi_scheduler.add_events(note_events=[NoteEvent(dt=1000, note=60, status=128, velocity=100), NoteEvent(dt=0, note=64, status=128, velocity=100), NoteEvent(dt=0, note=67, status=128, velocity=100)])
    midi_scheduler.add_events_with_duration(note_events=[NoteEvent(dt=1000, note=62, status=144, velocity=100), NoteEvent(dt=0, note=65, status=144, velocity=100),NoteEvent(dt=0, note=69, status=144, velocity=100), NoteEvent(dt=0, note=72, status=144, velocity=100)], durations=[1000, 0, 0, 0])
    midi_scheduler.add_events_with_duration(note_events=[NoteEvent(dt=1000, note=64, status=144, velocity=100), NoteEvent(dt=0, note=67, status=144, velocity=100),NoteEvent(dt=0, note=71, status=144, velocity=100), NoteEvent(dt=0, note=72, status=144, velocity=100)], durations=[1000, 0, 0, 0])
    midi_scheduler.add_events_with_duration(note_events=[NoteEvent(dt=1000, note=62, status=144, velocity=100), NoteEvent(dt=0, note=65, status=144, velocity=100),NoteEvent(dt=0, note=69, status=144, velocity=100), NoteEvent(dt=0, note=72, status=144, velocity=100)], durations=[1000, 0, 0, 0])
    midi_scheduler.add_events_with_duration(note_events=[NoteEvent(dt=1000, note=60, status=144, velocity=100), NoteEvent(dt=0, note=64, status=144, velocity=100),NoteEvent(dt=0, note=67, status=144, velocity=100), NoteEvent(dt=0, note=71, status=144, velocity=100)], durations=[1000, 0, 0, 0])
    midi_scheduler.schedule_events(initial_delay=1000)
    
    # Expected sequence:
    # initial delay of 1000 ms
    # 
    # Epoch begins at 0 ms
    # C E G note_on at 0 ms
    # C E G note_off at 1000 ms
    # D E F G note_on at 2000 ms
    # D E F G note_off at 3000 ms
    # E G B C note_on at 4000 ms
    # E G B C note_off at 5000 ms
    # D E F G note_on at 6000 ms
    # D E F G note_off at 7000 ms
    # C E G B note_on at 8000 ms
    # C E G B note_off at 9000 ms
    