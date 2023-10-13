import heapq
import time

import rtmidi

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "October 12th 2023 (creation)"

class MidiController:
    """
    This is a Midi Keyboard interface which allows for the manipulation of real time Midi data 
    before sending that data back out through a virtual port to another program such as a software instrument
    """

    def __init__(self, input_port="jacobs_ladder 2", output_port="analog_lab 4"):
        """Initializer gives the MidiReader all of the port information needed to integrate with the Midi keyboard and software instrument

        Args:
            input_port (str, optional): The Midi input port used for connecting the keyboard to the script. Defaults to "jacobs_ladder 2".
            output_port (str, optional): The Midi ouput port used for sending manipulated data to the software instrument. Defaults to "analog_lab 4".
        """
        self.midi_in = rtmidi.MidiIn()
        self.midi_out = rtmidi.MidiOut()
        self.available_input_ports = self.midi_in.get_ports()
        self.available_output_ports = self.midi_out.get_ports()

        print(f"Available input ports {self.available_input_ports}")
        print(f"Available output ports {self.available_output_ports}")
        self.input_port = input_port
        self.output_port = output_port

        # Heap to store active notes (message format: ([status, note, velocity], timestamp))
        self.note_heap = []
        self.available_channels_heap = [[144, 128], [145, 129], [146, 130], [147, 131], [148, 132], [149, 133], [150, 134], [151, 135], 
                                        [152, 136], [153, 137], [154, 138], [155, 139], [156, 140], [157, 141], [158, 142], [159, 143]]
        heapq.heapify(self.available_channels_heap)
        self.note_off = {}
        
        

    def open_ports(self):
        """This function used the ports extracted from the initializer to open Midi input and output ports
        """
        if self.input_port in self.available_input_ports:
            port_number = self.available_input_ports.index(self.input_port)
            self.midi_in.open_port(port_number)
            print(f"Opened MIDI input port: {self.input_port}")
        else:
            print(f"MIDI input port '{self.input_port}' not found.")
            exit()

        if self.output_port in self.available_output_ports:
            port_number = self.available_output_ports.index(self.output_port)
            self.midi_out.open_port(port_number)
            print(f"Opened MIDI output port: {self.output_port}")
        else:
            print(f"MIDI output port '{self.output_port}' not found.")
            exit()

    def on_midi_message(self, message, timestamp):
        """Function for maintaining a notes queue called note_heap based on note on and note off events. Used in forming callback (Midi filter)

        Args:
            message (tuple([status, note, velocity], dt)): message is the standard Midi message sent from the keyboard to the program
            timestamp (None): placeholder, for now having this in the callback makes the function work but timestamp has no other function
        """
        midi_event, dt = message
        status, note, velocity = midi_event
        # Note On event
        if status in range(144, 160):
            new_status = self.determineOctave(note)
            if new_status is not None:
                heapq.heappush(self.note_heap, [new_status, note, velocity, dt])
                self.note_off[note] = new_status - 16
            else:
                new_status, status_off = self.available_channels_heap.pop()
                heapq.heappush(self.note_heap, [new_status, note, velocity, dt])
                self.note_off[note] = status_off
                
            self.midi_out.send_message([new_status, note, velocity])
            
            print(f"{self.note_heap}")

        # Note Off event
        elif status in range (128, 144):
            new_status = self.note_off[note]
            if [new_status + 16, new_status] not in self.available_channels_heap:
                heapq.heappush(self.available_channels_heap, [new_status + 16, new_status])
            # Remove the note from the heap if it is present
            self.midi_out.send_message([new_status, note, velocity])
            self.note_heap = [
                note_info for note_info in self.note_heap if note_info[1] != note
            ]
            
    def determineOctave(self, note):
        """Determines if the current note is an octave of any currently active note. 
        If so then it is assigned the channel corresponding to the note in note_heap which is its octave.

        Args:
            note (int): the active Midi note that is being considered 

        Returns:
            int: status, the status which encapsulates the Midi channel information. Notes which are octaves of eachother can be on the same channel
        """
        get_status = lambda sublist: sublist[0]
        get_notes = lambda sublist: sublist[1]
        status = list(map(get_status, self.note_heap))
        notes = list(map(get_notes, self.note_heap))
        for n in notes:
            if abs(note-n) == 12:
                return status[notes.index(n)]
        return None

    def set_midi_callback(self):
        """This function filters the output to the console based on the on_midi_message function
        """
        self.midi_in.set_callback(self.on_midi_message)

    def start_listening(self):
        """This is the main loop where execution takes place. The listener waits for Midi messages and acts accordingly based on supporting functions
        """
        try:
            print("Listening for MIDI messages. Press Ctrl+C to exit.")
            while True:
                message = self.midi_in.get_message()
                if message:
                    _, dt = message
                    print("Received MIDI message:", message, "Timestamp:", dt)
                # Add a small delay to control the polling rate
                time.sleep(0.001)  
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            self.close_port()

    def close_port(self):
        """Close the ports at the end of execution
        """
        self.midi_in.close_port()
        self.midi_out.close_port()

    def just_intonation(self):
        """Retune the keyboard to match just intonation
        """
        if len(self.note_heap) == 3:
            status1, note1, _, _ = self.note_heap[0]
            status2, note2, _, _ = self.note_heap[1]
            status2, note3, _, _ = self.note_heap[2]

            # Check for major triad
            if abs(note1 - note2) in [4, 7] and abs(note1 - note3) in [4, 7]:
                print(note1, note2, note3)


def main():
    """Instantiates the class, opens ports, sets the callback for filtered Midi output, and listens for events
    """
    midi_controller = MidiController()
    midi_controller.open_ports()
    midi_controller.set_midi_callback()
    midi_controller.start_listening()


if __name__ == "__main__":
    main()
