from .test.MidiInjector import MidiInjector
from .music.scales.HarmonicMajorScales import get_harmonic_major_scales_dict
from .music.scales.HarmonicMinorScales import get_harmonic_minor_scales_dict
from .music.scales.MajorScales import get_major_scales_dict
from .music.scales.MelodicMinorScales import get_melodic_minor_scales_dict
from .utilities.DataClasses import Scale
from .utilities.Dictionaries import get_midi_notes

from multiprocessing import shared_memory
import numpy as np
import psutil
import time

class JacobsLadder:
    
    def __init__(self):
        self.midi_injector = MidiInjector()
        self.harm_maj_scales = get_harmonic_major_scales_dict()
        self.harm_min_scales = get_harmonic_minor_scales_dict()
        self.maj_scales      = get_major_scales_dict()
        self.mel_min_scales  = get_melodic_minor_scales_dict()
        
        self.shared_key = shared_memory.SharedMemory(name='shared_key', create=False)
        self.menu()
        
    def access_shared_key(self):
        previous_keys=None
        try:
            while True:
                
                keys = list(np.ndarray((28,), dtype="<U20", buffer=self.shared_key.buf))
                keys = sorted([key for key in keys if key != ''])

                if keys != previous_keys:
                    key_gen = self.key_generator(keys_list=keys)
                    for key in key_gen:
                        print(f"key {key}")
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
                        print(reduced_scale)
                        self.midi_injector.play_scale(note_list=full_scale[24:32], dur_list=[0.3] * len(full_scale[24:36]))
                    
                    previous_keys = keys
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("Exiting...")
            
    def key_generator(self, keys_list: list):
        for key in keys_list:
            new_keys = list(np.ndarray((28,), dtype="<U20", buffer=self.shared_key.buf))
            new_keys = sorted([key for key in new_keys if key != ''])
            if keys_list != new_keys:
                print(f"keys_list {keys_list}\n\n")
                print(f"new_keys {new_keys} \n\n")
                break
            yield key
                
        
    def menu(self):
        while True:
            print("Choose from the following options:")
            print("1. Play active scales")
            print("Quit/Q")
      
            choice = input("Enter your choice: ").lower()

            if choice == "1":
                self.access_shared_key()
                
            elif choice == "quit" or choice == "q":
                print("Exiting the program.")
                self.shared_key.close()
                self.shared_key.unlink()
                break
            else:
                print("Invalid choice. Please choose again.")
                
                
if __name__ == "__main__":
    jl = JacobsLadder()
    