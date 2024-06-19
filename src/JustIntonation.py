import logging
from collections import Counter

from .Enums import Pitch

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "November 11th 2023 (creation)"

logging.basicConfig(
    filename="./logs/JustIntonation.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class JustIntonation:
    """
    Just Intonation is a class used for pitch manipulating individual notes such that the outcome of each chord and/or melodic sequence remains in perfect pitch with the currenlty suspended notes.
    The secondary goal of the class is to ensure that after silence, new notes must be in pitch with the previously played notes creating pitch drift as would be expected in true Just Intonation.
    """
    def __init__(self):
        self.center_frequency = 8192
        self.pitch_table = {key: 8192 for key in range(-11, 12)}
        self.previous_root = [60, 0, 8192]
        self.root = [60, 0, 8192]
        
        self.calculate_pitch_table(offset=0)
        
    def calculate_pitch_table(self, offset):
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

        sorted_notes = sorted(notes)
        if len(sorted_notes) > 1:
            for idx in range(len(sorted_notes) - 1):
                intervals.append(notes[idx + 1] - notes[idx])

        if len(intervals) == 1:
            if intervals[0] >= 0:
                return intervals[0] % 12
            else:
                return -1 * (intervals[0] % 12)
        return intervals

    def get_pitch_bend_message(self, message_heap_elem: list, pitch_bend_amount: int):
        """
        Gets the formed MIDI pitch bend message to be sent by the MidiManager

        Args:
            message_heap_elem (list): a singular message_heap list represnting a single note plus metadata of the form [note, instance_index, status, velocity]
            pitch_bend_amount (int): number from 0-16383, 8192 is no tuning, 0 is max tune down, 16383 is max tune up
        """

        # Ensure pitch bend amount is within the valid range
        pitch_bend_amount = max(0, min(16383, pitch_bend_amount))

        # Calculate the LSB (Least Significant Byte) and MSB (Most Significant Byte) of the pitch bend value
        lsb = pitch_bend_amount & 0x7F
        msb = (pitch_bend_amount >> 7) & 0x7F

        # Status byte for pitch bend message NOTE_ON status + offset to convert to pitch bend message
        status_byte = message_heap_elem[2] + 80

        # Log the pitch bend message
        pitch_bend_message = [status_byte, lsb, msb]

        return pitch_bend_message

    def pitch_adjust_chord(self, message_heap: list[list], current_msg: list, dt: float, chord=None):
        """Adjust the pitch of individual notes within a given chord
        If the chord is unknown then it will be tuned using intervals instead

        Args:
            message_heap (list[list]): an unsorted list of notes with their metadata
            chord (string, optional): a unique string representation of the chord being played. Defaults to None.

        Returns:
            list[tuple(pitch_bend_message, instance_index)]: a list of actions in the form of pitch bend messages to be sent by certain instance indices.
        """
        print(f"dt {dt}")
        
        current_note, instance_index, _, _ = current_msg
        if len(message_heap) == 1:
            interval = self.get_intervals(notes=[self.root[0], current_note])
            offset = self.pitch_table[interval] - self.center_frequency
            self.calculate_pitch_table(offset=offset)
            self.root = (current_note, instance_index, self.pitch_table[interval])
            print(f"current_note {current_note}")
            print(f"instance_index {instance_index}")
            print(f"interval {interval}")
            print(f"offset {offset}")
            print(self.pitch_table)
            print(self.root)
            print()
            
        # TODO: Handle different ordering of notes by using dt from MidiController 
        
        if dt <= 0.01:
            print("fast")
        else:
            pass
        
        # Get the interval between the current root and the current note for possible tuning
        interval = self.get_intervals(notes=[self.root[0], current_note])
        pitch = self.pitch_table[interval]
        pitch_bend_message = self.get_pitch_bend_message(message_heap_elem=current_msg, pitch_bend_amount=pitch)
        print(f"interval {interval}")
        print(f"pitch {pitch}")
        print(f"pitch_bend_message {pitch_bend_message}")
        print()
        return pitch_bend_message, instance_index
        
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