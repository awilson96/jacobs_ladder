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
    
    def get_diad(self, intervals: list[int]):
        """
        Get the stringified name of a diad interval, used to make tuning decisions or displaying to the terminal

        Args:
            intervals (int): A list of integer interval used to determine intervallic relationships between notes

        Returns:
            list[string]: list of intervallic relationships expressed as strings
        """
        diads: list[str] = []
        
        for interval in intervals:
            match interval:
                case 1:
                    diads.append("Minor 2")
                case 2:
                    diads.append("Major 2")
                case 3:
                    diads.append("Minor 3")
                case 4:
                    diads.append("Major 3")
                case 5:
                    diads.append("Perfect 4")
                case 6:
                    diads.append("Minor 5")
                case 7: 
                    diads.append("Perfect 5")
                case 8:
                    diads.append("Minor 6")
                case 9:
                    diads.append("Major 6")
                case 10:
                    diads.append("Minor 7")
                case 11:
                    diads.append("Major 7")
                case 12:
                    diads.append("Octave 8")
                case 13:
                    diads.append("Minor 9")
                case 14:
                    diads.append("Major 9")
                case 15:
                    diads.append("Minor 10")
                case 16:
                    diads.append("Major 10")
                case 17:
                    diads.append("Major 11")
                case 18:
                    diads.append("Sharp 11")
                case 19:
                    diads.append("Major 12")
                case 20:
                    diads.append("Minor 13")
                case 21:
                    diads.append("Major 13")
                case 22:
                    diads.append("Minor 14")
                case 23:
                    diads.append("Major 14")
                case 24:
                    diads.append("Octave 15")
        return diads