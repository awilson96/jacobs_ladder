import logging

from ..utilities.Enums import Pitch

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "November 11th 2023 (creation)"

logging.basicConfig(
    filename="../logs/MidiManager.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class JustIntonation:
    def __init__(self):
        self.detuned_instances = []
        self.center_frequency = 8192  # No tuning

    def get_pitch_bend_message(self, message_heap_elem: list, pitch_bend_amount: int):
        """
        Gets the formed MIDI pitch bend message to be sent by the MidiManager

        Args:
            message_heap_elem (list): a message_heap list of the form [note, instance_index, status, velocity]
            pitch_bend_amount (int): number from 0-16383, 8192 is no tuning, 0 is max tune down, 16383 is max tune up
        """

        # Ensure pitch bend amount is within the valid range
        pitch_bend_amount = max(0, min(16383, pitch_bend_amount))

        # Calculate the LSB (Least Significant Byte) and MSB (Most Significant Byte) of the pitch bend value
        lsb = pitch_bend_amount & 0x7F
        msb = (pitch_bend_amount >> 7) & 0x7F

        # Status byte for pitch bend message NOTE_ON status + offset to convert to pitch bend message
        status_byte = message_heap_elem[2] + 80

        # Log the pitch bend message
        pitch_bend_message = [status_byte, lsb, msb]
        logging.debug(f"Pitch Bend Message: {pitch_bend_message}")

        return pitch_bend_message

    def pitch_adjust_chord(self, message_heap: list[list], chord=None):
        """Ajust the pitch of individual notes within a given chord
        If the chord is unknown then it will be tuned using intervals instead

        Args:
            message_heap (list[list]): an unsorted list of notes with their metadata
            chord (string, optional): a unique string representation of the chord being played. Defaults to None.

        Returns:
            list[tuple(pitch_bend_message, instance_index)]: a list of actions in the form of pitch bend messages to be sent by certain instance indices.
        """

        sorted_message_heap = sorted(message_heap, key=lambda x: x[0])
        notes = [note[0] for note in sorted_message_heap]
        instance_indices = [indices[1] for indices in sorted_message_heap]

        if chord is not None:
            if "Major Triad" in chord:
                action1 = (
                    self.get_pitch_bend_message(sorted_message_heap[1], Pitch.major_third),
                    instance_indices[1],
                )
                action2 = (
                    self.get_pitch_bend_message(sorted_message_heap[2], Pitch.perfect_fifth),
                    instance_indices[2],
                )
                # TODO: keep state of detuned instances to be used by the recenter frequency function
                # self.detuned_instances.append(instance_indices[1])
                # self.detuned_instances.append(instance_indices[2])
                # self.detuned_instances = list(set(self.detuned_instances))

                return [action1, action2]
        else:
            pass

    def recenter_frequency(self, message_heap: list[list], instance_index: int):
        """Used to recenter the base frequencies of instances which are no longer in use

        Args:
            message_heap (list[list]): a list of notes with their metadata [note, instance_index, status, velocity]
            instance_index (int): the instance index of the note which has received the note off message
        """
        pass