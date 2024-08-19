import threading
import time

from .MidiManager import MidiController
from .HarmonicMajorScales import get_harmonic_major_scales_dict
from .HarmonicMinorScales import get_harmonic_minor_scales_dict
from .MajorScales import get_major_scales_dict
from .MelodicMinorScales import get_melodic_minor_scales_dict
from .ScaleClassifier import ScaleClassifier
from .MidiInjector import MidiInjector
from .DataClasses import Scale


class JacobsLadder:
    """Jacob is a Class which was built as a tool for learning. The tool provides a menu for displaying information and 
    interacting with the user in real time."""
    
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
        
        self.menu()
            
    def initialize_midi_controller(self):
        """Initializes a MidiController instance in a separate thread for interacting with the user in real time"""
        self.midi_controller = MidiController(input_port="jacob", output_ports=list(map(str, range(12, 24))))
                
        
    def menu(self):
        """Main control loop for diplaying menu options to the user"""
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
                            # TODO: replace shared memory logic with UDP logic 
                            pass
                            
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
            
    def play_active_scales(self, playback_speed: float, num_voices=1):
        """Play all scales which are congruent with the currently held down notes as the notes evolve and change.  If the currently
        held down notes change, then change the set of scales played over those notes.  Useful in determining harmonic possibilities of a chord.

        Args:
            playback_speed (float): the number of miliseconds to play each note for in the scale
        """
        previous_keys=None
        try:
            while True:
                # TODO: Replace shared memory implementation with UDP 
                pass
        except KeyboardInterrupt:
            print("Exiting...")
        
                
if __name__ == "__main__":
    jl = JacobsLadder()
    