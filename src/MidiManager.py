import heapq
import logging
import time
import warnings

import rtmidi

from .JustIntonation import JustIntonation
from .MusicTheory import MusicTheory

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "October 12th 2023 (creation)"

logging.basicConfig(
    filename="./logs/MidiManager.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

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

    def __init__(self, input_port="jacobs_ladder", output_ports=list(map(str, range(12)))):
        """
        Class Constructor creates a MidiController object.
        MidiController handles MIDI port management, output port instance management, and sustain pedal management.

        Args:
            input_port (str, optional): input port name. Defaults to "jacobs_ladder 2".
            output_ports (list, optional): output port name. Defaults to a list on integers from 0-15.
        """
        # MIDI port management
        self.midi_in = rtmidi.MidiIn()
        self.midi_out_ports = [rtmidi.MidiOut() for _ in range(12)]
        self.input_port = input_port
        self.output_ports = output_ports

        # Create midi in and midi out virtual port objects
        self.initialize_ports()

        # Output port instance management
        self.instance_index = list(range(12))
        self.message_heap = [] 
        self.in_use_indices = {}

        # Sustain pedal management
        self.sustain = False
        self.sustained_notes = []

        # Tuning management
        self.tuning = False
        self.just_intonation = JustIntonation()
        
        self.set_midi_callback()
        self.start_listening()

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
            # print(f"available_input_ports \n{available_input_ports}")
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
            instance_index = self.determine_octave(note)
            if instance_index is None:
                if note not in [msg_note[0] for msg_note in self.message_heap]:
                    instance_index = heapq.heappop(self.instance_index)
                else:
                    instance_index = self.in_use_indices[note]
                    if not instance_index:
                        logging.warning(f"no instances are left! {self.instance_index}")
                        
            self.in_use_indices[note] = instance_index
            self.midi_out_ports[instance_index].send_message([status, note, velocity])
            heapq.heappush(self.message_heap, [note, instance_index, status, velocity])
            
            chord = self.music_theory.determine_chord(self.message_heap)
            key = self.music_theory.determine_key(self.message_heap)
            if self.tuning:
                pitch_adjust_message = self.just_intonation.pitch_adjust_chord(message_heap=self.message_heap, 
                                                                               current_msg=[note, instance_index, status, velocity], 
                                                                               dt=dt, 
                                                                               chord=chord)
 
            if pitch_adjust_message:
                pitch_bend_message, instance_idx = pitch_adjust_message
                self.midi_out_ports[instance_idx].send_message(pitch_bend_message)
                    
            self.music_theory.share_messages(message_heap=self.message_heap)

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
                if instance_index not in [sublist[1] for sublist in self.message_heap]:
                    if instance_index not in self.instance_index:
                        heapq.heappush(self.instance_index, instance_index)
                    del self.in_use_indices[note]

            else:
                heapq.heappush(self.sustained_notes, [note, instance_index, status, velocity])
            
            chord = self.music_theory.determine_chord(self.message_heap)
            self.music_theory.share_messages(message_heap=self.message_heap)

        elif status in range(176, 192) and note == 64:
            if velocity == 127:
                self.sustain = True
                for instance_index in range(12):
                    self.midi_out_ports[instance_index].send_message([status, 64, 127])
            elif velocity == 0:
                self.sustain = False
                for instance_index in range(12):
                    self.midi_out_ports[instance_index].send_message([status, 64, 0])
                for sus_note in self.sustained_notes:
                    instance_index = self.in_use_indices[sus_note[0]]
                    for index, sublist in enumerate(self.message_heap):
                        if sublist[0] == sus_note[0]:
                            del self.message_heap[index]
                            break
                    if sus_note[0] not in [sublist[0] for sublist in self.message_heap]:
                        if sus_note[1] not in [sublist[1] for sublist in self.message_heap]:
                            heapq.heappush(self.instance_index, instance_index)
                        del self.in_use_indices[sus_note[0]]

                heapq.heapify(self.message_heap)
                self.sustained_notes = []
        
        elif status in range(176, 192) and note == 1:
            # if velocity == 127:
            for midi_out in self.midi_out_ports:
                # No tuning message
                midi_out.send_message([status + 48, 0, 64])

        elif status == 169:
            self.turn_off_all_notes()

    def determine_octave(self, note: int):
        """
        Determine if the current note is an octave of any of the currently active notes.

        Args:
            note (int): an active note to check against self.message_heap

        Returns:
            int: returns the instance index if the current note is an octave multiple of an active note and None otherwise
        """
        notes= list(map(lambda sublist: sublist[0], self.message_heap))
        instance= list(map(lambda sublist: sublist[1], self.message_heap))

        octaves= [octave for octave in range(note + 12, 109, 12)]
        octaves += [octave for octave in range(note - 12, 20, -12)]

        for active_note in notes:
            if active_note in octaves:
                return instance[notes.index(active_note)]
        return None

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
            while self.terminate.buf[0] == 0:
                message = self.midi_in.get_message()
                time.sleep(0.001)
            self.turn_off_all_notes()
        except KeyboardInterrupt:
            print("Exiting...")
            self.turn_off_all_notes()
        finally:
            self.close_ports()
            
if __name__ == "__main__":
    midi_controller = MidiController()
