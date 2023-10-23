import heapq
import time

import rtmidi

__author__ = "Alex Wilson"
__copyright__ = "Copyright (c) 2023 Jacob's Ladder"
__date__ = "October 12th 2023 (creation)"


class MidiController:
    """
    This is a Midi Keyboard interface which allows for the manipulation of real time Midi data
    before sending that data back out through a virtual port to another program such as a software instrument
    """

    def __init__(self, input_port="jacobs_ladder 2", output_port="analog_lab 4"):
        """Initializer gives the MidiReader all of the port information needed to integrate with the Midi keyboard and software instrument

        Args:
            input_port (str, optional): The Midi input port used for connecting the keyboard to the script. Defaults to "jacobs_ladder 2".
            output_port (str, optional): The Midi ouput port used for sending manipulated data to the software instrument. Defaults to "analog_lab 4".
        """
        # All Midi In operations are done through self.midi_in
        self.midi_in = rtmidi.MidiIn()
        # All Midi Out operations are done through self.midi_in
        self.midi_out = rtmidi.MidiOut()
        # A list of all of the available input ports used for sending Midi data to the script
        self.available_input_ports = self.midi_in.get_ports()
        # A list of all of the available output ports used for sending Midi data from the script
        self.available_output_ports = self.midi_out.get_ports()

        # Uncomment to display the input and output port data to the user to aid in selection of port 
        # print(f"Available input ports {self.available_input_ports}")
        # print(f"Available output ports {self.available_output_ports}")
        
        # The input port chosen from the input port list
        self.input_port = input_port
        # The output port chosen from the output port list
        self.output_port = output_port

        # Heap to efficiently store active notes (message format: [status, note, velocity, timestamp])
        self.note_heap = []
        # Heap to store available channels, these channels are 'checked-out' when needed to be used by a note
        self.available_channels_heap = [144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159]
        # Sorts the heap into a min heap
        heapq.heapify(self.available_channels_heap)
        # {note: channel} used to map the note to its note on status messages. When it comes time to turn it off, we know which channel to send the note off message on.
        self.note_channel = {}
        self.int_note = {21: "A1", 22: "Bb1", 23: "B1", 24: "C1", 25: "Db1", 26: "D1", 27: "Eb1", 28: "E1", 29: "F1", 30: "Gb1", 31: "G1", 32: "Ab1", 
                         33: "A2", 34: "Bb2", 35: "B2", 36: "C2", 37: "Db2", 38: "D2", 39: "Eb2", 40: "E2", 41: "F2", 42: "Gb2", 43: "G2", 44: "Ab2",
                         45: "A3", 46: "Bb3", 47: "B3", 48: "C3", 49: "Db3", 50: "D3", 51: "Eb3", 52: "E3", 53: "F3", 54: "Gb3", 55: "G3", 56: "Ab3",
                         57: "A4", 58: "Bb4", 59: "B4", 60: "C4", 61: "Db4", 62: "D4", 63: "Eb4", 64: "E4", 65: "F4", 66: "Gb4", 67: "G4", 68: "Ab4",
                         69: "A5", 70: "Bb5", 71: "B5", 72: "C5", 73: "Db5", 74: "D5", 75: "Eb5", 76: "E5", 77: "F5", 78: "Gb5", 79: "G5", 80: "Ab5",
                         81: "A6", 82: "Bb6", 83: "B6", 84: "C6", 85: "Db6", 86: "D6", 87: "Eb6", 88: "E6", 89: "F6", 90: "Gb6", 91: "G6", 92: "Ab6", 
                         93: "A7", 94: "Bb7", 95: "B7", 96: "C7", 97: "Db7", 98: "D7", 99: "Eb7", 100: "E7", 101: "F7", 102: "Gb7", 103: "G7", 104: "Ab7",
                         105: "A8", 106: "Bb8", 107: "B8", 108: "C8"}
        
        # Used to track the status of the sustain pedal for sending out sustain control messages
        self.sustain = False

    def initialize_ports(self):
        """Uses the input and output ports from the initializer to open Midi input and output ports for reading and writing"""
        # Check that the input port provided by the user is indeed in the available_input_ports list
        if self.input_port in self.available_input_ports:
            # Find the index of the input port that was given by the user
            port_number = self.available_input_ports.index(self.input_port)
            # Use this index to open the port for reading in Midi data
            self.midi_in.open_port(port_number)
            # Display the opened port to the user to show that a successful connection was made
            print(f"Opened MIDI input port: {self.input_port}")
        # The input port provided by the user was not in the avilable_input_ports list
        else:
            # Display this error to the user and exit the program
            print(f"MIDI input port '{self.input_port}' not found.")
            exit()

        # Check that the input port provided by the user is indeed in the available_output_ports list
        if self.output_port in self.available_output_ports:
            # Find the index of the output port that was given by the user
            port_number = self.available_output_ports.index(self.output_port)
            # Use this index to open the port for sending out Midi data
            self.midi_out.open_port(port_number)
            # Display the opened port to the user to show that a successful connection was made
            print(f"Opened MIDI output port: {self.output_port}")
        # The output port provided by the user was not in the avilable_output_ports list
        else:
            # Display this error to the user and exit the program
            print(f"MIDI output port '{self.output_port}' not found.")
            exit()

    def filter(self, message: tuple, timestamp: float):
        """Function for maintaining a notes queue called note_heap based on note on and note off events. Used in forming callback (Midi filter)

        Args:
            message (tuple([status, note, velocity], dt)): message is the standard Midi message sent from the keyboard to the program
            timestamp (None): the callback expects this function signiture although timestamp is unused
        """
        # Parsing message to separate payload [status, note, velocity] from difference in time in between messages (dt)
        payload, dt = message
        # Further parsing the payload into status, note, and velocity
        status, note, velocity = payload
        
        # Process NOTE_ON events here
        if status in range(144, 160):
            # Call determine_octave to check if the current note is an octave of any active notes. These notes can share the same channel
            # Returns the status message of the note it is an octave of or None if no octave is not found
            unique_status = self.determine_octave(note)
            # If no octave is found between the current note and the active note list
            if unique_status is None:
                # Checkout an unused channel for that note. Note that the status message encapsulates the message type and channel information in the same number
                unique_status = self.available_channels_heap.pop()
            
            # Add the note to the note_heap used to track the state of all active notes
            heapq.heappush(self.note_heap, [note, unique_status, velocity, dt])
            # Update the note_off dictionary to assign a note off status message to the current note. 
            # Once the note_off signal is found the script can then use this dictionary to form the note off message and be sure to turn the note off on the right channel
            self.note_channel[note] = unique_status
            
            # Determine chord prints the chord in human readable format to the console
            self.determine_chord()
            
            # Send the Midi out message with a unique channel number for all non-octave notes and the same channel number for all octave notes. This was done to help reserve
            # more channels in case more than 16 notes need to be held at once, (i.e. the sutain pedal has been held down for a long time)
            self.midi_out.send_message([unique_status, note, velocity])
            # self.just_intonation()

            # Display the note heap to the user. Used in troubleshooting
            # print(f"{self.note_heap}")
            
        # Process NOTE_OFF events here
        elif status in range(128, 144):
            # Find the channel that the note was played on via status message
            unique_status = self.note_channel[note]
            # If the channel is not available, (it is not in available_channels_heap), then add it back so it can be used by another process.
            if unique_status not in self.available_channels_heap:
                heapq.heappush(
                    self.available_channels_heap, unique_status
                )
            # Send the Midi out message with the status message subtracted by 16 to account for the difference between NOTE_ON and NOTE_OFF messages (NOTE_OFF = NOTE_ON -16)
            self.midi_out.send_message([unique_status - 16, note, velocity])
            # Remove note from the active notes represented by note_heap since we have received the NOTE_OFF message
            self.note_heap = [
                active_note for active_note in self.note_heap if active_note[0] != note
            ]
            # Determine chord prints the chord in human readable format to the console
            self.determine_chord()
            # Clean up the note_channel dictionary to show that the note channel pair is no longer active
            del self.note_channel[note]
            
        # Pads (used for triggering CC: All Notes Off event on all channels). Useful when testing. FIXME: Remove this later when no longer needed
        elif status == 169:
            self.turn_off_all_notes()
            
        # Process CC: Pedal (Sustain) events here
        elif status in range(176, 192):
            # Inquire about the state of the sustain pedal and set self.sustain to either False or True based on whether we received a velocity of 127 (on) or 0 (off)
            self.is_sustain_pedal(velocity)
            # If the sustain pedal is pressed
            if self.sustain == True:
                # Cycle through all possible channels and send out a control change message with note 64 to indicate that it is a sustain message and velocity 127 (on)
                for control_msg in range(176, 192):
                    self.midi_out.send_message([control_msg, 64, 127])
            # If the sustain pedal has been released
            else:
                # Cycle through all possible channels and send out a control change message with note 64 to indicate that it is a sustain message and velocity 0 (off)
                for control_msg in range(176, 192):
                    self.midi_out.send_message([control_msg, 64, 0])

    def determine_octave(self, note: int):
        """Determines if the current note is an octave of any currently active note.
        If so then it is assigned the channel corresponding to the note in note_heap which is its octave.

        Args:
            note (int): the active Midi note that is being considered

        Returns:
            int: status, the status which encapsulates the Midi channel information. Notes which are octaves of eachother can be on the same channel
        """
        # Define lambda functions to extract the statuses and notes from the sublist [status, note, velocity, dt]
        get_notes = lambda sublist: sublist[0]
        get_status = lambda sublist: sublist[1]
        
        # Extract the statuses and notes from self.note_heap and store them in the 'status' and 'notes' lists
        status = list(map(get_status, self.note_heap))
        notes = list(map(get_notes, self.note_heap))
        
        # Create an unordered list of notes that are octaves of the current note.  The list does not include the current note
        octaves = [octave for octave in range(note + 12, 109, 12)]
        octaves += [octave for octave in range(note - 12, 20, -12)]
    
        # Iterate through the notes list to check if the current note is an octave of any active note
        for active_note in notes:
            # If the active note is in the octaves list (a list of notes which are octaves of the played note)
            if active_note in octaves:
                # Return the status (channel information) so that we can use the same channel as this active note for the currently playing note
                return status[notes.index(active_note)]
        # If no notes are found in the active notes list to be octaves of the current note than return None
        return None
    
    def is_sustain_pedal(self, velocity: int):
        """Is the sustain pedal pressed or not

        Args:
            velocity (int): the state of the pedal (127: the sustain pedal has been pressed, 0: the sustain pedal has been released)
        """
        # Track the state of the sustain pedal for determining what kind of control messages to send out on each channel, SUSTAIN_ON or SUSTAIN_OFF
        if velocity == 127:
            self.sustain = True
        elif velocity == 0:
            self.sustain = False
            
    def turn_off_all_notes(self):
        """Utility function used for silencing all active notes on all channels. Used in testing. FIXME: Remove this function at a later point"""
        # Send All Notes Off message for channel 0
        all_notes_off_message = [176, 123, 0]
        # Iterate through all 16 MIDI channels
        for channel in range(16):  
            # Set the appropriate channel in the status byte and send out the message
            all_notes_off_message[0] = 176 + channel  
            self.midi_out.send_message(all_notes_off_message)

    def set_midi_callback(self):
        """This function filters the output to the console based on the filter function"""
        self.midi_in.set_callback(self.filter)

    def start_listening(self):
        """This is the main loop where execution takes place. The listener waits for Midi messages and acts accordingly based on supporting functions"""
        try:
            print("Listening for MIDI messages. Press Ctrl+C to exit.")
            while True:
                # Get the current message contents, filtering and display are handled by the filter function
                message = self.midi_in.get_message()
                # Add a small delay to control the polling rate
                time.sleep(0.001)
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            self.turn_off_all_notes()
            self.close_port()

    def close_port(self):
        """Close the input and output ports at the end of execution"""
        self.midi_in.close_port()
        self.midi_out.close_port()
        
    def determine_chord(self):
        """Determine chord name to be used internally for just intonation operations as well as visual display to the user
        """
        # Get a list of all of the notes that are currently being played 
        chord_notes = [self.int_note[note[0]] for note in self.note_heap]
        left_hand = chord_notes[0:4]
        right_hand = chord_notes[4:]
        # Create a string by joining a space to each note
        left_chord = " ".join(left_hand)
        right_chord = " ".join(right_hand)
        print(f"{left_chord}   {right_chord}")
        return f"{left_chord}   {right_chord}"
    
    def modify_note_pitch(self, status: int, portemento_value: int):
        """Modify the pitch of a channel by entering a pitch bend value, channel is obtained through status bytes.

        Args:
            status (int): Message | Channel, used to send portemento message to proper channel
            portemento_value (int): pitch bend takes values (0 to 127)
        """
        # Constructing the pitch bend message
        portemento_message = [status, 65, portemento_value]
        # Sending the pitch bend message
        self.midi_out.send_message(portemento_message)

    def just_intonation(self):
        """Retune the keyboard to match just intonation"""
        # TODO: Finish basic case of major triad
        # TODO: Create a self.just_intonation boolean to compare and contrast just intonation with equal temperment
        # TODO: Handle all combinations of 3 notes
        # TODO: Handle all combinations of 4 notes
        # TODO: Investigate if there is some more general intervallic way of handling m notes
        # If the active notes list has only three notes
        if len(self.note_heap) == 3:
            # Get the statuses and note numbers for each note
            sorted_note_heap = sorted(self.note_heap)
            note1, status1, _, _ = sorted_note_heap[0]
            note2, status2, _, _ = sorted_note_heap[1]
            note3, status3, _, _ = sorted_note_heap[2]
            
            print(status1, status2, status3)

            # Check for major triad
            if abs(note1 - note2) in [4, 7] and abs(note1 - note3) in [4, 7]:
                pass
                
                

def main():
    """Instantiates the class, opens ports, sets the callback for filtered Midi output, and listens for events"""
    midi_controller = MidiController()
    midi_controller.initialize_ports()
    midi_controller.set_midi_callback()
    midi_controller.start_listening()

if __name__ == "__main__":
    main()
