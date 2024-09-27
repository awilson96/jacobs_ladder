import argparse
import heapq
import json
import logging
import time
import warnings
from copy import copy, deepcopy

import rtmidi

from .JustIntonation import JustIntonation
from .MusicTheory import MusicTheory
from .Udp import UDPSender, UDPReceiver
from .Utilities import determine_octave
from .Logging import setup_logging

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "October 12th 2023 (creation)"

warnings.filterwarnings("ignore", message="RtMidiIn::getNextMessage.*user callback.*")


class MidiController:
    """
    This is a Midi Keyboard interface which allows for the manipulation of real time Midi data.
    MidiController maps 1 input port to 12 output ports used for single note manipulation.
    The MidiController does this to take advantage of the pitch wheel which globally alters the pitch of all 16 channels.
    By separating each note on to a unique rtmidi.MidiOut port, individual tuning of notes is possible.
    MidiController handles the mapping of a single port to 12 ports and all instance allocation and re-allocation.
    All tuning, chord display, and additional features are handled by other submodules.
    """

    def __init__(self, input_port: str = "jacobs_ladder", 
                 output_ports: list = list(map(str, range(12))), 
                 print_msgs: bool = False,
                 tuning: dict = None,
                 tuning_mode: str = None):
        """Class Constructor creates a MidiController object.  MidiController handles MIDI port management, 
        output port instance management, and sustain pedal management.

        Args:
            input_port (str, optional): input port name. Defaults to "jacobs_ladder".
            output_ports (list, optional): output port name. Defaults to list(map(str, range(12))).
            print_msgs (bool, optional): True if you wish to print msgs to the console. Defaults to False.
            tuning (dict, optional): a dictionary giving the controller its tuning. Defaults to None.
            tuning_mode (str, optional): static, dynamic, or None for no tuning. Defaults to None.
        """
        # Set up logging
        if input_port == "jacobs_ladder":
            self.logger = setup_logging("User")
        elif input_port == "jacob":
            self.logger = setup_logging("Jacob")
        else:
            self.logger = setup_logging(input_port)
        self.logger.info("Initializing MidiController...")
        
        # MIDI port management
        self.midi_in = rtmidi.MidiIn()
        self.midi_out_ports = [rtmidi.MidiOut() for _ in range(12)]
        self.input_port = input_port
        self.output_ports = output_ports
        self.logger.info(f"Input port: {input_port}")
        self.logger.info(f"Output ports: {output_ports}")
        
        # Set print settings
        self.print_msgs = print_msgs
        print(self.print_msgs)
        self.logger.info("Printing to the terminal is enabled") if self.print_msgs else \
            self.logger.info("Printing to the terminal is disabled")
        
        # Create midi in and midi out virtual port objects
        self.initialize_ports()

        # Output port instance management
        self.instance_index = list(range(12))
        self.message_heap = [] 
        self.in_use_indices = {}

        # Sustain pedal management
        self.sustain = False
        self.sustained_notes = []
        
        # Music Theory
        self.music_theory = MusicTheory(print_msgs=self.print_msgs, player=input_port if input_port != "jacobs_ladder" else "User")
        self.logger.info(f"Initializing MusicTheory...")

        # Tuning management
        self.tuning = tuning
        self.tuning_mode = tuning_mode
        self.logger.info("Initializing JustIntonation...")
        if self.tuning and self.tuning_mode: 
            self.logger.info("Tuning is enabled")
            self.logger.info(f"Mode is set to \"{self.tuning_mode}\" tuning")
        else:
            self.logger.info("Tuning is disabled")
        self.just_intonation = JustIntonation(player=input_port if input_port != "jacobs_ladder" else "User", 
                                              tuning=self.tuning,
                                              tuning_mode=tuning_mode)
            
        # Transposition Management
        self.transpose = 0
        
        # Communication with Jacob
        if self.output_ports == list(map(str, range(12))):
            self.udp_receiver = UDPReceiver(host='127.0.0.1', port=50000)
            self.udp_receiver.start_listener()
            self.udp_sender = UDPSender(host='127.0.0.1', port=50001)
            self.logger.info("Initializing connection to Jacob...")
        
        self.logger.info("Listening for Midi messages...")
        self.set_midi_callback()
        self.start_listening()
        
        self.logger.info("Exiting...")

    def initialize_ports(self):
        """
        Initialize input and output ports based on user provided values

        Raises:
            ValueError: If the input/output port is not found, an error is raised
            RuntimeError: If either a value error or a rtmidi system error is caught, then an error is raised
        """
        # Initialize MIDI input port
        try:
            available_input_ports = self.midi_in.get_ports()
            if self.print_msgs:
                print(f"available_input_ports \n{available_input_ports}")
            input_port_index = None
            for port in available_input_ports:
                if port.split(" ")[0] == (self.input_port):
                    input_port_index = available_input_ports.index(port)
                    break
            if input_port_index is not None:
                self.midi_in.open_port(input_port_index)
            else:
                raise ValueError(f"Input port '{self.input_port}' not found.")
        except (ValueError, rtmidi._rtmidi.SystemError):
            raise RuntimeError(f"Failed to open input port '{self.input_port}'")

        # Initialize MIDI output ports
        try:
            available_output_ports = [port.split(" ", 1)[0] for port in self.midi_out_ports[0].get_ports()]
            for midi_out_idx, port_name in enumerate(self.output_ports):
                if port_name in available_output_ports:
                    output_port_index = available_output_ports.index(port_name)
                    midi_out_port = self.midi_out_ports[midi_out_idx]
                    midi_out_port.open_port(output_port_index)
                else:
                    raise ValueError(f"Output port '{port_name}' not found.")
        except (ValueError, rtmidi._rtmidi.SystemError):
            raise RuntimeError(f"Failed to open output port '{port_name}'")

    def close_ports(self):
        """
        Closes all opened input and output ports.
        """
        # Close MIDI input port
        if self.midi_in.is_port_open():
            self.midi_in.close_port()

        # Close MIDI output ports
        for midi_out_port in self.midi_out_ports:
            if midi_out_port.is_port_open():
                midi_out_port.close_port()

    def filter(self, message: tuple, timestamp: float):
        """
        Filter used to set the MIDI callback.
        The MIDI callback filters out only the messages you want to process within the callback.
        The filter handles NOTE_ON, NOTE_OFF, CONTROL_CHANGE, and ALL_NOTES_OFF message types.
        The filter is called by start_listening() and can be thought of as the main control loop.

        Args:
            message (tuple): The raw MIDI message ([status, note, velocity], dt)
            timestamp (float): Empty variable, necessary for MIDI callback as the underlying C++ code 
            is expecting this function signiture
        """
        payload, dt  = message
        status, note, velocity = payload

        if status in range(144, 160):
            instance_index = determine_octave(message_heap=self.message_heap, note=note)
            if instance_index is None:
                if note not in [msg_note[0] for msg_note in self.message_heap]:
                    instance_index = heapq.heappop(self.instance_index)
                else:
                    logging.warning(f"no instances are left! {instance_index}")
                        
            self.in_use_indices[note] = instance_index
            heapq.heappush(self.message_heap, [note + self.transpose, instance_index, status, velocity, None])
            
            chord = self.music_theory.determine_chord(self.message_heap)
            key, candidate_keys = self.music_theory.determine_key(self.message_heap)
            self.udp_sender.send(candidate_keys)

            pitch_adjust_message = None
            if self.tuning:
                tuning_index, pitch_bend_message, message_heap = self.just_intonation.get_tuning_info(message_heap=self.message_heap, current_msg=[note, instance_index, status, velocity, None], dt=dt, chord=chord)
                self.message_heap = message_heap
                print(message_heap)

                self.midi_out_ports[tuning_index].send_message(pitch_bend_message)

            if self.print_msgs: 
                print(f"{chord=}")
                print(f"{key=}")
                print(f"{candidate_keys}")
            
            self.midi_out_ports[instance_index].send_message([status, note, velocity])
            self.udp_sender.send(self.message_heap)

        elif status in range(128, 144):
            instance_index = self.in_use_indices[note]
            self.midi_out_ports[instance_index].send_message([status, note, velocity])
            if not self.sustain:
                # Delete only the first occurance of note in self.message_heap
                for index, sublist in enumerate(self.message_heap):
                    if sublist[0] == note:
                        del self.message_heap[index]
                        break
                heapq.heapify(self.message_heap)
                if instance_index not in self.instance_index:
                    heapq.heappush(self.instance_index, instance_index)
                del self.in_use_indices[note]

            else:
                heapq.heappush(self.sustained_notes, [note, instance_index, status, velocity])
            
            self.udp_sender.send(self.message_heap)
            chord = self.music_theory.determine_chord(self.message_heap)

        elif status in range(176, 192) and note == 64:
            if velocity == 127:
                self.sustain = True
                for instance_index in range(12):
                    self.midi_out_ports[instance_index].send_message([status, 64, 127])
            elif velocity == 0:
                self.sustain = False
                for instance_index in range(12):
                    self.midi_out_ports[instance_index].send_message([status, 64, 0])
                
                sus_notes_copy = deepcopy(self.sustained_notes)
                multiple_played_notes = []
                for sus_note in sus_notes_copy:
                    instance_index = self.in_use_indices[sus_note[0]]
                    self.delete_suspended_note(sus_note=sus_note)
                    if instance_index or instance_index == 0:
                        if sus_note[1] not in [sublist[1] for sublist in self.message_heap]:
                            heapq.heappush(self.instance_index, instance_index)
                            del self.in_use_indices[sus_note[0]]
                        else:
                            multiple_played_notes.append(sus_note)

                if not self.message_heap:
                    self.in_use_indices = {}
                else:
                    counter = 0
                    length = len([note[0] for note in self.in_use_indices.items()])
                    while sorted([note[0] for note in self.in_use_indices.items()]) != sorted([note[0] for note in self.message_heap]):
                        if counter > 1000:
                            logging.warning("Loop is misbehaving or you just held the sustain pedal for a really long time!")
                            break
                        for duplicate_note in [note[0] for note in self.in_use_indices.items()]:
                            counter += 1
                            if duplicate_note not in [note[0] for note in self.message_heap]:
                                del self.in_use_indices[duplicate_note]
                                break
                
                heapq.heapify(self.message_heap)
                sus_notes_copy = []
                self.sustained_notes = []
        
        elif status in range(176, 192) and note == 1:
            # if velocity == 127:
            for midi_out in self.midi_out_ports:
                # No tuning message
                midi_out.send_message([status + 48, 0, 64])

        elif status == 169:
            self.turn_off_all_notes()
            
    def set_tuning_mode(self, tuning_mode: str = None) -> None:
        """Change the tuning mode while running the MidiManager. Tuning options are static for static Just Intonation,
        dynamic for dynamic Just Intonation, or None for Equal temperment (default).

        Args:
            tuning_mode (str, optional): static, dynamic, or None. Defaults to None.
        """
        previous_tuning_mode = self.just_intonation.tuning_mode.copy()
        if tuning_mode:
            if tuning_mode in ["static", "dynamic"]:
                self.just_intonation.tuning_mode = tuning_mode
                self.logger.info(f"Tuning mode state change: {previous_tuning_mode}->{tuning_mode}")
            else:
                self.logger.info("Tuning mode state change unsuccessful."
                                 "Acceptable state change keys are static, dynamic, or None")
        else:
            self.just_intonation.tuning_mode = tuning_mode
            self.logger.info(f"Tuning mode state change: {previous_tuning_mode}->Equal Temperment")
    
    def delete_suspended_note(self, sus_note: list):
        for index, sublist in enumerate(self.message_heap):
            if sublist[0] == sus_note[0]:
                del self.message_heap[index]
                return
    
    def transpose_by(self, amount: int) -> None:
        """Transpose by a given integer number of notes away from the root up or down

        Args:
            amount (int): a transposition amount in the range (-12, 12) inclusive
        """
        if -12 <= amount <= 12:
            self.transpose = amount

    def turn_off_all_notes(self):
        """ Utility function used in troubleshooting/debugging. It is useful when handling hanging MIDI messages, 
        and it's used to silence all output by sending ALL_NOTES_OFF message to all instances
        """
        all_notes_off_message = [176, 123, 0]
        retune_to_center_frequency = [224, 0, 64]
        for instance_index in range(12):
            self.midi_out_ports[instance_index].send_message(all_notes_off_message)
            self.midi_out_ports[instance_index].send_message(retune_to_center_frequency)

    def set_midi_callback(self):
        """This function filters the output to the console based on the filter function"""
        self.midi_in.set_callback(self.filter)

    def start_listening(self):
        """ This is the main control loop where execution takes place.
        The listener waits for Midi messages and acts according to the filter function
        """
        try:
            print("Listening for MIDI messages. Press Ctrl+C to exit.")
            while True:
                message = self.midi_in.get_message()
                time.sleep(0.001)
        except KeyboardInterrupt:
            print("Exiting...")
            self.turn_off_all_notes()
        finally:
            self.close_ports()
            
if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Initialize the MidiController with specific settings.")
    
    # Define the flags for print and tuning with a file path for tuning
    parser.add_argument('-p', '--print', action='store_true', help="Enable printing to the console.")
    parser.add_argument('-t', '--tuning', type=str, help="Path to a JSON pitch config.")
    
    # Define mutually exclusive group for static and dynamic
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--static', action='store_true', help="Enable static tuning.")
    group.add_argument('-d', '--dynamic', action='store_true', help="Enable dynamic tuning.")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Ensure -s or -d can only be used if -t is provided
    if (args.static or args.dynamic) and not args.tuning:
        print("Error: The -s or -d flag requires the -t <config> flag to be provided.")
        exit(1)

    # Load tuning from JSON file if -t flag is used
    pitch_config = None
    if args.tuning:
        try:
            with open(args.tuning, 'r') as f:
                pitch_config = json.load(f)
        except FileNotFoundError:
            print(f"Error: File {args.tuning} not found.")
            exit(1)
        except json.JSONDecodeError:
            print(f"Error: File {args.tuning} is not a valid JSON file.")
            exit(1)
            
    if pitch_config:
        max_key_length = max(len(key) for key in pitch_config.keys()) + 1
        print(f"{'Interval':<{max_key_length}}  Pitch Setting")
        print('-' * (max_key_length + 16))  # Print a separator line
        for key, value in pitch_config.items():
            print(f"{key+":":<{max_key_length}}  {value}")
            
    # Determine if static or dynamic tuning is enabled
    tuning_mode = 'static' if args.static else 'dynamic' if args.dynamic else None
    print(f"Tuning mode: {tuning_mode}")
    print(f"args.print {args.print}")
    print_msgs = args.print
    
    # Initialize MidiController with parsed flags and static_tuning
    midi_controller = MidiController(
        print_msgs=print_msgs,
        tuning=pitch_config,
        tuning_mode=tuning_mode
    )
