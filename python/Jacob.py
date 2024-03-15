import threading
import time
from multiprocessing import shared_memory

import numpy as np

from .MidiManager import MidiController
from .music.scales.HarmonicMajorScales import get_harmonic_major_scales_dict
from .music.scales.HarmonicMinorScales import get_harmonic_minor_scales_dict
from .music.scales.MajorScales import get_major_scales_dict
from .music.scales.MelodicMinorScales import get_melodic_minor_scales_dict
from .test.MidiInjector import MidiInjector
from .utilities.DataClasses import Scale


class JacobsLadder:
    
    def __init__(self):
        self.midi_injector = MidiInjector(output_port="jacob")
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
        self.midi_controller = MidiController(input_port="jacob", output_ports=list(map(str, range(12, 24))))
            
    def key_generator(self, keys_list: list):
        for key in keys_list:
            new_keys = list(np.ndarray((28,), dtype="<U20", buffer=self.shared_key.buf))
            new_keys = sorted([key for key in new_keys if key != ''])
            if keys_list != new_keys:
                break
            yield key
                
        
    def menu(self):
        try:
            while True:
                print("Choose from the following options:")
                print("1. Play active scales")
                print("2. Display active keys")
                print("3. Print messages")
                print("Quit/Q")
        
                choice = input("Enter your choice: ").lower()

                if choice == "1":
                    while True:
                        speed = input("Enter the playback speed in ms or press q to exit: ")
                        if speed == '':
                            self.play_active_scales(0.15)
                            continue
                        elif speed.lower() in ["q", "quit"]:
                            break
                    
                        speed = float(speed)
                        if 0.009 <= speed <= 2.0:
                            self.play_active_scales(speed)
                        else:
                            print("Speed must be between 0.009 and 2.0")
                
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
            
    def play_active_scales(self, playback_speed: float):
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
                        self.midi_injector.play_scale(note_list=reduced_scale, dur_list=[playback_speed] * len(reduced_scale))
                    
                    previous_keys = keys
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("Exiting...")
            
    def terminate_midi_controller(self):
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
    