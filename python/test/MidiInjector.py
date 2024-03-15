import logging
import time
import threading
import numpy as np
from ..utilities.Dictionaries import get_midi_notes
from ..music.scales.MajorScales import get_major_scales
from ..music.scales.MelodicMinorScales import get_melodic_minor_scales
from ..music.scales.HarmonicMajorScales import get_harmonic_major_scales
from ..music.scales.HarmonicMinorScales import get_harmonic_minor_scales
from ..utilities.DataClasses import Scale

import rtmidi

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "November 8th 2023 (creation)"

logging.basicConfig(
    filename="MidiManager.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class MidiInjector:
    """
    This is a Midi Injector which sends in Midi Data to a specified port for the purpose of testing MidiManager
    """

    # TODO: Look into standardizing these ports as well as the port setup.  See if there is a more robust way to use
    # pyautogui and/or find a new backend solution to configure LoopMidi with predefined ports 
    # TODO: Look into packaging options, containerization, etc... Figure out how to wrap other people's existing 
    # software into my software package. 
    # TODO: Figure out how to make my software work for other software synths with port support and start writing 
    # interfaces/configuration files to automatically interface with commonly used software.
    def __init__(self, output_port="jacobs_ladder"):
        """_summary_

        Args:
            output_port (str, optional): Name of the output port you want to send Midi data on. Defaults to "jacobs_ladder".
        """
        self.midi_out = rtmidi.MidiOut()
        self.output_ports = output_port
        self.initialize_port()
        self.int_note = get_midi_notes()
        self.major_scales = get_major_scales()
        self.melodic_minor_scales = get_melodic_minor_scales()
        self.harmonic_major_scales = get_harmonic_major_scales()
        self.harmonic_minor_scales = get_harmonic_minor_scales()

    def initialize_port(self):
        """Initialize the port specified in __init__ by opening that port for Midi out operations

        Raises:
            RuntimeError: If the port cannot be found, this funtion raises an error
        """
        try:
            available_output_ports = [port.split(" ", 1)[0] for port in self.midi_out.get_ports()]
            index = available_output_ports.index(self.output_ports)
            self.midi_out.open_port(index)

        except (ValueError, rtmidi._rtmidi.SystemError):
            raise RuntimeError(f"Failed to open output port '{index}'")

    def send_note_on(self, note, velocity):
        """Send a note-on message

        Args:
            note (int): The note number corresponding the key you want to send a note on message for
            velocity (int): The velocity of the note (0-127 inclusive)
        """
        note_on = [144, note, velocity]
        self.midi_out.send_message(note_on)

    def send_note_off(self, note):
        """Send a note-off message

        Args:
            note (int): The note number corresponding to the key you want to send a note off message for
        """
        note_off = [[128 + channel, note, 80] for channel in range(16)]
        for notes in note_off:
            self.midi_out.send_message(notes)

    def send_sustain_pedal_high(self):
        """Send a sustain pedal message (sustain pedal is held down)"""
        sustain_pedal_high = [176, 64, 127]
        self.midi_out.send_message(sustain_pedal_high)

    def send_sustain_pedal_low(self):
        """Send a sustain pedal message (sustain pedal is released)"""
        sustain_pedal_low = [176, 64, 0]
        self.midi_out.send_message(sustain_pedal_low)

    def toggle_sustain_pedal(self, dur):
        """Toggle the sustain pedal on and off

        Args:
            dur (float): time in seconds
        """
        self.send_sustain_pedal_high()
        time.sleep(dur)
        self.send_sustain_pedal_low()

    def play_scale(self, note_list, dur_list):
        """Send a list of notes and durations to be played

        Args:
            note_list (list[int]): A list of note numbers to be played one after another
            dur_list (list[float]): A list of durations which correspond to the length of each note in seconds
        """
        
        for note, dur in zip(note_list, dur_list):
            if isinstance(note, str):
                note_keys = [key for key, value in self.int_note.items() if value == note]
                for all_note in note_keys:
                    self.send_note_on(all_note, 80)
                    self.send_note_off(all_note)
                time.sleep(dur)
            elif isinstance(note, int):
                self.send_note_on(note, 80)
                time.sleep(dur)
                self.send_note_off(note)
                
    def create_scale(self, scale: Scale):
        full_scale = []
        lowest_note = min([key for key, value in self.int_note.items() if value == scale.notes[0]])
        highest_note = max([key for key, value in self.int_note.items() if value == scale.notes[0]])
        parsed_scale = scale.notes
        for note in parsed_scale:
            note_keys = [key for key, value in self.int_note.items() if value == note]
            full_scale.extend(note_keys)
            
        full_scale = [num for num in full_scale if lowest_note <= num <= highest_note]
        return sorted(full_scale)
    
    def reduce_scale(self, full_scale, starting_note, num_octaves):
        starting_note = self.find_starting_index(starting_note)
        full_scale_index = full_scale.index(starting_note)
        print(f"starting_note {starting_note}")
        print(f"full_scale_index {full_scale_index}")
        reduced_scale = full_scale[full_scale_index:full_scale_index + ((num_octaves * 7) + 1)]
        print(f"reduced_scale {reduced_scale}")
        print()
        
        return reduced_scale
    
    def find_starting_index(self, starting_note):
        starting_note_indices = [midi_note for midi_note, note_name in self.int_note.items() if note_name == starting_note]
        closest_note = min(starting_note_indices, key=lambda x: abs(x - 61))
        return closest_note

    def play_chord(self, note_list):
        """Play a chord by sending note-on messages for the specified notes and holding them for 2 seconds

        Args:
            note_list (list[int]): A list of notes you would like to play simultaneously
        """
        for note in note_list:
            self.send_note_on(note, 127)
        time.sleep(0.5)
        for note in note_list:
            self.send_note_off(note)
            
    def play_chord_by_intervals(self, interval_list):
        """Play a chord by sending note-on messages for the specified notes and holding them for 2 seconds

        Args:
            interval_list (list[int]): A list of intervals for constructing the chord
        """
        base_note = 60
        note_list = [base_note] + [base_note + interval for interval in list(np.cumsum(interval_list))]
        
        for note in note_list:
            self.send_note_on(note, 80)

        time.sleep(0.6)

        for note in note_list:
            self.send_note_off(note)
       

    def testPlayDistinctNotes(self):
        """
        Play note on messages followed by note off messages and ensure that instances are allocated correctly
        """

        note_list = [60, 62, 64, 65, 67, 69, 71, 72]
        dur_list = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.play_scale(note_list, dur_list)

    def testPlayOverlappingNotes(self):
        """
        Play notes which overlap to test that instances are allocated correctly and that all note on messages have a corresponding note off
        """

        # Create threads for testPlayDistinctNotes and play_chord
        thread_distinct_notes = threading.Thread(target=self.testPlayDistinctNotes)
        c_major_chord = [60, 64, 67]
        thread_chord = threading.Thread(target=self.play_chord, args=(c_major_chord,))

        # Start the threads
        thread_distinct_notes.start()
        thread_chord.start()

    def testPlayOverlappingNotesWithSustain(self):
        """
        Play overlapping notes and hold down the sustain pedal releasing it half way through
        """

        # Create threads for testPlayDistinctNotes and play_chord
        thread_overlapping_notes = threading.Thread(target=self.testPlayOverlappingNotes)
        duration = 0.7
        thread_sustain_pedal = threading.Thread(target=self.toggle_sustain_pedal, args=(duration,))
        
        # Start the threads
        thread_overlapping_notes.start()
        thread_sustain_pedal.start()
        
    def testIntervalSets(self):
        # interval_sets = [[i, j] for i in range(1, 12) for j in range(1, 12)]
        
        interval_sets = [[4, 3], [7, 9], [3, 5], [8, 7], [5, 4], [9, 8], [3, 4], [7, 8], [4, 5], [9, 7], [5, 3], [8, 9], [2, 2], 
                         [2, 8], [8, 2], [3, 3], [6, 9], [4, 4], [8, 8], [5, 5], [10, 7], [2, 5], [7, 7], [5, 2], [7, 10], [7, 3], 
                         [3, 2], [2, 7], [4, 6], [6, 2], [2, 4], [3, 6], [6, 3], [7, 4], [4, 1], [1, 7], [4, 7], [7, 1], [1, 4], 
                         [1, 1], [1, 10], [10, 1], [11, 2], [2, 11], [11, 11],[2, 9], [9, 1], [1, 2], [3, 8], [8, 1], [1, 3], 
                         [5, 6], [6, 1], [1, 5], [6, 5], [5, 1], [1, 6], [3, 1], [1, 8], [8, 3], [9, 2], [2, 1], [1, 9], [3, 7], 
                         [7, 2], [2, 3], [4, 2], [2, 6], [6, 4], [11, 3], [3, 10], [10, 11], [4, 9], [4, 10], [4, 11], [5, 8], 
                         [5, 9], [5, 10], [5, 11], [6, 7], [6, 8], [6, 10], [6, 11], [7, 2], [7, 6], [7, 11], [8, 5], [8, 6], 
                         [8, 10], [8, 11], [9, 4], [9, 5], [9, 6], [9, 9], [9, 10], [9, 11], [10, 3], [10, 4], [10, 5], [10, 6], 
                         [10, 8], [10, 9], [10, 10], [11, 2], [11, 4], [11, 5], [11, 6], [11, 7], [11, 8], [11, 9], [11, 10]]
        
        for interval_set in interval_sets:
            self.play_chord_by_intervals(interval_list=interval_set)


def main():
    midi_injector = MidiInjector()
    # midi_injector.testPlayDistinctNotes()
    # midi_injector.testPlayOverlappingNotes()
    # midi_injector.testPlayOverlappingNotesWithSustain()
    # midi_injector.testIntervalSets()

    midi_injector.play_scale(midi_injector.harmonic_major_scales[0].notes + ["C"], [0.10] * (len(midi_injector.harmonic_major_scales[0].notes)+1))
    midi_injector.play_scale(reversed(midi_injector.harmonic_major_scales[0].notes[1:]), [0.12] * (len(midi_injector.harmonic_major_scales[0].notes)+1))

    midi_injector.play_scale(midi_injector.harmonic_minor_scales[0].notes + ["C"], [0.12] * (len(midi_injector.harmonic_minor_scales[0].notes)+1))
    midi_injector.play_scale(reversed(midi_injector.harmonic_minor_scales[0].notes[1:]), [0.10] * (len(midi_injector.harmonic_minor_scales[0].notes)+1))
        
    C_Harm_maj_full_scale = midi_injector.create_scale(midi_injector.harmonic_major_scales[0])
    midi_injector.play_scale(C_Harm_maj_full_scale[:-1], [0.20] * (len(C_Harm_maj_full_scale)-1))
    midi_injector.play_scale(reversed(C_Harm_maj_full_scale), [0.20] * len(C_Harm_maj_full_scale))
    


if __name__ == "__main__":
    main()
