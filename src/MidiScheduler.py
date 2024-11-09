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
        self.stash = []
        self.playing = False
        
        self.CONTROL_CHANGE_STATUS = 176
        self.SUSTAIN_PEDAL_NOTE = 64
        self.MAX_VELOCITY = 127
        self.MIN_VELOCITY = 0
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

    def add_event(self, note_event: NoteEvent, stash: bool = False):
        """Add a new NoteEvent to the end of the deque.

        Args:
            note_event (NoteEvent): A NoteEvent object to be added.
        """
        self.events.append(note_event) if not stash else self.stash.append(note_event)
        
    def add_event_with_duration(self, note_event: NoteEvent, duration: int, stash: bool = False):
        self.add_event(note_event=note_event, stash=stash)
        note_off_event = NoteEvent(
            dt=duration, note=note_event.note, status=self.NOTE_OFF_STATUS, velocity=note_event.velocity
            )
        self.events.append(note_off_event) if not stash else self.stash.append(note_off_event)

    def add_events(self, note_events: list[NoteEvent], stash: bool = False):
        """Add multiple NoteEvents to the end of the deque.

        Args:
            note_events (list[NoteEvent]): A list of NoteEvent objects to be added.
        """
        self.events.extend(note_events) if not stash else self.stash.extend(note_events)
    
    def add_events_with_duration(self, note_events: list[NoteEvent], durations: list[int], stash: bool = False):
        assert(len(note_events) == len(durations))
        for note_event in note_events:
            self.add_event(note_event=note_event, stash=stash)
        for note_event, duration in zip(note_events, durations):
            self.add_event(note_event=NoteEvent(dt=duration, note=note_event.note, status=self.NOTE_OFF_STATUS, velocity=note_event.velocity), stash=stash)
            
    def add_sustain_pedal_event(self, duration: int, sustain: bool, stash: bool = False):
        if duration <= -1:
            assert(len(self.events) >= abs(duration))
            duration = self.events[duration].dt
        if sustain:
            self.add_event(note_event=NoteEvent(dt=duration, note=self.SUSTAIN_PEDAL_NOTE, status=self.CONTROL_CHANGE_STATUS, velocity=self.MAX_VELOCITY), stash=stash)
        else:
            self.add_event(note_event=NoteEvent(dt=duration, note=self.SUSTAIN_PEDAL_NOTE, status=self.CONTROL_CHANGE_STATUS, velocity=self.MIN_VELOCITY), stash=stash)

    def schedule_events(self, initial_delay: int = 0):
        """Schedule all NoteEvents for playback with appropriate timing.

        Args:
            initial_delay (int): The delay in milliseconds before playing the first note.
        """
        
        # If there are no events left to process then set playing to false and return
        if len(self.events) == 0:
            print("No more events")
            self.playing = False
            return
            
        self.playing = True
    
        # Schedule events
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
        else:
            self.playing = False
            threading.Timer(0, self.schedule_events).start()

    def play_event(self, event: NoteEvent):
        """Play a single NoteEvent and schedule the next one.

        Args:
            event (NoteEvent): The NoteEvent to play.
        """
        msg = [event.status, event.note, event.velocity]
        self.midi_out.send_message(msg)

    def sort_events_by_dt(self, relative: bool, stash: bool = False):
        """Sort the events by their dt attribute and convert to relative time."""
        if not stash:
            sorted_events = sorted(self.events, key=lambda event: event.dt)

            if relative:
                last_dt = 0  
                for event in sorted_events:
                    event.dt -= last_dt
                    last_dt += event.dt

            self.events = deque(sorted_events)
        else:
            sorted_events = sorted(self.stash, key=lambda event: event.dt)

            if relative:
                last_dt = 0  
                for event in sorted_events:
                    event.dt -= last_dt
                    last_dt += event.dt

            self.stash = deque(sorted_events)

    def pop_stash(self):
        self.events.extend(self.stash) 
        self.stash = []

    def get_absolute_length(self) -> int:
        """Return the amount of time of scheduled events total if using absolute time 

        Returns:
            int: the amount of time allocated for events 
        """
        return self.events[-1].dt / 1000

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
    