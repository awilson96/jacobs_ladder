import threading
import time
from multiprocessing import shared_memory

import numpy as np

from .MidiManager import MidiController
from .HarmonicMajorScales import get_harmonic_major_scales_dict
from .HarmonicMinorScales import get_harmonic_minor_scales_dict
from .MajorScales import get_major_scales_dict
from .MelodicMinorScales import get_melodic_minor_scales_dict
from .ScaleClassifier import ScaleClassifier
from .MidiInjector import MidiInjector
from .DataClasses import Scale


class JacobsLadder:
    """
    Jacob is a Class which was built as a tool for learning. The tool provides a menu for displaying information and interacting with the user in real time.
    The class uses a shared memory buffer to snoop on message traffic published by the MidiManager class and use that data to assist the user with various tasks.
    """
    
    def __init__(self):
        self.midi_injector = MidiInjector(output_port="jacob")
        self.scale_classifier = ScaleClassifier()
        self.midi_controller_thread = threading.Thread(target=self.initialize_midi_controller)
        self.midi_controller_thread.start()
        time.sleep(0.1)
        
        self.harm_maj_scales = get_harmonic_major_scales_dict()
        self.harm_min_scales = get_harmonic_minor_scales_dict()
        self.maj_scales      = get_major_scales_dict()
        self.mel_min_scales  = get_melodic_minor_scales_dict()
        
        self.shared_key = shared_memory.SharedMemory(name='shared_key1', create=False)
        self.messages = shared_memory.SharedMemory(name='messages1', create=False)
        self.terminate1 = shared_memory.SharedMemory(name='terminate1', create=False)
        self.terminate2 = shared_memory.SharedMemory(name='terminate2', create=False)
        self.menu()
            
    def initialize_midi_controller(self):
        """Initializes a MidiController instance in a separate thread for interacting with the user in real time"""
        self.midi_controller = MidiController(input_port="jacob", output_ports=list(map(str, range(12, 24))))
            
    def key_generator(self, keys_list: list):
        """Creates a scale generator yielding a list of notes 

        Args:
            keys_list (list): a list of scales in the shared memory buffer in the form of strings

        Yields:
            list: A scale in the form of a list of Midi notes
        """
        for key in keys_list:
            new_keys = list(np.ndarray((28,), dtype="<U20", buffer=self.shared_key.buf))
            new_keys = sorted([key for key in new_keys if key != ''])
            if keys_list != new_keys:
                break
            yield key
                
        
    def menu(self):
        """Main control loop for siplaying menu options to the user"""
        try:
            while True:
                print("Choose from the following options:")
                print("1. Play active scales")
                print("2. Display active keys")
                print("3. Print messages")
                print("4. Play generated scales")
                print("Quit/Q")
        
                choice = input("Enter your choice: ").lower()

                if choice == "1":
                    print("Choose from the following options:")
                    print("1. Play scale version")
                    print("2. Play chord version")
                    selection = input("Enter your selection: ")
                    while True:
                        speed = input("Enter the playback speed in ms or press q to exit: ")
                        if speed.lower() in ["q", "quit"]:
                                break
                        if selection == "1":
                            if speed == '':
                                self.play_active_scales(0.15)
                                continue
                            speed = float(speed)
                            if 0.009 <= speed <= 2.0:
                                self.play_active_scales(speed)
                            else:
                                print("Speed must be between 0.009 and 2.0")

                        elif selection == "2":
                            num_voices = input("Enter the number of voices: ")
                            num_voices = int(num_voices)
                            if num_voices <= 1 or num_voices > 5:
                                print("Invalid number of voices, choose a number between 2 and 5!")
                            elif speed == '':
                                self.play_active_scales(playback_speed=0.15, num_voices=num_voices)
                            else:
                                self.play_active_scales(playback_speed=float(speed), num_voices=num_voices)
                            
                    
                        
                
                elif choice == "2":
                    try:
                        previous_keys = None
                        while True:
                            keys = list(np.ndarray((28,), dtype="<U20", buffer=self.shared_key.buf))
                            keys = sorted([key for key in keys if key != ''])
                            if keys != previous_keys:
                                print(keys)
                                
                            previous_keys = keys
                            
                    except KeyboardInterrupt:
                        print("Exitting...")
                
                elif choice == "3":
                    try:
                        previous_messages = None
                        while True:
                            messages = self.parse_messages()
                            if messages:
                                if messages != previous_messages:
                                    print(messages)
                                    
                            previous_messages = messages
                            
                    except KeyboardInterrupt:
                        print("Exitting...")
                        
                elif choice == "4":
                    print("Choose from the following options:")
                    print("1. Play scale version")
                    print("2. Play chord version")
                    try:
                        selection = input("Enter your selection: ")
                        # TODO: Use the most recently played note instead of hard-coding 60
                        scales = self.scale_classifier.convert_intervals(starting_note=60)
                        if selection == "1":
                            for scale in scales:
                                print(scale)
                                for _ in range(2):
                                    self.midi_injector.play_scale(note_list=scale, dur_list=[0.20]*len(scale))
                                    self.midi_injector.play_scale(note_list=scale[::-1][1:-1], dur_list=[0.20]*len(scale))
                        elif selection == "2":
                            num_voices = input("Enter the number of voices: ")
                            if int(num_voices) > 0 and int(num_voices) <= 5:
                                for scale in scales:
                                    harmonized_scale = self.scale_classifier.create_harmonized_scale(scale=scale, num_voices=int(num_voices))
                                    print(scale)
                                    for _ in range(2):
                                        for harmony in harmonized_scale:
                                            self.midi_injector.play_chord(note_list=harmony, duration=0.15, velocity=50)
                                        for harmony in harmonized_scale[::-1][1:-1]:
                                            self.midi_injector.play_chord(note_list=harmony, duration=0.15, velocity=50)
                                    
                            else:
                                print("Invalid number of voices: choose a number between 1 and 4.")
                        else:
                            print("Invalid selection")
                        
                            
                    except KeyboardInterrupt:
                        print("Exitting...")

                elif choice == "quit" or choice == "q":
                    print("Exiting the program.")
                    self.terminate_midi_controller()
                    break
                else:
                    print("Invalid choice. Please choose again.")
        except KeyboardInterrupt:
            print("Exiting...")
            self.terminate_midi_controller()
            
    def parse_messages(self):
        """Convert messages from nd-arrays in the shared memory buffer to actual MidiManager messages

        Returns:
            list[list]: a list of MidiManager messages placed in the shared memeory buffer
        """
        messages = np.ndarray((313, 4), dtype=np.int32, buffer=self.messages.buf)
   
        index = 0
        for arr in messages:
            index += 1
            if np.array_equal(arr, [0, 0, 0, 0]):
                index -= 1 
                break

        filtered_messages = messages[:index, :].tolist()
        filtered_messages = [mes for mes in filtered_messages if mes != [0, 0, 0, 0]]
        if filtered_messages:
            return filtered_messages
            
    def play_active_scales(self, playback_speed: float, num_voices=1):
        """Play all scales which are congruent with the currently held down notes as the notes evolve and change.  If the currently
        held down notes change, then change the set of scales played over those notes.  Useful in determining harmonic possibilities of a chord.

        Args:
            playback_speed (float): the number of miliseconds to play each note for in the scale
        """
        previous_keys=None
        try:
            while True:
                keys = list(np.ndarray((28,), dtype="<U20", buffer=self.shared_key.buf))
                keys = sorted([key for key in keys if key != ''])

                if keys != previous_keys:
                    key_gen = self.key_generator(keys_list=keys)
                    for key in key_gen:
                        print(f"{key}")
                        if key in self.maj_scales.keys():
                            scale = self.maj_scales[key]
                        elif key in self.harm_maj_scales.keys():
                            scale = self.harm_maj_scales[key]
                        elif key in self.harm_min_scales.keys():
                            scale = self.harm_min_scales[key]
                        elif key in self.mel_min_scales.keys():
                            scale = self.mel_min_scales[key]
                            
                        full_scale = self.midi_injector.create_scale(scale=Scale(name=key, notes=scale))
                        reduced_scale = self.midi_injector.reduce_scale(full_scale=full_scale, starting_note=key.split(" ")[0], num_octaves=1)
                        if num_voices == 1:
                            self.midi_injector.play_scale(note_list=reduced_scale, dur_list=[playback_speed] * len(reduced_scale))
                        elif num_voices > 1 and num_voices <= 5:
                            harmonized_scale = self.scale_classifier.create_harmonized_scale(scale=reduced_scale, num_voices=num_voices)
                            for harmony in harmonized_scale:
                                self.midi_injector.play_chord(note_list=harmony, duration=playback_speed, velocity=60)
                    
                    previous_keys = keys
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("Exiting...")
            
    def terminate_midi_controller(self):
        """Terminate all incoming and outgoing connections to Jacob and safely shut down"""
        self.terminate2.buf[0] = 1
        self.messages.close()
        self.messages.unlink()
        self.shared_key.close()
        self.shared_key.unlink()
        self.terminate1.close()
        self.terminate1.unlink()
        self.terminate2.close()
        self.terminate2.unlink()
        
                
if __name__ == "__main__":
    jl = JacobsLadder()
    