import logging
import time
import numpy as np

from .Dictionaries import get_midi_notes
from .MajorScales import get_major_scales
from .MelodicMinorScales import get_melodic_minor_scales
from .HarmonicMajorScales import get_harmonic_major_scales
from .HarmonicMinorScales import get_harmonic_minor_scales
from .DataClasses import Scale

import rtmidi

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "November 8th 2023 (creation)"

logging.basicConfig(
    filename="./logs/MidiInjector.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class MidiInjector:
    """
    This is a Midi Injector which sends in Midi Data to a specified MIDI port for playing back audio to the user
    """

    # TODO: Look into standardizing these ports as well as the port setup.  See if there is a more robust way to use
    # pyautogui and/or find a new backend solution to configure LoopMidi with predefined ports 
    # TODO: Look into packaging options, containerization, etc... Figure out how to wrap other people's existing 
    # software into my software package. 
    # TODO: Figure out how to make my software work for other software synths with port support and start writing 
    # interfaces/configuration files to automatically interface with commonly used software.
    def __init__(self, output_port="jacob"):
        """Given an output MIDI port, the MidiInjector can be used to send MIDI data for the purposes of playing audio back to the user

        Args:
            output_port (str, optional): Name of the output port you want to send Midi data on. Defaults to "jacob".
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
                
    def create_full_scale(self, scale: Scale):
        """Given a Scale object, create a full scale with all of the possible notes

        Args:
            scale (Scale): a scale object which can be used to create the full scale

        Returns:
            list[int]: a list of integer MIDI notes representing the full scale
        """
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
        """TODO: Replace this function with something better

        Args:
            full_scale (list[int]): A full list of MIDI notes representing a specific scale
            starting_note (str): The letter name of the note you are interested in starting from in your scale
            num_octaves (_type_): the number of octaves to include from the starting note

        Returns:
            list[int]: a reduced scale based on filtering criteria
        """
        starting_note = self.find_starting_index(starting_note)
        full_scale_index = full_scale.index(starting_note)
        print(f"starting_note {starting_note}")
        print(f"full_scale_index {full_scale_index}")
        reduced_scale = full_scale[full_scale_index:full_scale_index + ((num_octaves * 7) + 1)]
        print(f"reduced_scale {reduced_scale}")
        print()
        
        return reduced_scale
    
    def find_starting_index(self, starting_note):
        """TODO: Replace this function with something better

        Args:
            starting_note (str): the name of the note you are interested in finding the starting index of

        Returns:
            int: the closest index to of this note to middle C
        """
        starting_note_indices = [midi_note for midi_note, note_name in self.int_note.items() if note_name == starting_note]
        closest_note = min(starting_note_indices, key=lambda x: abs(x - 61))
        return closest_note

    def play_chord(self, note_list: list, duration: float, velocity: int):
        """Play a chord by sending note-on messages for the specified notes and holding them for 2 seconds

        Args:
            note_list (list[int]): A list of notes you would like to play simultaneously
        """
        for note in note_list:
            self.send_note_on(note, int(velocity))
        time.sleep(float(duration))
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


if __name__ == "__main__":
    midi_injector = MidiInjector()

    midi_injector.play_scale(midi_injector.harmonic_major_scales[0].notes + ["C"], [0.10] * (len(midi_injector.harmonic_major_scales[0].notes)+1))
    midi_injector.play_scale(reversed(midi_injector.harmonic_major_scales[0].notes[1:]), [0.12] * (len(midi_injector.harmonic_major_scales[0].notes)+1))

    midi_injector.play_scale(midi_injector.harmonic_minor_scales[0].notes + ["C"], [0.12] * (len(midi_injector.harmonic_minor_scales[0].notes)+1))
    midi_injector.play_scale(reversed(midi_injector.harmonic_minor_scales[0].notes[1:]), [0.10] * (len(midi_injector.harmonic_minor_scales[0].notes)+1))
        
    C_Harm_maj_full_scale = midi_injector.create_full_scale(midi_injector.harmonic_major_scales[0])
    midi_injector.play_scale(C_Harm_maj_full_scale[:-1], [0.20] * (len(C_Harm_maj_full_scale)-1))
    midi_injector.play_scale(reversed(C_Harm_maj_full_scale), [0.20] * len(C_Harm_maj_full_scale))