from jacobs_ladder import virtual_midi
import time
import subprocess

# Create a list of port configurations (pairs of <string, int>)
port_configs = [("jacobs_ladder", 12)]

# Instantiate the VirtualMIDIPortManager
manager = virtual_midi.VirtualMIDIPortManager(port_configs)

# Access the list of port names
port_names = manager.getPortNames()
print(port_names)

# Path to your VBScript
script_path = "C:\\Program Files (x86)\\MIDIOX\\WSH\\PortMapping.vbs"
profile_path = "C:\\Users\\awils\\OneDrive\\Documents\\Repos\\jacobs_ladder\\jacobs_ladder\\src\\ini\\jacobs_ladder.ini"

# Start the VBScript using subprocess
process = subprocess.Popen(
    ['cscript', script_path, profile_path], 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE,
    stdin=subprocess.PIPE,  # We need to send input to the script later
    text=True
)

# Simulate setting up things in Python (you can add your setup code here)
time.sleep(10)  # Simulating some setup work

# Now, to stop the script, we send the "Enter" key as input
process.stdin.write("\n")
process.stdin.flush()

# Optionally, wait for the process to finish
process.wait()

print("MIDI-OX profile script terminated gracefully.")

# Clean up after usage
manager.cleanup()
