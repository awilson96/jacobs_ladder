from dataclasses import dataclass

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
    division: str
    note: str
    status: str
    velocity: int