from .test.MidiInjector import MidiInjector
from .MidiManager import MidiController

from multiprocessing import shared_memory
import numpy as np
import psutil
import time

class JacobsLadder:
    
    def __init__(self):
        self.midi_injector = MidiInjector()
        
    def menu(self):
        
        while True:
            print("Choose from the following options:")
            print("1. Play active scales")
            print("Quit/Q")
      
            choice = input("Enter your choice: ").lower()

            if choice == "1":
                pass
                
            elif choice == "quit" or choice == "q":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please choose again.")
                
def access_shared_key():
    while True:
        shared_key = shared_memory.SharedMemory(name='shared_key', create=False)
        keys = list(np.ndarray((28,), dtype="<U20", buffer=shared_key.buf))
        keys = [key for key in keys if key != '']
        print(keys, "\n")
        time.sleep(2)
                
if __name__ == "__main__":
    jl = JacobsLadder()
    access_shared_key()
    