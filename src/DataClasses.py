from dataclasses import dataclass
from .Utilities import division_to_dt

@dataclass
class Scale:
    name: str
    notes: list[str]
    
@dataclass
class IntervalScale:
    name: str
    starting_note: int
    intervals: list[int]
    divisions: list[str]
    velocities: list[int]
    
@dataclass
class NoteEvent:
    dt: float
    note: int
    status: int
    velocity: int
    
@dataclass
class RhythemNoteEvent:
    offset: float
    division: str
    note: str
    status: str
    velocity: int
    tempo: int

    def __init__(self, offset, division, note, status, velocity, tempo):
        self.offset = offset
        self.division = division
        self.note = note
        self.status = status
        self.velocity = velocity
        self.tempo = tempo
        self.absolute_time = offset + division_to_dt(division=division, tempo=tempo)