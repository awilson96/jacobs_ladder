import heapq
import time

import rtmidi


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
        if status == 148:
            heapq.heappush(self.note_heap, [note, velocity, dt])
            self.just_intonation()
            print(f"{self.note_heap}")

        # Note Off event
        elif status == 132:
            # Remove the note from the heap if it is present
            self.note_heap = [
                note_info for note_info in self.note_heap if note_info[0] != note
            ]

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
            note1, _, _ = self.note_heap[0]
            note2, _, _ = self.note_heap[1]
            note3, _, _ = self.note_heap[2]

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
