import rtmidi
import time
import numpy as np
import heapq

class MidiController:
    def __init__(self, port_name="jacobs_ladder 2"):
        self.midi_in = rtmidi.MidiIn()
        self.available_ports = self.midi_in.get_ports()
        print(self.available_ports)
        self.port_name = port_name
        # Set NumPy print options and display values to 3 decimal places
        np.set_printoptions(suppress=True, precision=3)
        self.note_heap = []  # Heap to store active notes (message format: ([status, note, velocity], timestamp))

    def open_port(self):
        if self.port_name in self.available_ports:
            port_number = self.available_ports.index(self.port_name)
            self.midi_in.open_port(port_number)
            print(f"Opened MIDI input port: {self.port_name}")
        else:
            print(f"MIDI input port '{self.port_name}' not found.")
            exit()

    def on_midi_message(self, message, timestamp):
        print(message)
        midi_event, _ = message
        status, note, velocity = midi_event
        if status == 148:  # Note On event
            heapq.heappush(self.note_heap, [note, velocity, timestamp])
            print(f"{self.note_heap}")
        elif status == 132:  # Note Off event
            # Remove the note from the heap if it is present
            self.note_heap = [note_info for note_info in self.note_heap if note_info[0] != note]
            print(f"{self.note_heap}")

    def set_midi_callback(self):
        self.midi_in.set_callback(self.on_midi_message)

    def start_listening(self):
        try:
            print("Listening for MIDI messages. Press Ctrl+C to exit.")
            while True:
                message = self.midi_in.get_message()
                if message:
                    _, dt = message
                    print("Received MIDI message:", message, "Timestamp:", dt)
                time.sleep(0.001)  # Add a small delay to control the polling rate
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            self.close_port()

    def close_port(self):
        self.midi_in.close_port()

def main():
    midi_controller = MidiController()
    midi_controller.open_port()
    midi_controller.set_midi_callback()
    midi_controller.start_listening()

if __name__ == "__main__":
    main()
