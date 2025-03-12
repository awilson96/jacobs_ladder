from jacobs_ladder import virtual_midi
import time
# Create a list of port configurations (pairs of <string, int>)
port_configs = [("PortPrefix", 3), ("AnotherPort", 2)]

# Instantiate the VirtualMIDIPortManager
manager = virtual_midi.VirtualMIDIPortManager(port_configs)

# Access the list of port names
port_names = manager.getPortNames()

print(port_names)

time.sleep(20)

# Clean up after usage
manager.cleanup()
