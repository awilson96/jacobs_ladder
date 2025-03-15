from jacobs_ladder import virtual_midi
import time
import subprocess
import os

# Create a list of port configurations (pairs of <string, int>)
port_configs = [("jacobs_ladder", 12)]

# Instantiate the VirtualMIDIPortManager
manager = virtual_midi.VirtualMIDIPortManager(port_configs, 1, True)

# Access the list of port names
port_names = manager.getPortNames()
print(port_names)

# Path to your VBScript
script_path = "C:\\Program Files (x86)\\MIDIOX\\WSH\\PortMapping.vbs"

if not os.path.isfile(script_path):
    manager.cleanup()
    raise FileNotFoundError(f"Could not find the VBScript at {script_path}")

jacobs_ladder_path1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "\\ini\\jacobs_ladder1.ini")

# Start the VBScript using subprocess
process1 = subprocess.Popen(
    ['cscript', script_path, jacobs_ladder_path1], 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE,
    stdin=subprocess.PIPE,  # We need to send input to the script later
    text=True
)

input("Press Enter to terminate...")

# Clean up after usage
manager.cleanup()

# Now, to stop the script, we send the "Enter" key as input
process1.stdin.write("\n")
process1.stdin.flush()
process1.wait()

print("MIDI-OX profile script terminated gracefully.")

