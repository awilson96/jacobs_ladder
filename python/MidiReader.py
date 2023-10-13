import rtmidi

class MidiController:
    def __init__(self, port_name="jacobs_ladder 2"):
        self.midi_in = rtmidi.MidiIn()
        # self.available_ports = self.midi_in.get_ports()
        print(self.available_ports)
        print(self.available_ports)
        self.port_name = port_name

    def open_port(self):
        if self.port_name in self.available_ports:
            port_number = self.available_ports.index(self.port_name)
            self.midi_in.open_port(port_number)
            print(f"Opened MIDI input port: {self.port_name}")
        else:
            print(f"MIDI input port '{self.port_name}' not found.")
            exit()

    def on_midi_message(self, message, time_stamp):
        print(message)

    def set_midi_callback(self):
        self.midi_in.set_callback(self.on_midi_message)

    def start_listening(self):
        try:
            self.set_midi_callback()
            print("Listening for MIDI messages. Press Ctrl+C to exit.")
            while True:
                pass
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            self.close_port()

    def close_port(self):
        self.midi_in.close_port()

def main():
    midi_controller = MidiController()
    midi_controller.open_port()
    midi_controller.start_listening()

if __name__ == "__main__":
    main()
