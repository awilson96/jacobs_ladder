import logging

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "November 11th 2023 (creation)"

logging.basicConfig(
    filename="../logs/MidiManager.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class MusicTheory:
    def __init__(self):
        pass
    
    def determine_chord(self, message_heap: list[list]):
        """
        Based on the currently active notes in the message_heap, determine the chord
        This function can be used to display chord data to the terminal or to make tuning decisions based on intervalic relationships

        Args:
            message_heap (list[list]): A list of lists of the form [[note, instance_index, status, velocity], ...]
        """
        notes = [note[0] for note in message_heap]
        notes = set(notes)
        
        if len(notes) == 2:
            pass
        
    def get_intervals(self, notes: list[int]):
        """Determine the intervals between notes

        Args:
            notes (list[int]): A list of unsorted integer notes

        Returns:
            list[int]: A sorted list of the intervals from the lowest note to the highest note
        """
        intervals: list[int] = []
        
        sorted_notes = sorted(notes)
        if len(sorted_notes) > 1:
            for idx in range(len(sorted_notes)-1):
                intervals.append(notes[idx+1] - notes[idx])
        
        return intervals