import logging

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "November 11th 2023 (creation)"

logging.basicConfig(
    filename="MidiManager.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class JustIntonation:
    def __init__(self):
        self.detuned_instances = []

    def send_pitch_bend(self, midi_out: object, message: list, pitch_bend_amount: int):
        """
        Send MIDI pitch bend message to a MIDI output port

        Args:
            midi_out (object): rtmidi.MidiOut() object for sending pitch bend message
            message (list): a message_heap list of the form [note, instance_index, status, velocity]
            pitch_bend_amount (int): number from 0-16383, 8192 is no tuning, 0 is max tune down, 16383 is max tune up
        """

        # Ensure pitch bend amount is within the valid range
        pitch_bend_amount = max(0, min(16383, pitch_bend_amount))

        # Calculate the LSB (Least Significant Byte) and MSB (Most Significant Byte) of the pitch bend value
        lsb = pitch_bend_amount & 0x7F
        msb = (pitch_bend_amount >> 7) & 0x7F

        # Status byte for pitch bend message NOTE_ON status + offset to convert to pitch bend message
        status_byte = message[2] + 80

        # Send the pitch bend message
        logging.debug(f"Pitch Bend Message: {[status_byte, lsb, msb]}")
        midi_out.send_message([status_byte, lsb, msb])
