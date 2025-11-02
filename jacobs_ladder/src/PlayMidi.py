import time
import mido
import rtmidi
import tkinter as tk
from tkinter import filedialog

def play_midi_file(filename: str, port_name: str = "jacob"):
    """
    Play a MIDI file through a virtual or hardware MIDI port using rtmidi.

    Args:
        filename (str): Path to the .mid file
        port_name (str): Name of the MIDI output port (default: 'jacob')
    """
    midiout = rtmidi.MidiOut()

    # Try to open an existing port called "jacob"
    available_ports = midiout.get_ports()
    port_index = None
    for i, name in enumerate(available_ports):
        if port_name.lower() == name.split(" ")[0]:
            port_index = i
            break

    if port_index is not None:
        midiout.open_port(port_index)
        print(f"Connected to existing port: {available_ports[port_index]}")
    else:
        print(f"No existing port: ")

    mid = mido.MidiFile(filename)
    print(f"Playing MIDI file: {filename}")

    start_time = time.time()
    for msg in mid.play():
        if not msg.is_meta:
            midiout.send_message(msg.bytes())

    elapsed = time.time() - start_time
    print(f"Playback finished in {elapsed:.2f} seconds")

    del midiout


if __name__ == "__main__":
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Ask the user to select a MIDI file
    file_path = filedialog.askopenfilename(
        title="Select a MIDI file",
        filetypes=[("MIDI files", "*.mid *.midi")],
    )

    print(f"Opening file: {file_path}")

    if file_path:
        play_midi_file(file_path)
    else:
        print("No file selected. Exiting.")
