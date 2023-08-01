import mido
import pygame
import numpy
import rtmidi
import scipy
import sounddevice
import time


class MidiReader:
    def __init__(self, input_device_name):
        self.input_device_name = input_device_name

    # List available ports
    @staticmethod
    def list_available_ports():
        midi_in = rtmidi.MidiIn()
        available_ports = midi_in.get_ports()

        if available_ports:
            print(available_ports)
        else:
            print("No devices are connected.")


def main():
    MidiReader.list_available_ports()


if __name__ == "__main__":
    main()
