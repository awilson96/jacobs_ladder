import heapq
import logging
import time

import rtmidi

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "October 12th 2023 (creation)"

logging.basicConfig(
    filename="MidiManager.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class MidiController:
    """
    This is a Midi Keyboard interface which allows for the manipulation of real time Midi data
    before sending that data back out through a virtual port to another program such as a software instrument
    """

    def __init__(
        self, input_port="jacobs_ladder 2", output_ports=list(map(str, range(16)))
    ):
        self.midi_in = rtmidi.MidiIn()
        self.midi_out_ports = [rtmidi.MidiOut() for _ in range(16)]
        self.input_port = input_port
        self.output_ports = output_ports
        self.initialize_ports()
        self.instance_index = list(range(16))
        heapq.heapify(self.instance_index)
        self.message_heap = []
        self.in_use_indices = {}
        self.sustain = False
        self.sustained_notes = []

    def initialize_ports(self):
        # Initialize MIDI input port
        try:
            available_input_ports = self.midi_in.get_ports()
            input_port_index = None
            for port in available_input_ports:
                if port.startswith(self.input_port):
                    input_port_index = available_input_ports.index(port)
                    break
            if input_port_index is not None:
                self.midi_in.open_port(input_port_index)
            else:
                raise ValueError(f"Input port '{self.input_port}' not found.")
        except (ValueError, rtmidi._rtmidi.SystemError):
            raise RuntimeError(f"Failed to open input port '{self.input_port}'")

        # Initialize MIDI output ports with specified names
        try:
            available_output_ports = [
                port.split(" ", 1)[0] for port in self.midi_out_ports[0].get_ports()
            ]
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
        payload, dt = message
        status, note, velocity = payload

        if status in range(144, 160):
            if note not in [msg_note[0] for msg_note in self.message_heap]:
                instance_index = heapq.heappop(self.instance_index)
            else:
                instance_index = self.in_use_indices[note]
                if not instance_index:
                    print("not instance index")
            self.in_use_indices[note] = instance_index
            self.midi_out_ports[instance_index].send_message([status, note, velocity])
            heapq.heappush(self.message_heap, [note, instance_index, status, velocity])

            print(f"self.sustain {self.sustain}")
            print(f"self.sustained_notes {self.sustained_notes}")
            print(f"self.instance_index {self.instance_index}")
            print(f"self.message_heap {self.message_heap}")
            print(f"self.in_use_indices {self.in_use_indices}")
            print()
            
            logging.debug(f"self.sustain {self.sustain}")
            logging.debug(f"self.sustained_notes {self.sustained_notes}")
            logging.debug(f"self.instance_index {self.instance_index}")
            logging.debug(f"self.message_heap {self.message_heap}")
            logging.debug(f"self.in_use_indices {self.in_use_indices}\n")


        elif status in range(128, 144):
            instance_index = self.in_use_indices[note]
            self.midi_out_ports[instance_index].send_message([status, note, velocity])

            if not self.sustain:
                heapq.heappush(self.instance_index, instance_index)
                del self.in_use_indices[note]
                self.message_heap = [
                    sublist for sublist in self.message_heap if sublist[0] != note
                ]
                heapq.heapify(self.message_heap)
            else:
                if note not in [sus_note[0] for sus_note in self.sustained_notes]:
                    heapq.heappush(
                        self.sustained_notes, [note, instance_index, status, velocity]
                    )

        elif status in range(176, 192) and note == 64:
            if velocity == 127:
                self.sustain = True
                for instance_index in range(16):
                    self.midi_out_ports[instance_index].send_message([status, 64, 127])
            elif velocity == 0:
                self.sustain = False
                for instance_index in range(16):
                    self.midi_out_ports[instance_index].send_message([status, 64, 0])
                for sus_note in self.sustained_notes:
                    instance_index = self.in_use_indices[sus_note[0]]
                    heapq.heappush(self.instance_index, instance_index)
                    del self.in_use_indices[sus_note[0]]
                    self.message_heap = [
                        filtered_list
                        for filtered_list in self.message_heap
                        if filtered_list[0] != sus_note[0]
                    ]
                    heapq.heapify(self.message_heap)
                self.sustained_notes = []

        elif status == 169:
            self.turn_off_all_notes()
            
    def determine_octave(self, note: int):

        notes = list(map(lambda sublist: sublist[0], self.message_heap))
        instance = list(map(lambda sublist: sublist[1], self.message_heap))
    
        octaves = [octave for octave in range(note + 12, 109, 12)]
        octaves += [octave for octave in range(note - 12, 20, -12)]
    
        for active_note in notes:
            if active_note in octaves:
                return instance[notes.index(active_note)]
        return None

    def turn_off_all_notes(self):
        all_notes_off_message = [176, 123, 0]
        for instance_index in range(16):
            self.midi_out_ports[instance_index].send_message(all_notes_off_message)

    def set_midi_callback(self):
        """This function filters the output to the console based on the filter function"""
        self.midi_in.set_callback(self.filter)

    def start_listening(self):
        """This is the main loop where execution takes place. The listener waits for Midi messages and acts accordingly based on supporting functions"""
        try:
            print("Listening for MIDI messages. Press Ctrl+C to exit.")
            while True:
                # Get the current message contents, filtering and display are handled by the filter function
                message = self.midi_in.get_message()
                # Add a small delay to control the polling rate
                time.sleep(0.001)
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            self.close_port()

    def close_port(self):
        pass


def main():
    midi_controller = MidiController()
    midi_controller.set_midi_callback()
    midi_controller.start_listening()


if __name__ == "__main__":
    main()
