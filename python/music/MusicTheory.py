import logging
from collections import Counter

from ..utilities.DataClasses import Scale
from ..utilities.Dictionaries import get_midi_notes
from ..utilities.Queue import InOutQueue
from .chord_definitions.TriadDefinitions import TriadDefinitions
from .scales.HarmonicMajorScales import get_harmonic_major_scales
from .scales.HarmonicMinorScales import get_harmonic_minor_scales
from .scales.MajorScales import get_major_scales
from .scales.MelodicMinorScales import get_melodic_minor_scales

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "November 11th 2023 (creation)"

logging.basicConfig(
    filename="./logs/MidiManager.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class MusicTheory:
    def __init__(self):
        # Dictionary to convert int midi notes into letter notes assuming all flats for ease of logic
        self.int_note:              dict[int, str]              = get_midi_notes()
        
        # Scales used for justly tuning between two chords from different potential scales
        self.harmonic_major_scales: list[Scale]                 = get_harmonic_major_scales()
        self.harmonic_minor_scales: list[Scale]                 = get_harmonic_minor_scales()
        self.major_scales:          list[Scale]                 = get_major_scales()
        self.melodic_minor_scales:  list[Scale]                 = get_melodic_minor_scales()
        
        # Used for matching triads in a more robust way
        self.triad_definitions = TriadDefinitions()

        # History of at most the last 5 lists of candidate keys used to determine the key uniquely at a given point in time
        # TODO: Determine the optimum lookback period (more than 5, less than 5?)
        self.QUEUE_SIZE = 5
        self.history = InOutQueue(self.QUEUE_SIZE)

    def determine_chord(self, message_heap: list[list[int]]):
        """Based on the currently active notes in the message_heap, determine the chord
        This function can be used to display chord data to the terminal or to make tuning decisions based on intervalic relationships

        Args:
            message_heap (list[list[int]]): A list of lists of the form [[note, instance_index, status, velocity], ...]

        Returns:
            str: stringified description of the chord that was played
        """
        sorted_message_heap:        list[list[int]]             = sorted(message_heap, key=lambda x: x[0])
        notes:                      list[int]                   = [note[0] for note in sorted_message_heap]
        instance_indices:           list[int]                   = [indices[1] for indices in sorted_message_heap]
        
        logging.debug(f"Notes: {notes}")

        intervals:                  list[int]                   = self.get_intervals(notes)
        logging.debug(f"Intervals: {intervals}")
        
        if len(intervals) == 0:
            return f" "
        elif len(intervals) == 1:
            diads:                  str                   = self.get_diad(intervals)
            logging.debug(f"Diads: {diads}")
            return f"{diads}"
            
        elif len(intervals) == 2:
            triad:                  list[str]             = self.get_triad(intervals, notes)
            logging.debug(f"Triad: {triad}")
            return triad
        
        elif len(intervals) == 3:
            tetrad:                 list[str]             = self.get_tetrad(intervals, notes)
            logging.debug(f"Tetrad: {tetrad}")
            return tetrad
        else:
            return None
    
    # TODO: Look into the case where nothing is returned due to the current chord not matching any known scale
    # TODO: Look into cases where a major scale would just as easily describe the current chord being held, it may be wise to rank major a bit higher
    def determine_key(self, message_heap: list[list[int]]):
        """Determines candidate keys based on the notes that are currently being held down. Then it compares those candidate
        keys to the previous QUEUE_SIZE lists of candidate keys and performs the intersection with the current key and each of the previous lists.
        The key with the most occurences gets returned as it has best described the key for the last QUEUE_SIZE frames.

        Args:
            message_heap (list[list[int]]): a list of currently active notes with their metadata

        Returns:
            str: a single key which can represent the key of the last few chords played
        """
        notes:                      list[int]             = [self.int_note[note[0]] for note in message_heap]
        unique_notes:               list[int]             = list(set(notes))
        
        candidate_keys:             list[str]             = []
        for scale in self.major_scales:
            is_sublist = all(element in scale.notes for element in unique_notes) 
            if is_sublist:
                candidate_keys.append(scale.name)
        if len(candidate_keys) < 7:
            for scale in self.harmonic_minor_scales:
                is_sublist = all(element in scale.notes for element in unique_notes) 
                if is_sublist:
                    candidate_keys.append(scale.name)
            for scale in self.harmonic_major_scales:
                is_sublist = all(element in scale.notes for element in unique_notes) 
                if is_sublist:
                    candidate_keys.append(scale.name)
            for scale in self.melodic_minor_scales:
                is_sublist = all(element in scale.notes for element in unique_notes) 
                if is_sublist:
                    candidate_keys.append(scale.name)
        
        # print(candidate_keys)
                
        self.history.enqueue(candidate_keys)
        return self.find_most_common_scale()
        
    def find_most_common_scale(self):
        """Uses the InOutQueue to determine out of the previous self.QUEUE_SIZE frames which scale occured the most frequently
        If there is a tie then one will be chosen arbitrarily from the most frequent scales

        Returns:
            str | None: most frequently occuring scale if the length of history is greater than self.QUEUE_SIZE and None otherwise
        """
        history = self.history.get_queue()       
        if len(history) >= self.QUEUE_SIZE:
            oldest_frame, older_frame, middle_frame, previous_frame, current_frame = history
            
            current_frame = set(current_frame)
            previous_frame = set(previous_frame)
            middle_frame = set(middle_frame)
            older_frame = set(older_frame)
            oldest_frame = set(oldest_frame)
            
            frames = [previous_frame, middle_frame, older_frame, oldest_frame]
            
            scale_counter = Counter()
            
            for frame in frames:
                intersection = current_frame.intersection(frame)
                scale_counter.update(intersection)
                
            most_common_scale, occurrences = scale_counter.most_common(1)[0]
           
            return most_common_scale
        else:
            logging.warning(f"Queue is not yet populated with at least {self.QUEUE_SIZE} elements. Play at least 5 different chords to use this feature.")
            return None
    

    def get_intervals(self, notes: list[int]):
        """Determine the intervals between notes

        Args:
            notes (list[int]): A list of unsorted integer notes

        Returns:
            list[int]: A sorted list of the intervals from the lowest note to the highest note
        """
        intervals:                  list[int]             = []

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
            str: intervallic relationship between two notes expressed as a string
        """

        for interval in intervals:
            match interval:
                case 1:
                    return "Minor 2" 
                case 2:
                    return "Major 2"
                case 3:
                    return "Minor 3"
                case 4:
                    return "Major 3"
                case 5:
                    return "Perfect 4"
                case 6:
                    return "Tritone"
                case 7 | 19 | 31 | 43 | 55 | 67 | 79 | 91 | 103:
                    return "Perfect 5"
                case 8:
                    return "Minor 6"
                case 9:
                    return "Major 6"
                case 10 | 22 | 34 | 46 | 58 | 70 | 82 | 94 | 106:
                    return "Minor 7"
                case 11 | 23 | 35 | 47 | 59 | 71 | 83 | 95 | 107:
                    return "Major 7"
                case 12 | 24 | 36 | 48 | 60 | 72 | 84 | 96 | 108:
                    return "Octave"
                case 13 | 25 | 37 | 49 | 61 | 73 | 85 | 97:
                    return "Minor 9"
                case 14 | 26 | 38 | 50 | 62 | 74 | 86 | 98:
                    return "Major 9"
                case 15 | 27 | 39 | 51 | 63 | 75 | 87 | 99:
                    return "Minor 10"
                case 16 | 28 | 40 | 52 | 64 | 76 | 88 | 100:
                    return "Major 10"
                case 17 | 29 | 41 | 53 | 65 | 77 | 89 | 101:
                    return "Major 11"
                case 18 | 30 | 42 | 54 | 66 | 78 | 90 | 102:
                    return "Sharp 11"
                case 20 | 32 | 44 | 56 | 68 | 80 | 92 | 104:
                    return "Minor 13"
                case 21 | 33 | 45 | 57 | 69 | 81 | 93 | 105:
                    return "Major 13"

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
        root:               int
        branch:             int
        leaf:               int
        root, branch, leaf = notes
        root, branch, leaf = self.int_note[root], self.int_note[branch], self.int_note[leaf]
        
        if self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.major_triad):
            return f"{root} Major Triad"        # Major (C, E, G) or (C, G, E)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.major_triad_1st_inv):
            return f"{leaf}/{root}"             # Major 1st Inversion (E, G, C)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.major_triad_1st_inv_var):
            return f"{branch}/{root}"           # Major 1st Inversion (E, C, G)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.major_triad_2nd_inv):
            return f"{branch}/{root}"           # Major 2nd Inversion (G, C, E)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.major_triad_2nd_inv_var):
            return f"{leaf}/{root}"             # Major 2nd Inversion (G, E, C)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.minor_triad):
            return f"{root}m"                   # Minor (C, Eb, G)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.minor_triad_1st_inv):
            return f"{leaf}m/{root}"            # Minor 1st Inversion (Eb, G, C)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.minor_triad_1st_inv_var):
            return f"{branch}m/{root}"          # Minor 1st Inversion (Eb, C, G)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.minor_triad_2nd_inv):
            return f"{branch}m/{root}"          # Minor 2nd Inversion (G, C, Eb)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.minor_triad_2nd_inv_var):
            return f"{leaf}m/{root}"            # Minor 2nd Inversion (G, Eb, C)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.add2):
            return f"{root}add(2)"              # Add 2 chord
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.diminished):
            return f"{root}dim"                 # Diminished (C, Eb, Gb) or (C, Gb, Eb)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.augmented):
            return f"{root}aug"                 # Augmented (C, E, Ab) or (C, Ab, E)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.eleven_sus4):
            return f"{root}11sus4"              # Quartal chord (stacking fourths)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sus2):
            return f"{root}sus2"                # Suspended 2
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.nine_chord):
            return f"{root}9"                   # 9 chord with no third
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sus4):
            return f"{root}sus4"                # Suspended 4
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.eleven_chord):
            return f"{root}11"                  # 11 chord with no third
        
        match intervals:
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
        bass:               int
        tenor:              int
        alto:               int
        soprano:            int

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