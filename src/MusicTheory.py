import logging
from collections import Counter

from .DataClasses import Scale
from .Dictionaries import get_midi_notes
from .Queue import InOutQueue
from .TriadDefinitions import TriadDefinitions
from .HarmonicMajorScales import get_harmonic_major_scales
from .HarmonicMinorScales import get_harmonic_minor_scales
from .MajorScales import get_major_scales
from .MelodicMinorScales import get_melodic_minor_scales
from .Logging import setup_logging

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "November 11th 2023 (creation)"

class MusicTheory:
    """The MusicTheory Class is used to encapsulate the fundamentals of music theory to perform activities such as chord 
    recognition and display, potential scales which can be played over currently suspended notes, representing 
    chords in the simplest harmonic form possible, and key determination.
    """
    def __init__(self, print: bool = False):
        """MusicTheory class takes a flag called print to indicate whether or not to print chords to the console, 
        (defaults to false).

        Args:
            print (bool, optional): if true print chords to the console, otherwise don't. Defaults to False.
        """
        # Setup logging
        self.logger = setup_logging("MusicTheory")
        
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
        
        # Jacob's Ladder
        self.print = print

    def determine_chord(self, message_heap: list[list[int]]):
        """Based on the currently active notes in the message_heap, determine the chord
        This function can be used to display chord data to the terminal or to make tuning decisions based on intervalic relationships

        Args:
            message_heap (list[list[int]]): A list of lists of the form [[note, instance_index, status, velocity], ...]

        Returns:
            str: stringified description of the chord that was played
        """
        sorted_message_heap: list[list[int]] = self.remove_harmonically_redundant_intervals(message_heap=message_heap)
        
        notes: list[int] = [note[0] for note in sorted_message_heap]
        instance_indices: list[int] = [indices[1] for indices in sorted_message_heap]

        intervals: list[int] = self.get_intervals(notes)
        
        if len(intervals) == 0:
            return f" "
        elif len(intervals) == 1:
            diads = self.get_diad(intervals)
            if self.print: print(diads)   
            return f"{diads}"      
            
        elif len(intervals) == 2:      
            triad_log, triad_internal = self.get_triad(intervals, notes)
            if self.print: print(triad_log)
            return triad_internal      
        
        elif len(intervals) == 3:      
            tetrad = self.get_tetrad(intervals, notes)
            if self.print: print(tetrad)
            return tetrad
        else:
            return None
    
    
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
        
        self.history.enqueue(candidate_keys)
        key = self.find_most_common_scale()
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
                if intersection != set():
                    scale_counter.update(intersection)
                else:
                    intersection = ["unknown"]
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
        intervals = []

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
            return f"{root} Maj", "major_triad"                                                                       # Major (C, E, G) or (C, G, E)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.major_triad_1st_inv):
            return f"{leaf}/{root}", "major_triad_1st_inv"                                                            # Major 1st Inversion (E, G, C)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.major_triad_1st_inv_var):
            return f"{branch}/{root}", "major_triad_1st_inv_var"                                                      # Major 1st Inversion (E, C, G)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.major_triad_2nd_inv):
            return f"{branch}/{root}", "major_triad_2nd_inv"                                                          # Major 2nd Inversion (G, C, E)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.major_triad_2nd_inv_var):
            return f"{leaf}/{root}", "major_triad_2nd_inv_var"                                                        # Major 2nd Inversion (G, E, C)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.minor_triad):
            return f"{root}m", "minor_triad"                                                                          # Minor (C, Eb, G)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.minor_triad_1st_inv):
            return f"{leaf}m/{root}", "minor_triad_1st_inv"                                                           # Minor 1st Inversion (Eb, G, C)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.minor_triad_1st_inv_var):
            return f"{branch}m/{root}", "minor_triad_1st_inv_var"                                                     # Minor 1st Inversion (Eb, C, G)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.minor_triad_2nd_inv):
            return f"{branch}m/{root}", "minor_triad_2nd_inv"                                                         # Minor 2nd Inversion (G, C, Eb)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.minor_triad_2nd_inv_var):
            return f"{leaf}m/{root}", "minor_triad_2nd_inv_var"                                                       # Minor 2nd Inversion (G, Eb, C)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.add2):
            return f"{root}add(2)", "add2"                                                                            # Add 2 chord (C, D, E)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.add2_1st_inv):
            return f"{leaf}add(2)/{root}", "add2_1st_inv"                                                             # Add 2 chord 1st inversion (D, E, C)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.add2_2nd_inv):
            return f"{branch}add(2)/{root}", "add2_2nd_inv"                                                           # Add 2 chord 2nd inversion (E, C, D)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.diminished):
            return f"{root}dim", "diminished"                                                                         # Diminished (C, Eb, Gb) or (C, Gb, Eb)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.augmented):
            return f"{root}aug", "augmented"                                                                          # Augmented (C, E, Ab) or (C, Ab, E)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.eleven_sus4):
            return f"{root}11sus4", "eleven_sus4"                                                                     # Quartal chord (C, F, Bb)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sus2):
            return f"{root}sus2", "sus2"                                                                              # Suspended 2 (C, D, G)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.nine_chord):
            return f"{root}9", "nine_chord"                                                                           # 9 chord with no third (C, G, D)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sus4):
            return f"{root}sus4", "sus4"                                                                              # Suspended 4 (C, F, G)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.eleven_chord):
            return f"{root}11", "eleven_chord"                                                                        # 11 chord with no third (C, G, F)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.dominant_no_third):
            return f"{root}7sus", "dominant_no_third"                                                                 # Dominant with no 3rd (C, G, Bb)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.dominant_no_third_1st_inv):
            return f"{leaf}7sus/{root}", "dominant_no_third_1st_inv"                                                  # Dominant with no 3rd 1st Inversion (G, Bb, C)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.dominant_no_third_2nd_inv):
            return f"{branch}7sus/{root}", "dominant_no_third_2nd_inv"                                                # Dominant with no 3rd 2nd Inversion (Bb, C, G)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.dominant_no_fifth):
            return f"{root}7", "dominant_no_fifth"                                                                    # Dominant with no 5th
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.dominant_no_fifth_1st_inv):
            return f"{leaf}7/{root}", "dominant_no_fifth_1st_inv"                                                     # Dominant with no 5th 1st Inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.dominant_no_fifth_2nd_inv):
            return f"{branch}7/{root}", "dominant_no_fifth_2nd_inv"                                                   # Dominant with no 5th 2nd Inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.min6):
            return f"{root}min6", "min6"                                                                              # Minor 6 (Diminished 1st Inversion)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.min6_1st_inv):
            return f"{leaf}min6/{root}", "min6_1st_inv"                                                               # Minor 6 1st inv (Diminished 2nd Inversion)
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_no_third):
            return f"{root}maj7sus", "maj7_no_third"                                                                  # Major 7 no 3rd
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_no_third_1st_inv):
            return f"{leaf}maj7sus/{root}", "maj7_no_third_1st_inv"                                                   # Major 7 no 3rd 1st Inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_no_third_2nd_inv):
            return f"{branch}maj7sus/{root}", "maj7_no_third_2nd_inv"                                                 # Major 7 no 3rd 2nd Inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_no_fifth):
            return f"{root}maj7", "maj7_no_fifth"                                                                     # Major 7 no 5th
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_no_fifth_1st_inv):
            return f"{leaf}maj7/{root}", "maj7_no_fifth_1st_inv"                                                      # Major 7 no 5th 1st Inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_no_fifth_2nd_inv):
            return f"{branch}maj7/{root}", "maj7_no_fifth_2nd_inv"                                                    # Major 7 no 5th 2nd Inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.mush):
            return f"{root} mush", "mush"                                                                             # Mush
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_add2):
            return f"{root} maj7/9", "maj7_add2"                                                                      # Major 7/9 no third no fifth
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_add2_1st_inv):
            return f"{leaf} maj7/9/{root}", "maj7_add2_1st_inv"                                                       # Major 7/9 no third no fifth 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_add2_2nd_inv):
            return f"{branch} maj7sus2(no5)/{root}", "maj7_add2_2nd_inv"                                              # Major 7/9 no third no fifth 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.dim_maj7_no_fifth):
            return f"{root} dim maj7", "dim_maj7_no_fifth"                                                            # Diminished major 7 with no fifth
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.dim_maj7_no_fifth_1st_inv):
            return f"{leaf} dim maj7/{root}", "dim_maj7_no_fifth_1st_inv"                                             # Diminished major 7 with no fifth 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.dim_maj7_no_fifth_2nd_inv):
            return f"{root} phryg", "dim_maj7_no_fifth_2nd_inv"                                                       # Diminished major 7 with no fifth 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sus_maj47):
            return f"{root}maj7sus4 ", "sus_maj47"                                                                    # Suspended 4th with a major 7th 
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sus_maj47_1st_inv):
            return f"{leaf}maj7sus4/{root}", "sus_maj47_1st_inv"                                                      # Suspended 4th with a major 7th 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sus_maj47_2nd_inv):
            return f"{branch}maj7sus4/{root}", "sus_maj47_2nd_inv"                                                    # Suspended 4th with a major 7th 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_flat5):
            return f"{root}maj7\u266d5", "maj7_flat5"                                                                 # Major 7 flat 5
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_flat5_1st_inv):
            return f"{leaf}maj7\u266d5/{root}", "maj7_flat5_1st_inv"                                                  # Major 7 flat 5 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_flat5_2nd_inv):
            return f"{branch}maj7\u266d5/{root}", "maj7_flat5_2nd_inv"                                                # Major 7 flat 5 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.majmin):
            return f"{root}maj min", "majmin"                                                                         # Major Minor
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.aug_maj7_3rd_inv_no_third):
            return f"{branch}aug/{root}", "aug_maj7_3rd_inv_no_third"                                                 # Major Minor 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.aug_maj7_no_third):
            return f"{root}aug maj7", "aug_maj7_no_third"                                                             # Augmented maj7
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sus67):
            return f"{root}maj7sus(add6)", "sus67"                                                                    # Suspened maj7 add 6
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.min_add2_no_fifth):
            return f"{root}min(add2)", "min_add2_no_fifth"                                                            # Minor add 2
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.min_add2_no_fifth_1st_inv):
            return f"{leaf}min(add2)/{root}", "min_add2_no_fifth_1st_inv"                                             # Min add2 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.min7_no5):
            return f"{root}min7(no5)", "min7_no5"                                                                     # Min7 no 5th
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sus56):
            return f"{root}sus6", "sus56"                                                                             # Sus chord add 6
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.min7_no5_2nd_inv):
            return f"{branch}min7(no5)/{root}", "min7_no5_2nd_inv"                                                    # Min7 no 5th 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.major_flat5):
            return f"{root}maj \u266d5", "major_flat5"                                                                # Major flat 5
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.major_flat5_1st_inv):
            return f"{leaf}maj \u266d5/{root}", "major_flat5_1st_inv"                                                 # Major flat 5 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.major_flat5_2nd_inv):
            return f"{root}7 \u266d5", "major_flat5_2nd_inv"                                                          # Major flat 5 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj79):
            return f"{root}maj7/9", "maj79"                                                                           # Major 7 add 9
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj79_1st_inv):
            return f"{leaf}maj7/9/{root}", "maj79_1st_inv"                                                            # Major 7 add 9 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj79_2nd_inv):
            return f"{branch}maj7/9/{root}", "maj79_2nd_inv"                                                          # Major 7 add 9 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj_flat9):
            return f"{root}maj \u266d9", "maj_flat9"                                                                  # Major flat 9
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj_flat9_1st_inv):
            return f"{leaf}maj \u266d9/{root}", "maj_flat9_1st_inv"                                                   # Major flat 9 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj_flat9_2nd_inv):
            return f"{branch}maj \u266d9/{root}", "maj_flat9_2nd_inv"                                                 # Major flat 9 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj_add9):
            return f"{root}maj(add9no5)", "maj_add9"                                                                  # Major add 9 no fifth
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj_add9_1st_inv):
            return f"{leaf}maj(add9no5)/{root}", "maj_add9_1st_inv"                                                   # Major add 9 no fifth 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj_add9_2nd_inv):
            return f"{branch}maj(add9no5)/{root}", "maj_add9_2nd_inv"                                                 # Major add 9 no fifth 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_flat13):
            return f"{root}maj7/\u266d13(no3no5)", "maj7_flat13"                                                      # Major 7 flat 13 no third no fifth
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sus4_flat9):
            return f"{root}sus4/\u266d9(no3no5)", "sus4_flat9"                                                        # Sus 4 flat 9 no third no fifth
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sus49):
            return f"{root}sus4(add9no5)", "sus49"                                                                    # Sus 4 add 9 no fifth
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sus49_1st_inv):
            return f"{leaf}sus4(add9no5)/{root}", "sus49_1st_inv"                                                     # Sus 4 flat 9 no third no fifth 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.min_sus4):
            return f"{root}min sus4(no5)", "min_sus4"                                                                 # Sus 4 flat 9 no third no fifth 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.dominant_no_third_var):
            return f"{root}7(no3)", "dominant_no_third_var"                                                           # Dominant no third 
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.six_nine):
            return f"{root} 6/9", "six_nine"                                                                          # Six nine chord
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_no_third_var):
            return f"{root}maj7(no3)", "maj7_no_third_var"                                                            # Major7 no third high fifth
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_no_third_var_1st_inv):
            return f"{leaf}maj7(no3)/{root}", "maj7_no_third_var_1st_inv"                                             # Major7 no third high fifth 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_no_third_var_2nd_inv):
            return f"{branch}maj7(no3)/{root}", "maj7_no_third_var_2nd_inv"                                           # Major7 no third high fifth 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sharp11_no_third):
            return f"{root}\u266f11(no3)", "sharp11_no_third"                                                         # Sharp 11 no third
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sharp11_no_third_1st_inv):
            return f"{leaf}\u266f11(no3)/{root}", "sharp11_no_third_1st_inv"                                          # Sharp 11 no third 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.sharp11_no_third_2nd_inv):
            return f"{branch}\u266f11(no3)/{root}", "sharp11_no_third_2nd_inv"                                        # Sharp 11 no third 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.dominant_no_fifth_var):
            return f"{root}7(no5)", "dominant_no_fifth_var"                                                           # Dominant no fifth
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.dominant_no_fifth_var_1st_inv):
            return f"{leaf}7(no5)/{root}", "dominant_no_fifth_var_1st_inv"                                            # Dominant no fifth 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.dominant_no_fifth_var_2nd_inv):
            return f"{branch}7(no5)/{root}", "dominant_no_fifth_var_2nd_inv"                                          # Dominant no fifth 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj_flat5_var):
            return f"{root}maj\u266d5", "maj_flat5_var"                                                               # Major flat 5 
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj_flat5_var_1st_inv):
            return f"{leaf}maj\u266d5/{root}", "maj_flat5_var_1st_inv"                                                # Major flat 5 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj_flat5_var_2nd_inv):
            return f"{branch}maj\u266d5/{root}", "maj_flat5_var_2nd_inv"                                              # Major flat 5 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_flat5_var):
            return f"{root}maj7\u266d5", "maj7_flat5_var"                                                             # Major 7 flat 5 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_flat5_var_1st_inv):
            return f"{leaf}maj7\u266d5/{root}", "maj7_flat5_var_1st_inv"                                              # Major 7 flat 5 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.maj7_flat5_var_2nd_inv):
            return f"{branch}maj7\u266d5/{root}", "maj7_flat5_var_2nd_inv"                                            # Major 7 flat 5 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.min6_var):
            return f"{root}min6(no5)", "min6_var"                                                                     # Minor 6
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.min6_var_2nd_inv):
            return f"{branch}min6(no5)/{root}", "min6_var_2nd_inv"                                                    # Minor 6 2nd inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.min9_no5):
            return f"{root}min9(no5)", "min9_no5"                                                                     # Minor 9 no fifth
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.min9_no5_1st_inv):
            return f"{leaf}min9(no5)/{root}", "min9_no5_1st_inv"                                                      # Minor 9 no fifth 1st inversion
        elif self.triad_definitions.query(interval_set=intervals, valid_interval_set=self.triad_definitions.min9_no5_2nd_inv):
            return f"{branch}min9(no5)/{root}", "min9_no5_2nd_inv"                                                    # Minor 9 no fifth 2nd inversion
    
        return None
    
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
    
    def remove_harmonically_redundant_intervals(self, message_heap: list[list[int]]):
        """Take in a message heap and return a sorted message heap with redundant harmonies excluded 

        Args:
            message_heap (list[list[int]]): a message heap of the form [[note, instance_index, status, velocity], ...] 

        Returns:
            list[list[int]]: a sorted message heap with redundant harmonies removed
        """
        
        sorted_message_heap:        list[list[int]]             = sorted(message_heap, key=lambda x: x[0])
        instance_indices:           list[int]                   = [indices[1] for indices in sorted_message_heap]
        
        unique_instances = []
        instances_to_remove = []
        for index, instance in enumerate(instance_indices):
            if instance not in unique_instances:
                unique_instances.append(instance)
            else:
                instances_to_remove.append(index)
                
        harmonically_unique_message_heap = []
        for index, message in enumerate(sorted_message_heap):
            if index not in instances_to_remove:
                harmonically_unique_message_heap.append(message)
                
        return harmonically_unique_message_heap