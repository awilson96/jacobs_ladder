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
        self.int_note = {21: "A", 22: "B\u266d", 23: "B", 24: "C", 25: "D\u266d", 26: "D", 27: "E\u266d", 28: "E", 29: "F", 30: "G\u266d", 31: "G", 32: "A\u266d", 
                         33: "A", 34: "B\u266d", 35: "B", 36: "C", 37: "D\u266d", 38: "D", 39: "E\u266d", 40: "E", 41: "F", 42: "G\u266d", 43: "G", 44: "A\u266d",
                         45: "A", 46: "B\u266d", 47: "B", 48: "C", 49: "D\u266d", 50: "D", 51: "E\u266d", 52: "E", 53: "F", 54: "G\u266d", 55: "G", 56: "A\u266d",
                         57: "A", 58: "B\u266d", 59: "B", 60: "C", 61: "D\u266d", 62: "D", 63: "E\u266d", 64: "E", 65: "F", 66: "G\u266d", 67: "G", 68: "A\u266d",
                         69: "A", 70: "B\u266d", 71: "B", 72: "C", 73: "D\u266d", 74: "D", 75: "E\u266d", 76: "E", 77: "F", 78: "G\u266d", 79: "G", 80: "A\u266d",
                         81: "A", 82: "B\u266d", 83: "B", 84: "C", 85: "D\u266d", 86: "D", 87: "E\u266d", 88: "E", 89: "F", 90: "G\u266d", 91: "G", 92: "A\u266d", 
                         93: "A", 94: "B\u266d", 95: "B", 96: "C", 97: "D\u266d", 98: "D", 99: "E\u266d", 100: "E", 101: "F", 102: "G\u266d", 103: "G", 104: "A\u266d",
                         105: "A", 106: "B\u266d", 107: "B", 108: "C"}

    def determine_chord(self, message_heap: list[list]):
        """
        Based on the currently active notes in the message_heap, determine the chord
        This function can be used to display chord data to the terminal or to make tuning decisions based on intervalic relationships

        Args:
            message_heap (list[list]): A list of lists of the form [[note, instance_index, status, velocity], ...]
        """
        notes = [note[0] for note in message_heap]
        notes = sorted(list(set(notes)))
        logging.debug(f"Notes: {notes}")

        intervals = self.get_intervals(notes)
        logging.debug(f"Intervals: {intervals}")

        if len(intervals) == 1:
            diads = self.get_diads(intervals)
            logging.debug(f"Diads: {diads}")
            return f"{diads[0]}"
            
        elif len(intervals) == 2:
            triad = self.get_triads(intervals, notes)
            logging.debug(f"Triad: {triad}")
            return triad

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
            for idx in range(len(sorted_notes) - 1):
                intervals.append(notes[idx + 1] - notes[idx])

        return intervals

    def get_diads(self, intervals: list[int]):
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
                case 7 | 19 | 31 | 43 | 55 | 67 | 79 | 91 | 103:
                    diads.append("Perfect 5")
                case 8:
                    diads.append("Minor 6")
                case 9:
                    diads.append("Major 6")
                case 10 | 22 | 34 | 46 | 58 | 70 | 82 | 94 | 106:
                    diads.append("Minor 7")
                case 11 | 23 | 35 | 47 | 59 | 71 | 83 | 95 | 107:
                    diads.append("Major 7")
                case 12 | 24 | 36 | 48 | 60 | 72 | 84 | 96 | 108:
                    diads.append("Octave")
                case 13 | 25 | 37 | 49 | 61 | 73 | 85 | 97:
                    diads.append("Minor 9")
                case 14 | 26 | 38 | 50 | 62 | 74 | 86 | 98:
                    diads.append("Major 9")
                case 15 | 27 | 39 | 51 | 63 | 75 | 87 | 99:
                    diads.append("Minor 10")
                case 16 | 28 | 40 | 52 | 64 | 76 | 88 | 100:
                    diads.append("Major 10")
                case 17 | 29 | 41 | 53 | 65 | 77 | 89 | 101:
                    diads.append("Major 11")
                case 18 | 30 | 42 | 54 | 66 | 78 | 90 | 102:
                    diads.append("Sharp 11")
                case 20 | 32 | 44 | 56 | 68 | 80 | 92 | 104:
                    diads.append("Minor 13")
                case 21 | 33 | 45 | 57 | 69 | 81 | 93 | 105:
                    diads.append("Major 13")
        return diads

    def get_triads(self, intervals: list, notes: list):
        """
        Get the chord as a triad given a list of two intervals

        Args:
            diads (list): _description_

        Returns:
            _type_: _description_
        """
        root, branch, leaf = notes
        root, branch, leaf = self.int_note[root], self.int_note[branch], self.int_note[leaf]
        
        match intervals:
            case [4, 3] | [7, 9]:
                return f"{root}"                    # Major
            case [3, 5]:
                return f"{leaf}/{root}"             # Major 1st Inversion
            case [5, 4]:
                return f"{branch}/{root}"           # Major 2nd Inversion
            case [3, 4]:
                return f"{root}m"                   # Minor
            case [4, 5]:
                return f"{leaf}m/{root}"            # Minor 1st Inversion
            case [5, 3]:
                return f"{branch}m/{root}"          # Minor 2nd Inversion
            case [2, 2]:
                return f"{root}add(2)"              # Add 2 chord
            case [3, 3]:
                return f"{root}dim"                 # Diminished
            case [4, 4]:
                return f"{root}aug"                 # Augmented
            case [5, 5]:
                return f"{root}11sus4"              # Quartal chord (stacking fourths)
            case [2, 5] | [7, 7]:
                return f"{root}sus2"                # Suspended 2
            case [5, 2]:
                return f"{root}sus4"                # Suspended 4
            case [7, 3]:
                return f"{branch}7 Sus"             # Dominant with no 3rd
            case [3, 2]:
                return f"{leaf}7sus/{root}"         # Dominant with no 3rd 1st Inversion
            case [2, 7]:
                return f"{branch}7sus/{root}"       # Dominant with no 3rd 2nd Inversion
            case [4, 6]:
                return f"{root}7"                   # Dominant with no 5th
            case [6, 2]:
                return f"{leaf}7/{root}"            # Dominant with no 5th 1st Inversion
            case [2, 4]:
                return f"{branch}7/{root}"          # Dominant with no 5th 2nd Inversion
            case [3, 6]:
                return f"{root}min6"                # Minor 6 (Diminished 1st Inversion)
            case [6, 3]:
                return f"{leaf}min6/{root}"         # Minor 6 1st inv (Diminished 2nd Inversion)
            case [7, 4]:
                return f"{root}maj7sus"             # Major 7 no 3rd
            case [4, 1]:
                return f"{leaf}maj7sus/{root}"      # Major 7 no 3rd 1st Inversion
            case [1, 7]:
                return f"{branch}maj7sus/{root}"    # Major 7 no 3rd 2nd Inversion
            case [4, 7]:
                return f"{root}maj7"                # Major 7 no 5th
            case [7, 1]:
                return f"{leaf}maj7/{root}"         # Major 7 no 5th 1st Inversion
            case [1, 4]:
                return f"{branch}maj7/{root}"       # Major 7 no 5th 2nd Inversion
            case [7, 5]:
                return f"{root}sus"                 # Suspended Chord
            
        
        triad: str = ""
        return triad