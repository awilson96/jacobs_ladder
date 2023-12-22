import logging
from dataclasses import dataclass

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "November 11th 2023 (creation)"

logging.basicConfig(
    filename="../logs/MidiManager.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class InOutQueue:
    def __init__(self, size):
        self.queue = []
        self.size = size

    def enqueue(self, elem):
        self.queue.append(elem)
        if len(self.queue) > self.size:
            self.queue.pop(0)  # Remove the oldest element at index 0

    def get_queue(self):
        return self.queue


@dataclass
class Scale:
    name: str
    notes: list[str]   
    
# Major/Minor scales
C_Major = Scale("C Ionian", ["C", "D", "E", "F", "G", "A", "B"])
Db_Major = Scale("Db Ionian", ["D\u266d", "E\u266d", "F", "G\u266d", "A\u266d", "B\u266d", "C"])
D_Major = Scale("D Ionian", ["D", "E", "G\u266d", "G", "A", "B", "D\u266d"])
Eb_Major = Scale("Eb Ionian", ["E\u266d", "F", "G", "A\u266d", "B\u266d", "C", "D"])
E_Major = Scale("E Ionian", ["E", "G\u266d", "A\u266d", "A", "B", "D\u266d", "E\u266d"])
F_Major = Scale("F Ionian", ["F", "G", "A", "B\u266d", "C", "D", "E"])
Gb_Major = Scale("Gb Ionian", ["G\u266d", "A\u266d", "B\u266d", "B", "D\u266d", "E\u266d", "F"])
G_Major = Scale("G Ionian", ["G", "A", "B", "C", "D", "E", "G\u266d"])
Ab_Major = Scale("Ab Ionian", ["A\u266d", "B\u266d", "C", "D\u266d", "E\u266d", "F", "G"])
A_Major = Scale("A Ionian", ["A", "B", "D\u266d", "D", "E", "G\u266d", "A\u266d"])
Bb_Major = Scale("Bb Ionian", ["B\u266d", "C", "D", "E\u266d", "F", "G", "A"])
B_Major = Scale("B Ionian", ["B", "D\u266d", "E\u266d", "E", "G\u266d", "A\u266d", "B\u266d"])

# TODO: Add Harmonic Minor Scales
# TODO: Add Harmonic Major Scales
# TODO: Add Melodic Minor Scales
# TODO: Determine where these scales should live since they are all just dataclasses

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
        
        self.major_scales = [C_Major, Db_Major, D_Major, Eb_Major, E_Major, F_Major, Gb_Major, G_Major, Ab_Major, A_Major, Bb_Major, B_Major]

        # History of at most the last 5 lists of candidate keys used to determine the key uniquely at a given point in time
        # TODO: Determine the optimum lookback period (more than 5, less than 5?)
        self.history = InOutQueue(5)

    def determine_chord(self, message_heap: list[list]):
        """
        Based on the currently active notes in the message_heap, determine the chord
        This function can be used to display chord data to the terminal or to make tuning decisions based on intervalic relationships

        Args:
            message_heap (list[list]): A list of lists of the form [[note, instance_index, status, velocity], ...]
        """
        sorted_message_heap = sorted(message_heap, key=lambda x: x[0])
        notes = [note[0] for note in sorted_message_heap]
        instance_indices = [indices[1] for indices in sorted_message_heap]
        
        logging.debug(f"Notes: {notes}")

        intervals = self.get_intervals(notes)
        logging.debug(f"Intervals: {intervals}")
        
        if len(intervals) == 0:
            return f" "
        elif len(intervals) == 1:
            diads = self.get_diad(intervals)
            logging.debug(f"Diads: {diads}")
            return f"{diads[0]}"
            
        elif len(intervals) == 2:
            triad = self.get_triad(intervals, notes)
            logging.debug(f"Triad: {triad}")
            return triad
        
        elif len(intervals) == 3:
            tetrad = self.get_tetrad(intervals, notes)
            logging.debug(f"Tetrad: {tetrad}")
            return tetrad
    
    # TODO: In the future it could be cool to create an ambiguity resolver.  Take for example the two chords Db major
    # and C major.  These two chords will have no shared keys since Db Major will have [Db Major, Gb Major, Ab Major] 
    # as its set and C major will have [C Major, F Major, G Major] as its set.  An interesting way to resolve this would
    # be to take the union operation between the notes in Db Major and C Major which would yield [F, B]. The chord 
    # Db Major contains an F, and although the previous chord C major does not, you could tune off of the F which would \
    # have been a perfect fourth away from C considering F the fulcrum and using it to tune the Db
    def determine_key(self, message_heap: list[list]):
        """Using the unique notes and instance indices, determine the key of the chord you are currently playing. 
        This is done by comparing the unique notes in the chord to the list of scales to see where there is a 
        match of all notes. If there are multiple possibilites, the method will look at previous lists of potential keys 
        and perform the union operation on this previous list until it finds a unique key to return.  If there is no 
        history then the method will add the current set of potential candidates to the history and begin building it,
        and in the beginning will default to selecting the first chord in the list of potential keys.  See
        _create_history() for a full description of how keys are selected when the history is ambiguous.  

        Args:
            message_heap (list[list]): a list of currently active notes with their metadata

        Returns:
            list[str]: a single key which can represent the key of the last few chords played
        """
        notes = [self.int_note[note[0]] for note in message_heap]
        unique_notes = list(set(notes))
        print(unique_notes)
        
        candidate_keys = []
        for scale in self.major_scales:
            is_sublist = all(element in scale.notes for element in unique_notes) 
            if is_sublist:
                candidate_keys.append(scale.name)

        unique_key = self._create_history(candidate_keys)
        if len(candidate_keys) == 1:
            return candidate_keys[0]
        else:
            return unique_key
    
    def _create_history(self, potential_keys: list[list]):
        """Create a InOut queue of size 5 enqueuing new potential lists of keys as they arrive, then continuously 
        perform union operations on the current element and the previous union operation resultant list until either
        a) the set operation results in an empty set in which case the first element in the previous resultant is chosen
        b) the set operation results in a single element in which case this element is selected
        c) the set operation results in multiple elements in which case the method continues to perform union operations
        with the resultants of the previous iteration until a) or b) occurs or if the max lookthrough period of 5 has
        been reached. In this case the first element of the final resultant will be selected. 

        Args:
            potential_keys (list[list]): possible keys that the current chord being played could belong to

        Returns:
            str: A single key to which the history of chords can be proven to belong to, or a selected chord the key 
            belongs to out of multiple possibly ambiguous keys the chord could also belong to based on the history 
            of the past five chords played.
        """

        if potential_keys != [] and potential_keys is not None:
            self.history.enqueue(potential_keys) 
            # If there is already only one possible key for the chord being played then just break out of the funtion
            # after enqueuing the current key to the key history
            if len(potential_keys) == 1:
                return potential_keys[0] 
            
            candidate_keys_list: list[list] = self.history.get_queue()
            # If the history queue has not yet been populated then just return the first found potential key 
            if len(candidate_keys_list) == 0 or len(candidate_keys_list) == 1:
                return potential_keys[0]

            union_result = list(set(candidate_keys_list[0]) | set(candidate_keys_list[1]))
            if len(union_result) == 0:
                # TODO: Handle the situation where the union of the two previous chords yields the empty set
                # right now we are assuming that the new chord is the most up to date so we arbitrarily select the first
                # key in the sequence
                return candidate_keys_list[1][0]
            
            elif len(union_result) == 1:
                return union_result[0]
            
            elif len(union_result) >= 2:
                if len(candidate_keys_list) >= 3:
                    for i in range(2, len(candidate_keys_list)):
                        union_result_2 = list(set(union_result) | set(candidate_keys_list[i]))
                        if len(union_result_2) == 0:
                            # Skip this iteration since it doesn't provide valuable key information
                            continue
                        elif len(union_result_2) == 1:
                            return union_result_2[0]
                        else:
                            # If we are on the last iteration and still have not found a unique key then just return
                            # the first element of the most recent resultant union operation
                            if i == len(candidate_keys_list) - 1:
                                return union_result_2[0]
                            # Otherwise set union_result to the most recent resultant union operation and continue looping
                            else:
                                union_result = union_result_2
                else:
                    union_result_2 = list(set(union_result) | set(candidate_keys_list[2]))
                    if union_result_2 == 0:
                        # TODO: Handle the situation where the union of the two previous chords yields the empty set
                        # Right now we are just returning the first element of the previous resultant union operation 
                        # as this will hopefully be a more narrowed down list and will be a good estimate
                        return union_result[0]
                    
                    elif len(union_result_2) == 1:
                        return union_result_2[0]
                    
                    else:
                        # TODO: Handle the situation where after three chords and only three chords of history have been
                        # played, the key is still ambiguous. Right now we are just returning the first value in this 
                        # iteration's resultant union operation
                        return union_result_2[0]
        
        else:
            logging.warning("potential_keys is equal to either [] or None meaning that the key was either unable to \
                            be classified, or scales have not been built out to support this chord yet")

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
                    diads.append("Tritone")
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

    def get_triad(self, intervals: list, notes: list):
        """
        Get triad chord from a list of two intervals and a list of notes

        Args:
            intervals (list): a list of intervals between sorted notes (lowest to highest)
            notes (list): a list of sorted notes (lowest to highest)

        Returns:
            str: a stringified description of the triad you just played
            
        Source: https://www.scales-chords.com/chord-namer/piano?notes=C;F;D&key=&bass=C
        """
        root, branch, leaf = notes
        root, branch, leaf = self.int_note[root], self.int_note[branch], self.int_note[leaf]
        
        match intervals:
            case [4, 3] | [7, 9]:
                return f"{root} Major Triad"        # Major
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
    
    def get_tetrad(self, intervals: list[int], notes: list[int]):
        """
        Get tetrad chord based on a list of three intervals and a list of notes

        Args:
            intervals (list[int]): a list of intervals between sorted notes (lowest to highest)
            notes (list[int]): a list of sorted notes (lowest to highest)

        Returns:
            str: a stringified description of the chord
        """

        bass, tenor, alto, soprano = notes
        bass, tenor, alto, soprano = self.int_note[bass], self.int_note[tenor], self.int_note[alto], self.int_note[soprano]

        match intervals:
            case [4, 3, 4]:
                return f"{bass}maj7"                        # Major 7 
            case [3, 4, 1]:
                return f"{soprano}maj7/{bass}"              # Major 7 1st Inversion
            case [4, 1, 4]:
                return f"{alto}maj7/{bass}"                 # Major 7 2nd Inversion
            case [1, 4, 3]:
                return f"{tenor}maj7/{bass}"                # Major 7 3rd Inversion
            case [3, 4, 3]:
                return f"{bass}min7"                        # Minor 7 
            case [4, 3, 2]:
                return f"{soprano}min7/{bass}"              # Minor 7 1st Inversion
            case [3, 2, 3]:
                return f"{alto}min7/{bass}"                 # Minor 7 2nd Inversion
            case [2, 3, 4]:
                return f"{tenor}min7/{bass}"                # Minor 7 3rd Inversion
            case [3, 4, 4]:
                return f"{bass}m(maj7)"                     # Minor Major 7 
            case [4, 4, 1]:
                return f"{soprano}m(maj7)/{bass}"           # Minor Major 7 1st Inversion
            case [4, 1, 3]:
                return f"{alto}m(maj7)/{bass}"              # Minor Major 7 2nd Inversion
            case [1, 3, 4]:
                return f"{tenor}m(maj7)/{bass}"             # Minor Major 7 3rd Inversion
            case [4, 3, 3]:
                return f"{bass}7"                           # Dominant 7
            case [3, 3, 2]:
                return f"{soprano}7/{bass}"                 # Dominant 7 1st Inversion
            case [3, 2, 4]:
                return f"{alto}7/{bass}"                    # Dominant 7 2nd Inversion
            case [2, 4, 3]:
                return f"{tenor}7/{bass}"                   # Dominant 7 3rd Inversion
            case [3, 3, 4]:
                return f"{bass}m7\u266d5"                   # Half Diminished
            case [3, 3, 3]:
                return f"{bass}dim7"                        # Full Diminished
            case [4, 4, 4]:
                return f"{bass}aug"                         # Augmented 
            case [5, 5, 5]:
                return f"{bass}m11"                         # Minor 11
            case [2, 1, 4]:
                return f"{bass}m add(2)"                    # Minor add 2
            case [2, 2, 3]:
                return f"{bass} add(2)"                     # Major add 2
            
        tetrad: str = ""
        return tetrad