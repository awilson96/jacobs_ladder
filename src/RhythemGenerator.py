from bidict import bidict

from .DataClasses import IntervalScale, NoteEvent, RhythemNoteEvent
from .Dictionaries import notes_to_midi
from .Enums import NoteDivisions, MidiStatus
from .MidiScheduler import MidiScheduler


class RhythmGenerator:
    SECONDS_IN_MINUTE = 60

    def __init__(self, tempo: int):
        """Initialize the RhythmGenerator with a tempo and a MidiScheduler instance.

        Args:
            tempo (int): the tempo of the rhythems you wish to produce
        """
        self.note_str_to_int = bidict(notes_to_midi)
        self.tempo = tempo
        self.midi_scheduler = MidiScheduler()
        self.note_divisions_ms = NoteDivisions
        self.midi_status = MidiStatus
    
    def add_event(self, rhythem_note_event: RhythemNoteEvent):
        """Add an event using a more intuitive RhythemNoteEvent dataclass

        Args:
            rhythem_note_event (RhythemNoteEvent): a RhythemNoteEvent dataclass to add to the event sequence
        """
        note_event = NoteEvent(dt=self.division_to_dt(division=rhythem_note_event.division), 
                               note=self.note_str_to_int[rhythem_note_event.note], 
                               status=self.midi_status[rhythem_note_event.status].value,
                               velocity=rhythem_note_event.velocity)
        self.midi_scheduler.add_event(note_event=note_event)
        
    def add_event_with_duration(self, rhythem_note_event: RhythemNoteEvent, duration_division: str):
        """Add a single note with a specified duration expressed as a duration division. This method is useful if you
        only plan on playing one note for the whole duration division with no other held notes

        Args:
            rhythem_note_event (RhythemNoteEvent): a RhythemNoteEvent dataclass to add NOTE_ON and NOTE_OFF messages for
            duration_division (str): the division length for which the note should play (i.e. quarter_note, half_note, etc)
        """
        note_event = NoteEvent(dt=self.division_to_dt(division=rhythem_note_event.division), 
                               note=self.note_str_to_int[rhythem_note_event.note], 
                               status=self.midi_status[rhythem_note_event.status].value,
                               velocity=rhythem_note_event.velocity)
        
        self.midi_scheduler.add_event(note_event=note_event)
        note_off_event = NoteEvent(dt=self.division_to_dt(division=duration_division),
                                   note=note_event.note,
                                   status=self.midi_status.NOTE_OFF.value,
                                   velocity=note_event.velocity)
        self.midi_scheduler.add_event(note_off_event)
        
    def add_events(self, rhythem_note_events: list[RhythemNoteEvent]):
        """Add multiple RhythemNoteEvents

        Args:
            rhythem_note_events (list[RhythemNoteEvent]): a list of RhythemNoteEvent dataclasses to add to the event queue
        """
        for rhythem_note_event in rhythem_note_events:
            note_event = NoteEvent(dt=self.division_to_dt(division=rhythem_note_event.division), 
                                   note=self.note_str_to_int[rhythem_note_event.note], 
                                   status=self.midi_status[rhythem_note_event.status].value, 
                                   velocity=rhythem_note_event.velocity)
            self.midi_scheduler.add_event(note_event=note_event)
            
    def add_events_with_duration(self, rhythem_note_events: list[RhythemNoteEvent], duration_divisions: list[str]):
        """Add multiple multiple notes with a specified duration expressed as a duration division. This method is useful
        for playing a sequence individual notes for the whole duration of each notes division with no other held notes. 

        Args:
            rhythem_note_events (list[RhythemNoteEvent]): a list of RhythemNoteEvents for adding to the event queue
            duration_divisions (list[str]): a list of duration divisions marking the placement of the NOTE_OFF event as 
                a time offset from the NOTE_ON event. Note that the duration_divisions must be less than or equal to
                the division parameter of each individual note for the function to work properly.
        """
        assert(len(rhythem_note_events) == len(duration_divisions))
        for rhythem_note_event, duration_division in zip(rhythem_note_events, duration_divisions):
            note_event = NoteEvent(dt=self.division_to_dt(division=rhythem_note_event.division), 
                                   note=self.note_str_to_int[rhythem_note_event.note], 
                                   status=self.midi_status[rhythem_note_event.status].value, 
                                   velocity=rhythem_note_event.velocity)

            self.midi_scheduler.add_event(note_event=note_event)
        
            note_off_event = NoteEvent(dt=self.division_to_dt(duration_division), 
                                       note=self.note_str_to_int[rhythem_note_event.note], 
                                       status=self.midi_status.NOTE_OFF.value, 
                                       velocity=rhythem_note_event.velocity)
            self.midi_scheduler.add_event(note_off_event)
            
    def add_sustain_pedal_event(self, division_duration: str, sustain: bool):
        self.midi_scheduler.add_sustain_pedal_event(duration=self.division_to_dt(division_duration), sustain=sustain)
        
    def construct_scale(self, interval_scale: IntervalScale, duration_divisions: list[str], direction: str):
        """Construct a scale for playing back to the user which has direction ascending 'ASC', descending 'DESC', 
        or both 'BOTH'

        Args:
            interval_scale (IntervalScale): IntervalScale object containing the blueprint for how to play an arbitrary scale
            duration_divisions (list[str]): The time offsets expressed as note divisions from NOTE_ON to NOTE_OFF messages.
                Note that the duration_divisions must be less than or equal to their corresponding note division for the
                function to work properly.
            direction (str): 'ASC', 'DESC', or 'BOTH'

        Raises:
            ValueError: if an invalid direction is selected
        """
        valid_directions = ['ASC', 'DESC', 'BOTH']
        if direction not in valid_directions:
            raise ValueError(f"The direction you provided '{direction}', is not valid. "
                                "\nPlease provide one of the following directions: " + ", ".join(valid_directions))
        
        rhythem_note_events = [RhythemNoteEvent(division=interval_scale.divisions[0], 
                                                note=self.note_str_to_int.inv[interval_scale.starting_note], 
                                                status='NOTE_ON',
                                                velocity=interval_scale.velocities[0])]
        for index, interval in enumerate(interval_scale.intervals, start=1):
            rhythem_note_events.append(RhythemNoteEvent(division=interval_scale.divisions[index],
                                                        note=self.note_str_to_int.inv[self.note_str_to_int[rhythem_note_events[index-1].note] + interval], 
                                                        status='NOTE_ON', 
                                                        velocity=interval_scale.velocities[index]))
        if direction == 'ASC':
            self.add_events_with_duration(rhythem_note_events=rhythem_note_events, duration_divisions=duration_divisions)
        elif direction == 'DESC':
            self.add_events_with_duration(rhythem_note_events=rhythem_note_events[::-1], duration_divisions=duration_divisions)
        elif direction == 'BOTH':
            self.add_events_with_duration(rhythem_note_events=rhythem_note_events, duration_divisions=duration_divisions)
            self.add_events_with_duration(rhythem_note_events=rhythem_note_events[::-1][1:], duration_divisions=duration_divisions[1:])
    
    def division_to_dt(self, division: str) -> int:
        """Convert a rhythmic division to a time delay (dt) in milliseconds.

        Args:
            division (str): The rhythmic division (e.g., 'WHOLE', 'HALF', 'QUARTER', 'EIGHTH', 'SIXTEENTH').

        Returns:
            int: The delay time in milliseconds.
        """
        try:
            division_ms = self.note_divisions_ms[division.upper()].value
        except KeyError:
            raise ValueError(f"Invalid division: {division}")
        
        return int(division_ms * (self.SECONDS_IN_MINUTE / self.tempo))
            
    def set_tempo(self, tempo: int):
        """Set a new tempo for the RhythmGenerator.

        Args:
            tempo (int): The new tempo in beats per minute.
        """
        self.tempo = tempo

if __name__ == "__main__":
    rhythem_generator = RhythmGenerator(tempo=120)
    rhythem_generator.add_event(RhythemNoteEvent(division="ZERO", note="C4", status="NOTE_ON", velocity=100))
    rhythem_generator.add_event(RhythemNoteEvent(division="ZERO", note="E4", status="NOTE_ON", velocity=100))
    rhythem_generator.add_event(RhythemNoteEvent(division="ZERO", note="G4", status="NOTE_ON", velocity=100))
    rhythem_generator.add_event(RhythemNoteEvent(division="ZERO", note="B4", status="NOTE_ON", velocity=100))
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="ZERO", note="C5", status="NOTE_ON", velocity=100), duration_division="QUARTER")
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="ZERO", note="D5", status="NOTE_ON", velocity=100), duration_division="QUARTER")
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="ZERO", note="E5", status="NOTE_ON", velocity=100), duration_division="QUARTER")
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="ZERO", note="F5", status="NOTE_ON", velocity=100), duration_division="QUARTER")
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="ZERO", note="G5", status="NOTE_ON", velocity=100), duration_division="QUARTER")
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="ZERO", note="A5", status="NOTE_ON", velocity=100), duration_division="QUARTER")
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="ZERO", note="B5", status="NOTE_ON", velocity=100), duration_division="QUARTER")
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="ZERO", note="C6", status="NOTE_ON", velocity=100), duration_division="QUARTER")
    
    rhythem_generator.add_event(RhythemNoteEvent(division="ZERO", note="C4", status="NOTE_OFF", velocity=100))
    rhythem_generator.add_event(RhythemNoteEvent(division="ZERO", note="E4", status="NOTE_OFF", velocity=100))
    rhythem_generator.add_event(RhythemNoteEvent(division="ZERO", note="G4", status="NOTE_OFF", velocity=100))
    rhythem_generator.add_event(RhythemNoteEvent(division="ZERO", note="B4", status="NOTE_OFF", velocity=100))
    rhythem_generator.add_events(rhythem_note_events=[RhythemNoteEvent(division="ZERO", note="C4", status="NOTE_ON", velocity=100),
                                                      RhythemNoteEvent(division="ZERO", note="E4", status="NOTE_ON", velocity=100),
                                                      RhythemNoteEvent(division="ZERO", note="G4", status="NOTE_ON", velocity=100),
                                                      RhythemNoteEvent(division="ZERO", note="B4", status="NOTE_ON", velocity=100)])
    rhythem_generator.add_events_with_duration(rhythem_note_events=[RhythemNoteEvent(division="ZERO", note="C5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="ZERO", note="D5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="ZERO", note="E5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="ZERO", note="F5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="ZERO", note="G5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="ZERO", note="A5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="ZERO", note="B5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="ZERO", note="C6", status="NOTE_ON", velocity=100)], 
                                               duration_divisions=["QUARTER", "QUARTER", "QUARTER", "QUARTER", "QUARTER", "QUARTER", "QUARTER", "QUARTER"])
    rhythem_generator.add_events(rhythem_note_events=[RhythemNoteEvent(division="ZERO", note="C4", status="NOTE_OFF", velocity=100),
                                                      RhythemNoteEvent(division="ZERO", note="E4", status="NOTE_OFF", velocity=100),
                                                      RhythemNoteEvent(division="ZERO", note="G4", status="NOTE_OFF", velocity=100),
                                                      RhythemNoteEvent(division="ZERO", note="B4", status="NOTE_OFF", velocity=100)])
    
    rhythem_generator.add_sustain_pedal_event(division_duration="ZERO", sustain=True)
    rhythem_generator.add_events_with_duration(rhythem_note_events=[RhythemNoteEvent(division="ZERO", note="C5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="ZERO", note="D5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="ZERO", note="E5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="ZERO", note="F5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="ZERO", note="G5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="ZERO", note="A5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="ZERO", note="B5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="ZERO", note="C6", status="NOTE_ON", velocity=100)], 
                                               duration_divisions=["EIGHTH", "EIGHTH", "EIGHTH", "EIGHTH", "EIGHTH", "EIGHTH", "EIGHTH", "EIGHTH"])
    rhythem_generator.add_sustain_pedal_event(division_duration="ZERO", sustain=False)
    
    for _ in range(5):
        rhythem_generator.construct_scale(interval_scale=IntervalScale(name="D5 Major", 
                                                                    starting_note=74,
                                                                    intervals=[2,2,3,2,3],
                                                                    divisions=["THIRTYSECOND", "THIRTYSECOND", "THIRTYSECOND", "THIRTYSECOND", 
                                                                                "THIRTYSECOND", "THIRTYSECOND"],
                                                                    velocities=[20, 30, 40, 50, 60, 70]),
                                        duration_divisions=["ZERO", "ZERO", "ZERO", "ZERO",
                                                            "ZERO", "ZERO"], 
                                        direction='BOTH')
    
    rhythem_generator.midi_scheduler.schedule_events(initial_delay=0)
    