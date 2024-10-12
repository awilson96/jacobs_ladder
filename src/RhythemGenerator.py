from .DataClasses import NoteEvent, RhythemNoteEvent
from .MidiScheduler import MidiScheduler
from .Dictionaries import notes_to_midi

class RhythmGenerator:
    SECONDS_IN_MINUTE = 60

    def __init__(self, tempo: int):
        """Initialize the RhythmGenerator with a tempo and a MidiScheduler instance.

        Args:
            tempo (int): the tempo of the rhythems you wish to produce
        """
        self.note_str_to_int = notes_to_midi
        self.tempo = tempo
        self.midi_scheduler = MidiScheduler()
        self.note_divisions_ms = {
            'whole': 4000,
            'half': 2000,
            'quarter': 1000,
            'eighth': 500,
            'sixteenth': 250,
            'zero': 0
        }
        self.status_str_to_int = {
            'NOTE_ON': 144,
            'NOTE_OFF': 128
        }

    def set_tempo(self, tempo: int):
        """Set a new tempo for the RhythmGenerator.

        Args:
            tempo (int): The new tempo in beats per minute.
        """
        self.tempo = tempo

    def division_to_dt(self, division: str) -> int:
        """Convert a rhythmic division to a time delay (dt) in milliseconds.

        Args:
            division (str): The rhythmic division (e.g., 'whole', 'half', 'quarter', 'eighth', 'sixteenth').

        Returns:
            int: The delay time in milliseconds.
        """
        if division not in self.note_divisions_ms:
            raise ValueError("Invalid division. Must be one of: " + ", ".join(self.note_divisions_ms.keys()))

        return int(self.note_divisions_ms[division] * (self.SECONDS_IN_MINUTE / self.tempo))
    
    def add_event(self, rhythem_note_event: RhythemNoteEvent):
        """Add an event using a more intuitive RhythemNoteEvent dataclass

        Args:
            rhythem_note_event (RhythemNoteEvent): a RhythemNoteEvent dataclass to add to the event sequence
        """
        note_event = NoteEvent(dt=self.division_to_dt(division=rhythem_note_event.division), 
                               note=self.note_str_to_int[rhythem_note_event.note], 
                               status=self.status_str_to_int[rhythem_note_event.status],
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
                               status=self.status_str_to_int[rhythem_note_event.status],
                               velocity=rhythem_note_event.velocity)
        
        self.midi_scheduler.add_event(note_event=note_event)
        note_off_event = NoteEvent(dt=self.division_to_dt(division=duration_division),
                                   note=note_event.note,
                                   status=self.status_str_to_int["NOTE_OFF"],
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
                                   status=self.status_str_to_int[rhythem_note_event.status], 
                                   velocity=rhythem_note_event.velocity)
            self.midi_scheduler.add_event(note_event=note_event)
            
    def add_events_with_duration(self, rhythem_note_events: list[RhythemNoteEvent], duration_divisions: list[str]):
        """Add multiple multiple notes with a specified duration expressed as a duration division. This method is useful
        for playing a sequence individual notes for the whole duration of each notes division with no other held notes. 

        Args:
            rhythem_note_events (list[RhythemNoteEvent]): a list of RhythemNoteEvents for adding to the event queue
            duration_divisions (list[str]): a list of duration divisions assigned in order to each RhythemNoteEvent
        """
        assert(len(rhythem_note_events) == len(duration_divisions))
        for rhythem_note_event, duration_division in zip(rhythem_note_events, duration_divisions):
            note_event = NoteEvent(dt=self.division_to_dt(division=rhythem_note_event.division), 
                                   note=self.note_str_to_int[rhythem_note_event.note], 
                                   status=self.status_str_to_int[rhythem_note_event.status], 
                                   velocity=rhythem_note_event.velocity)

            self.midi_scheduler.add_event(note_event=note_event)
        
            note_off_event = NoteEvent(dt=self.division_to_dt(duration_division), 
                                       note=self.note_str_to_int[rhythem_note_event.note], 
                                       status=self.status_str_to_int["NOTE_OFF"], 
                                       velocity=rhythem_note_event.velocity)
            self.midi_scheduler.add_event(note_off_event)
            
    
if __name__ == "__main__":
    rhythem_generator = RhythmGenerator(tempo=220)
    rhythem_generator.add_event(RhythemNoteEvent(division="zero", note="C4", status="NOTE_ON", velocity=100))
    rhythem_generator.add_event(RhythemNoteEvent(division="zero", note="E4", status="NOTE_ON", velocity=100))
    rhythem_generator.add_event(RhythemNoteEvent(division="zero", note="G4", status="NOTE_ON", velocity=100))
    rhythem_generator.add_event(RhythemNoteEvent(division="zero", note="B4", status="NOTE_ON", velocity=100))
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="zero", note="C5", status="NOTE_ON", velocity=100), duration_division="quarter")
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="zero", note="D5", status="NOTE_ON", velocity=100), duration_division="quarter")
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="zero", note="E5", status="NOTE_ON", velocity=100), duration_division="quarter")
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="zero", note="F5", status="NOTE_ON", velocity=100), duration_division="quarter")
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="zero", note="G5", status="NOTE_ON", velocity=100), duration_division="quarter")
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="zero", note="A5", status="NOTE_ON", velocity=100), duration_division="quarter")
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="zero", note="B5", status="NOTE_ON", velocity=100), duration_division="quarter")
    rhythem_generator.add_event_with_duration(RhythemNoteEvent(division="zero", note="C6", status="NOTE_ON", velocity=100), duration_division="quarter")
    
    rhythem_generator.add_event(RhythemNoteEvent(division="zero", note="C4", status="NOTE_OFF", velocity=100))
    rhythem_generator.add_event(RhythemNoteEvent(division="zero", note="E4", status="NOTE_OFF", velocity=100))
    rhythem_generator.add_event(RhythemNoteEvent(division="zero", note="G4", status="NOTE_OFF", velocity=100))
    rhythem_generator.add_event(RhythemNoteEvent(division="zero", note="B4", status="NOTE_OFF", velocity=100))
    rhythem_generator.add_events(rhythem_note_events=[RhythemNoteEvent(division="zero", note="C4", status="NOTE_ON", velocity=100),
                                                      RhythemNoteEvent(division="zero", note="E4", status="NOTE_ON", velocity=100),
                                                      RhythemNoteEvent(division="zero", note="G4", status="NOTE_ON", velocity=100),
                                                      RhythemNoteEvent(division="zero", note="B4", status="NOTE_ON", velocity=100)])
    rhythem_generator.add_events_with_duration(rhythem_note_events=[RhythemNoteEvent(division="zero", note="C5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="zero", note="D5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="zero", note="E5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="zero", note="F5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="zero", note="G5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="zero", note="A5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="zero", note="B5", status="NOTE_ON", velocity=100),
                                                                    RhythemNoteEvent(division="zero", note="C6", status="NOTE_ON", velocity=100)], 
                                               duration_divisions=["quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter"])
    rhythem_generator.add_events(rhythem_note_events=[RhythemNoteEvent(division="zero", note="C4", status="NOTE_OFF", velocity=100),
                                                      RhythemNoteEvent(division="zero", note="E4", status="NOTE_OFF", velocity=100),
                                                      RhythemNoteEvent(division="zero", note="G4", status="NOTE_OFF", velocity=100),
                                                      RhythemNoteEvent(division="zero", note="B4", status="NOTE_OFF", velocity=100)])
    
    rhythem_generator.midi_scheduler.schedule_events(initial_delay=0)