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
        self.midi_out = rtmidi.MidiOut()
        self.output_ports = output_port
        self.initialize_port()

    def initialize_port(self):
        # Initialize MIDI output port
        try:
            available_output_ports = [
                port.split(" ", 1)[0] for port in self.midi_out.get_ports()
            ]
            index = available_output_ports.index(self.output_ports)
            print(f'Opening port "{self.output_ports}" on index {index}')
            self.midi_out.open_port(index)

        except (ValueError, rtmidi._rtmidi.SystemError):
            raise RuntimeError(f"Failed to open output port '{index}'")


def main():
    midi_injector = MidiInjector()


if __name__ == "__main__":
    main()
