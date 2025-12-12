from collections import Counter
from copy import copy
from itertools import combinations
import time

from .Dictionaries import midi_notes
from .Enums import Pitch
from .Logging import setup_logging
from .Utilities import determine_octave, get_root_from_letter_note, remove_harmonically_redundant_intervals
from .TuningUtils import read_tuning_config
from jacobs_ladder.bindings.tuning_utils import generate_tunings

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "November 11th 2023 (creation)"

class JustIntonation:
    """Just Intonation is a class used for pitch manipulating individual notes such that the outcome of each 
    chord and/or melodic sequence remains in perfect pitch with the currenlty suspended notes. The secondary goal 
    of the class is to ensure that after silence, new notes must be in pitch with the previously played notes 
    creating pitch drift as would be expected in true Just Intonation."""
    def __init__(self, **kwargs):

        allowed_keys = {"player", "tuning", "tuning_mode", "tuning_config", "tuning_ratios_pref", "tuning_ratios_all"}

        for key in kwargs:
            if key not in allowed_keys:
                raise ValueError(f"Unknown argument: {key}")
            
        self.player = kwargs.get("player", "User")
        self.logger = setup_logging(f"JustIntonation{self.player.capitalize()}")
        self.center_frequency = 8192
        self.pitch_table = {key: 8192 for key in range(-11, 12)}
        self.previous_root = 60
        self.root = 60
        self.tuning = kwargs.get("tuning", None)
        self.tuning_mode = kwargs.get("tuning_mode", None)
        self.tuning_config = read_tuning_config(name=kwargs.get("tuning_ratios_all", "5-limit-ratios"))
        self.tuning_pref = read_tuning_config(name=kwargs.get("tuning_ratios_pref", "5-limit-pref"))
        self.tuning_limit = kwargs.get("tuning_limit", 5) 
        
        if self.tuning:
            self.calculate_pitch_table(offset=0)

        # print(f"{self.player=}")
        # print(f"{self.center_frequency=}")
        # print(f"{self.pitch_table=}")
        # print(f"{self.previous_root=}")
        # print(f"{self.root=}")
        # print(f"{self.tuning=}")
        # print(f"{self.tuning_mode=}")
        # print(f"{self.tuning_config=}")
        # print(f"{self.tuning_pref=}")
        # print(f"{self.tuning_limit=}")
        
    def calculate_pitch_table(self, offset):
        """Calculate the new pitch table based on the currently held down notes with respect to the most recently played note

        Args:
            offset (int): the amount of analog bits to adjust the pitch wheel in order for the pitch bend to track with pitch drift
        """
        temp_pitch_table = self.pitch_table.copy()
        for key, value in temp_pitch_table.items():
            self.pitch_table[key] = self.get_diad_pitch(interval=key) + offset
        
    def get_intervals(self, notes: list[int]):
        """Determine the intervals between notes

        Args:
            notes (list[int]): A list of unsorted integer notes

        Returns:
            list[int]: A sorted list of the intervals from the lowest note to the highest note
        """
        intervals = []

        for idx in range(len(notes) - 1):
            intervals.append((notes[idx + 1] - notes[idx]) % 12)

        return intervals

    def get_pitch_bend_message(self, message_heap_elem: list):
        """Gets the formed MIDI pitch bend message to be sent by the MidiManager

        Args:
            message_heap_elem (list): a singular message_heap list representing a single note plus metadata 
                                      of the form [note, instance_index, status, velocity, pitch]
        """
        # Ensure pitch bend amount is within the valid range
        pitch_bend_amount = max(0, min(16383, message_heap_elem[4]))

        # Calculate the LSB (Least Significant Byte) and MSB (Most Significant Byte) of the pitch bend value
        lsb = pitch_bend_amount & 0x7F
        msb = (pitch_bend_amount >> 7) & 0x7F

        # Status byte for pitch bend message NOTE_ON status + offset to convert to pitch bend message
        status_byte = message_heap_elem[2] + 80

        # Log the pitch bend message
        pitch_bend_message = [status_byte, lsb, msb]

        return pitch_bend_message

    def get_tuning_info(self, message_heap: list[list], current_msg: list, dt: float, key=None):
        """Adjust the pitch of individual notes within a given chord
        If the chord is unknown then it will be tuned using intervals instead

        Args:
            message_heap (list[list]): an unsorted list of notes with their metadata
            chord (string, optional): a unique string representation of the chord being played. Defaults to None.

        Returns:
            list[tuple(pitch_bend_message, instance_index)]: a list of actions in the form of pitch bend messages to be sent by certain instance indices.
        """
        if self.tuning_mode == "dynamic":
            self.previous_root = copy(self.root)
            if key and key != "unknown":
                self.root = get_root_from_letter_note(key.split(" ")[0])
            else:
                self.root = self.previous_root
            note = current_msg[0]
            tuning_index = determine_octave(message_heap=message_heap, note=note)
            octaves = [octave for octave in range(self.root + 12, 109, 12)]
            octaves += [octave for octave in range(self.root - 12, 20, -12)]
            octaves += [self.root]

            current_msg_index = message_heap.index(current_msg)
            if note in octaves:                
                message_heap[current_msg_index][4] = 8192
            else:
                min_diff = (-1, 108)
                differences = [(note - oct) for oct in octaves]
                
                for idx, diff in enumerate(differences):
                    if abs(diff) < min_diff[1]:
                        min_diff = (idx, abs(diff))
                shortest_difference = differences[min_diff[0]]
                if shortest_difference == -1:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["major_seventh_up"]
                elif shortest_difference == -2:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["minor_seventh_up"]
                elif shortest_difference == -3:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["major_sixth_up"]
                elif shortest_difference == -4:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["minor_sixth_up"]
                elif shortest_difference == -5:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["perfect_fifth_up"]
                elif shortest_difference == -6:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["tritone_up"]
                elif shortest_difference == 1:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["minor_second_up"]
                elif shortest_difference == 2:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["major_second_up"]
                elif shortest_difference == 3:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["minor_third_up"]
                elif shortest_difference == 4:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["major_third_up"]
                elif shortest_difference == 5:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["perfect_fourth_up"]
                elif shortest_difference == 6:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["tritone_up"]
                else:
                    print("something weird happened")

            pitch_bend_msg = self.get_pitch_bend_message(message_heap_elem=message_heap[current_msg_index])
    
            return tuning_index, pitch_bend_msg, message_heap
        
        elif self.tuning_mode == "static":
            note = current_msg[0]
            tuning_index = determine_octave(message_heap=message_heap, note=note)
            octaves = [octave for octave in range(self.root + 12, 109, 12)]
            octaves += [octave for octave in range(self.root - 12, 20, -12)]
            octaves += [self.root]

            current_msg_index = message_heap.index(current_msg)
            if note in octaves:                
                message_heap[current_msg_index][4] = 8192
            else:
                min_diff = (-1, 108)
                differences = [(note - oct) for oct in octaves]
                
                for idx, diff in enumerate(differences):
                    if abs(diff) < min_diff[1]:
                        min_diff = (idx, abs(diff))
                shortest_difference = differences[min_diff[0]]
                if shortest_difference == -1:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["major_seventh_up"]
                elif shortest_difference == -2:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["minor_seventh_up"]
                elif shortest_difference == -3:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["major_sixth_up"]
                elif shortest_difference == -4:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["minor_sixth_up"]
                elif shortest_difference == -5:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["perfect_fifth_up"]
                elif shortest_difference == -6:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["tritone_up"]
                elif shortest_difference == 1:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["minor_second_up"]
                elif shortest_difference == 2:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["major_second_up"]
                elif shortest_difference == 3:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["minor_third_up"]
                elif shortest_difference == 4:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["major_third_up"]
                elif shortest_difference == 5:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["perfect_fourth_up"]
                elif shortest_difference == 6:
                    message_heap[message_heap.index(current_msg)][4] = self.tuning["tritone_up"]
                else:
                    print("something weird happened")

            pitch_bend_msg = self.get_pitch_bend_message(message_heap_elem=message_heap[current_msg_index])
    
            return tuning_index, pitch_bend_msg, message_heap
        
        elif self.tuning_mode == "just-intonation":

            if len(message_heap) == 1:
                self.root = current_msg[0]
            else:
                sorted_message_heap = remove_harmonically_redundant_intervals(message_heap)
                keys = [k.split(" ")[0] for k in key]
            
        else:
            return None
        
    def get_diad_pitch(self, interval: int):
        """Given an interval between two notes, return the analog pitch value expressed as a range from 0-16383 

        Args:
            interval (int): intervalic distance between two notes

        Returns:
            int: analog value of pitch drift needed to correctly shift the pitch value of the note to its justly tuned form 
        """
        if interval == 0:
            return Pitch.octave.value
        elif interval == 1:
            return Pitch.minor_second_up.value
        elif interval == -1:
            return Pitch.minor_second_down.value
        elif interval == 2:
            return Pitch.major_second_up.value
        elif interval == -2:
            return Pitch.major_second_down.value
        elif interval == 3:
            return Pitch.minor_third_up.value
        elif interval == -3:
            return Pitch.minor_third_down.value
        elif interval == 4:
            return Pitch.major_third_up.value
        elif interval == -4:
            return Pitch.major_third_down.value
        elif interval == 5:
            return Pitch.perfect_fourth_up.value
        elif interval == -5:
            return Pitch.perfect_fourth_down.value
        elif interval == 6:
            return Pitch.tritone_up.value
        elif interval == -6:
            return Pitch.tritone_down.value
        elif interval == 7:
            return Pitch.perfect_fifth_up.value
        elif interval == -7:
            return Pitch.perfect_fifth_down.value
        elif interval == 8:
            return Pitch.minor_sixth_up.value
        elif interval == -8:
            return Pitch.minor_sixth_down.value
        elif interval == 9:
            return Pitch.major_sixth_up.value
        elif interval == -9:
            return Pitch.major_sixth_down.value
        elif interval == 10:
            return Pitch.minor_seventh_up.value
        elif interval == -10:
            return Pitch.minor_seventh_down.value
        elif interval == 11:
            return Pitch.major_seventh_up.value
        elif interval == -11:
            return Pitch.major_seventh_down.value
        
    def get_triad_pitch(self, chord: str):
        """Unused currently, may come in handy later

        Args:
            chord (str): the chord's name expressed as a string.  For list of strings, see get_triad in MusicTheory Class
        """
        if "major_triad" in chord:
            # Major (C, E, G) or (C, G, E)
            pass
        elif "major_triad_1st_inv" in chord:
            # Major 1st Inversion (E, G, C)
            pass
        elif "major_triad_1st_inv_var" in chord:
            # Major 1st Inversion (E, C, G)
            pass
        elif "major_triad_2nd_inv" in chord:
            # Major 2nd Inversion (G, C, E)
            pass
        elif "major_triad_2nd_inv_var" in chord:
            # Major 2nd Inversion (G, E, C)
            pass
        elif "minor_triad" in chord:
            # Minor (C, Eb, G)
            pass
        elif "minor_triad_1st_inv" in chord:
            # Minor 1st Inversion (Eb, G, C)
            pass
        elif "minor_triad_1st_inv_var" in chord:
            # Minor 1st Inversion (Eb, C, G)
            pass
        elif "minor_triad_2nd_inv" in chord:
            # Minor 2nd Inversion (G, C, Eb)
            pass
        elif "minor_triad_2nd_inv_var" in chord:
            # Minor 2nd Inversion (G, Eb, C)
            pass
        elif "add2" in chord:
            # Add 2 chord
            pass
        elif "add2_1st_inv" in chord:
            # Add 2 chord 1st inversion
            pass
        elif "add2_2nd_inv" in chord:
            # Add 2 chord 2nd inversion
            pass
        elif "diminished" in chord:
            # Diminished (C, Eb, Gb) or (C, Gb, Eb)
            pass
        elif "augmented" in chord:
            # Augmented (C, E, Ab) or (C, Ab, E)
            pass
        elif "eleven_sus4" in chord:
            # Quartal chord (stacking fourths)
            pass
        elif "sus2" in chord:
            # Suspended 2
            pass
        elif "nine_chord" in chord:
            # 9 chord with no third
            pass
        elif "sus4" in chord:
            # Suspended 4
            pass
        elif "eleven_chord" in chord:
            # 11 chord with no third
            pass
        elif "dominant_no_third" in chord:
            # Dominant with no 3rd
            pass
        elif "dominant_no_third_1st_inv" in chord:
            # Dominant with no 3rd 1st Inversion
            pass
        elif "dominant_no_third_2nd_inv" in chord:
            # Dominant with no 3rd 2nd Inversion
            pass
        elif "dominant_no_fifth" in chord:
            # Dominant with no 5th
            pass
        elif "dominant_no_fifth_1st_inv" in chord:
            # Dominant with no 5th 1st Inversion
            pass
        elif "dominant_no_fifth_2nd_inv" in chord:
            # Dominant with no 5th 2nd Inversion
            pass
        elif "min6" in chord:
            # Minor 6 (Diminished 1st Inversion)
            pass
        elif "min6_1st_inv" in chord:
            # Minor 6 1st inv (Diminished 2nd Inversion)
            pass
        elif "maj7_no_third" in chord:
            # Major 7 no 3rd
            pass
        elif "maj7_no_third_1st_inv" in chord:
            # Major 7 no 3rd 1st Inversion
            pass
        elif "maj7_no_third_2nd_inv" in chord:
            # Major 7 no 3rd 2nd Inversion
            pass
        elif "maj7_no_fifth" in chord:
            # Major 7 no 5th
            pass
        elif "maj7_no_fifth_1st_inv" in chord:
            # Major 7 no 5th 1st Inversion
            pass
        elif "maj7_no_fifth_2nd_inv" in chord:
            # Major 7 no 5th 2nd Inversion
            pass
        elif "mush" in chord:
            # Mush
            pass
        elif "maj7_add2" in chord:
            # Major 7/9 no third no fifth
            pass
        elif "maj7_add2_1st_inv" in chord:
            # Major 7/9 no third no fifth 1st inversion
            pass
        elif "maj7_add2_2nd_inv" in chord:
            # Major 7/9 no third no fifth 2nd inversion
            pass
        elif "dim_maj7_no_fifth" in chord:
            # Diminished major 7 with no fifth
            pass
        elif "dim_maj7_no_fifth_1st_inv" in chord:
            # Diminished major 7 with no fifth 1st inversion
            pass
        elif "dim_maj7_no_fifth_2nd_inv" in chord:
            # Diminished major 7 with no fifth 2nd inversion
            pass
        elif "sus_maj47" in chord:
            # Suspended 4th with a major 7th
            pass
        elif "sus_maj47_1st_inv" in chord:
            # Suspended 4th with a major 7th 1st inversion
            pass
        elif "sus_maj47_2nd_inv" in chord:
            # Suspended 4th with a major 7th 2nd inversion
            pass
        elif "maj7_flat5" in chord:
            # Major 7 flat 5
            pass
        elif "maj7_flat5_1st_inv" in chord:
            # Major 7 flat 5 1st inversion
            pass
        elif "maj7_flat5_2nd_inv" in chord:
            # Major 7 flat 5 2nd inversion
            pass
        elif "majmin" in chord:
            # Major Minor
            pass
        elif "aug_maj7_3rd_inv_no_third" in chord:
            # Major Minor 1st inversion
            pass
        elif "aug_maj7_no_third" in chord:
            # Major Minor 2nd inversion
            pass
        elif "sus67" in chord:
            # Suspened maj7 add 6
            pass
        elif "min_add2_no_fifth" in chord:
            # Minor add 2
            pass
        elif "min_add2_no_fifth_1st_inv" in chord:
            # Min add2 1st inversion
            pass
        elif "min7_no5" in chord:
            # Min7 no 5th
            pass
        elif "sus56" in chord:
            # Sus chord add 6
            pass
        elif "min7_no5_2nd_inv" in chord:
            # Min7 no 5th 2nd inversion
            pass
        elif "major_flat5" in chord:
            # Major flat 5
            pass
        elif "major_flat5_1st_inv" in chord:
            # Major flat 5 1st inversion
            pass
        elif "major_flat5_2nd_inv" in chord:
            # Major flat 5 2nd inversion
            pass
        elif "maj79" in chord:
            # Major 7 add 9
            pass
        elif "maj79_1st_inv" in chord:
            # Major 7 add 9 1st inversion
            pass
        elif "maj79_2nd_inv" in chord:
            # Major 7 add 9 2nd inversion
            pass
        elif "maj_flat9" in chord:
            # Major flat 9
            pass
        elif "maj_flat9_1st_inv" in chord:
            # Major flat 9 1st inversion
            pass
        elif "maj_flat9_2nd_inv" in chord:
            # Major flat 9 2nd inversion
            pass
        elif "maj_add9" in chord:
            # Major add 9 no fifth
            pass
        elif "maj_add9_1st_inv" in chord:
            # Major add 9 no fifth 1st inversion
            pass
        elif "maj_add9_2nd_inv" in chord:
            # Major add 9 no fifth 2nd inversion
            pass
        elif "maj7_flat13" in chord:
            # Major 7 flat 13 no third no fifth
            pass
        elif "sus4_flat9" in chord:
            # Sus 4 flat 9 no third no fifth
            pass
        elif "sus49" in chord:
            # Sus 4 add 9 no fifth
            pass
        elif "sus49_1st_inv" in chord:
            # Sus 4 flat 9 no third no fifth 1st inversion
            pass
        elif "min_sus4" in chord:
            # Sus 4 flat 9 no third no fifth 1st inversion
            pass
        elif "dominant_no_third_var" in chord:
            # Dominant no third 
            pass
        elif "six_nine" in chord:
            # Six nine chord
            pass
        elif "maj7_no_third_var" in chord:
            # Major7 no third high fifth
            pass
        elif "maj7_no_third_var_1st_inv" in chord:
            # Major7 no third high fifth 1st inversion
            pass
        elif "maj7_no_third_var_2nd_inv" in chord:
            # Major7 no third high fifth 2nd inversion
            pass
        elif "sharp11_no_third" in chord:
            # Sharp 11 no third
            pass
        elif "sharp11_no_third_1st_inv" in chord:
            # Sharp 11 no third 1st inversion
            pass
        elif "sharp11_no_third_2nd_inv" in chord:
            # Sharp 11 no third 2nd inversion
            pass
        elif "dominant_no_fifth_var" in chord:
            # Dominant no fifth
            pass
        elif "dominant_no_fifth_var_1st_inv" in chord:
            # Dominant no fifth 1st inversion
            pass
        elif "dominant_no_fifth_var_2nd_inv" in chord:
            # Dominant no fifth 2nd inversion
            pass
        elif "maj_flat5_var" in chord:
            # Major flat 5 
            pass
        elif "maj_flat5_var_1st_inv" in chord:
            # Major flat 5 1st inversion
            pass
        elif "maj_flat5_var_2nd_inv" in chord:
            # Major flat 5 2nd inversion
            pass
        elif "maj7_flat5_var" in chord:
            # Major 7 flat 5 2nd inversion
            pass
        elif "maj7_flat5_var_1st_inv" in chord:
            # Major 7 flat 5 1st inversion
            pass
        elif "maj7_flat5_var_2nd_inv" in chord:
            # Major 7 flat 5 2nd inversion
            pass
        elif "min6_var" in chord:
            # Minor 6
            pass
        elif "min6_var_2nd_inv" in chord:
            # Minor 6 2nd inversion
            pass
        elif "min9_no5" in chord:
            # Minor 9 no fifth
            pass
        elif "min9_no5_1st_inv" in chord:
            # Minor 9 no fifth 1st inversion
            pass
        elif "min9_no5_2nd_inv" in chord:
            # Minor 9 no fifth 2nd inversion
            pass
        else:
            # Handle case where chord is not known
            pass

    def recenter_frequency(self, message_heap: list[list], instance_index: int):
        """Used to recenter the base frequencies of instances which are no longer in use

        Args:
            message_heap (list[list]): a list of notes with their metadata [note, instance_index, status, velocity]
            instance_index (int): the instance index of the note which has received the note off message
        """
        pass

    def select_tuning_ratio(self, relationship: tuple[int], method: str) -> dict:
        """Select a JI tuning based on the interval relationship. There are two supported methods, random (which 
        uniformly chooses a potential tuning matching the interval type) or singular which selects a preferred
        tuning based on user input at instantiation

        Args:
            relationship (tuple[int]): the tuple representing (index, reference, and relative_interval)
            method (str): a method for selecting a tuning ratio 

        Returns:
            dict: a dictionary with keys "ratio", "cents_offset", and "analog_pitch_wheel_value_offset"
        """
        assert method in ["random", "singular"]
        assert len(relationship) == 3 and isinstance(relationship[2], int)

        index, reference, relative_interval = relationship
        if relative_interval == 0:
            return {"ratio": '1/1', "cents_offset": 0.000, "analog_pitch_wheel_value_offset": 0}
        
        tuning_ratios = self.tuning_config[str(relative_interval)]
        if method == "random":
            choice = random.choice(tuning_ratios)
            ratio = str(list(choice.keys())[0])
            cents_offset = choice[ratio]["cents offset"]
            analog_pitch_wheel_value_offset = choice[ratio]["analog pitch wheel value offset"]
            return {"ratio": ratio, "cents_offset": cents_offset, 
                    "analog_pitch_wheel_value_offset": analog_pitch_wheel_value_offset}

        elif method == "singular":
            if len(tuning_ratios) == 1:
                return tuning_ratios[0]
            else:
                choice = self.tuning_pref[str(relative_interval)]
                ratio = str(list(choice[0].keys())[0])
                cents_offset = choice[0][ratio]["cents offset"]
                analog_pitch_wheel_value_offset = choice[0][ratio]["analog pitch wheel value offset"]
                return {"ratio": ratio, "cents_offset": cents_offset, 
                        "analog_pitch_wheel_value_offset": analog_pitch_wheel_value_offset}

    def display_tunings(self, tunings: list[list[tuple[int]]], tuning_config: dict):
        """Display the different tuning options available for a given chord

        Args:
            tunings (list[list[tuple[int]]]): a list of potential valid tunings for a given chord
            tuning_config (dict): a dictionary with tuning metadata for some n-limit JI list of frequency ratios
        """
        for tuning in tunings:
            ratios = []
            for relationship in tuning:
                ratios.append(self.select_tuning_ratio(relationship=relationship, tuning_config=tuning_config, method="random")["ratio"])
            print(f"{tuning}\t{ratios}")

if __name__ == "__main__":
    kwargs = {
        "player": "User", 
        "tuning": None, 
        "tuning_mode": "just-intonation", 
        "tuning_config": "7-limit-ratios", 
        "tuning_pref": "7-limit-pref"
    }
    JI = JustIntonation(**kwargs)
    tuning_ratio = JI.select_tuning_ratio(relationship=(1, 1, 10), method="singular")
    print(tuning_ratio)