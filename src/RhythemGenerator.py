from .DataClasses import NoteEvent
# from .MidiScheduler import MidiScheduler

class RhythmGenerator:
    SECONDS_IN_MINUTE = 60

    def __init__(self, tempo: int):
        """Initialize the RhythmGenerator with a tempo and a MidiScheduler instance.

        Args:
            tempo (int): the tempo of the rhythems you wish to produce
        """
        self.tempo = tempo
        # self.midi_scheduler = MidiScheduler()
        self.note_durations = {
            'whole': 4000,
            'half': 2000,
            'quarter': 1000,
            'eighth': 500,
            'sixteenth': 250
        }

    def set_tempo(self, tempo: int):
        """Set a new tempo for the RhythmGenerator.

        Args:
            tempo (int): The new tempo in beats per minute.
        """
        self.tempo = tempo

    def duration_to_dt(self, duration: str) -> int:
        """Convert a rhythmic duration to a time delay (dt) in milliseconds.

        Args:
            duration (str): The rhythmic duration (e.g., 'whole', 'half', 'quarter', 'eighth', 'sixteenth').

        Returns:
            int: The delay time in milliseconds.
        """
        if duration not in self.note_durations:
            raise ValueError("Invalid duration. Must be one of: " + ", ".join(self.note_durations.keys()))

        return int(self.note_durations[duration] * (self.SECONDS_IN_MINUTE / self.tempo))
