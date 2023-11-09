import heapq
import logging
import time

import rtmidi

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "November 8th 2023 (creation)"

logging.basicConfig(
    filename="MidiManager.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class MidiInjector:
    """
    This is a Midi Injector which sends in Midi Data to a specified port for the purpose of testing MidiManager
    """

    def __init__(self, output_port="jacobs_ladder"):
        """_summary_

        Args:
            output_port (str, optional): Name of the output port you want to send Midi data on. Defaults to "jacobs_ladder".
        """
        self.midi_out = rtmidi.MidiOut()
        self.output_ports = output_port
        self.initialize_port()

    def initialize_port(self):
        """Initialize the port specified in __init__ by opening that port for Midi out operations

        Raises:
            RuntimeError: If the port cannot be found, this funtion raises an error
        """
        try:
            available_output_ports = [
                port.split(" ", 1)[0] for port in self.midi_out.get_ports()
            ]
            index = available_output_ports.index(self.output_ports)
            print(f'Opening port "{self.output_ports}" on index {index}')
            self.midi_out.open_port(index)

        except (ValueError, rtmidi._rtmidi.SystemError):
            raise RuntimeError(f"Failed to open output port '{index}'")

    def send_note_on(self, note, velocity):
        """Send a note-on message

        Args:
            note (int): The note number corresponding the key you want to send a note on message for
            velocity (int): The velocity of the note (0-127 inclusive)
        """
        note_on = [144, note, velocity]
        self.midi_out.send_message(note_on)

    def send_note_off(self, note):
        """Send a note-off message

        Args:
            note (int): The note number corresponding to the key you want to send a note off message for
        """
        note_off = [128, note, 0]
        self.midi_out.send_message(note_off)

    def send_sustain_pedal_high(self):
        """Send a sustain pedal message (sustain pedal is held down)"""
        sustain_pedal_high = [176, 64, 127]
        self.midi_out.send_message(sustain_pedal_high)

    def send_sustain_pedal_high(self):
        """Send a sustain pedal message (sustain pedal is released)"""
        sustain_pedal_low = [176, 64, 0]
        self.midi_out.send_message(sustain_pedal_low)


def main():
    midi_injector = MidiInjector()


if __name__ == "__main__":
    main()
