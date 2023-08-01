import mido
# import pygame
import numpy
import rtmidi
import scipy
import sounddevice
import time


class MidiReader:
    def __init__(self, input_device_name):
        """
        Examine incoming messages from the Midi keyboard
        :param input_device_name: name of user's Midi keyboard, (use list_available_in_ports() to see options)
        """
        self.input_device_name = input_device_name
        self.available_ports = self.list_available_in_ports()
        self.midi_in = None

    def connect_input_device(self):
        """
        Connect input device to rtmidi api
        :return: None
        """
        self.midi_in = rtmidi.MidiIn()

        for device in enumerate(self.available_ports):
            if self.input_device_name == device[1]:
                print(f"Opening \"{self.input_device_name}\" on port {device[0]}")
                self.midi_in.open_port(device[0])

    def disconnect_input_device(self):
        """
        Disconnect input device from rtmidi api
        :return: None
        """

        for device in enumerate(self.available_ports):
            if self.input_device_name == device[1]:
                print(f"Closing \"{self.input_device_name}\" on port {device[0]}")
                self.midi_in.close_port()

    def event_listener(self):
        """
        Listen for Midi messages sent from the input device to the MidiReader
        :return:
        """
        kill_key = 160
        note_on = 144
        note_off = 128

        while True:
            message = self.midi_in.get_message()
            if message:
                payload, dt = message
                print(f"{payload}")

                # This is the kill key which ends this function (corresponds to pad1 on my keyboard)
                if payload[0] == kill_key:
                    break

    @staticmethod
    def list_available_in_ports():
        """
        List all Midi capable devices
        :return: list of devices or None if there are no Midi capable devices
        """
        midi_in = rtmidi.MidiIn()
        available_ports = midi_in.get_ports()

        if available_ports:
            print(f"Listing available ports\n\t {available_ports}\n")
            return available_ports
        else:
            print("No devices are connected.")
            return None


def main():
    reader = MidiReader("Arturia KeyLab Essential 88 0")
    reader.connect_input_device()
    reader.event_listener()
    reader.disconnect_input_device()


if __name__ == "__main__":
    main()
