# Setup
To setup the software, a few programs are required:
1. MIDI-OX
2. loopMIDI

MIDI-OX is the interface used to setup your Midi IO. 
loopMIDI is a program used to setup virtual ports for routing Jacobs-Ladder and software instruments together.

To get started with running MidiReader.py do the following:
1. Download MIDI-OX and loopMIDI
2. Setup two virtual ports in loopMIDI. This is done by creating a name for the port and pressing the plus sign.  Name the first port jacobs_ladder and the second port software_instrument. Note that if you close out of the loopMIDI program the ports stay up.  To stop the connection you must click on the port in loopMIDI and then click the minus sign.
3. Now open up MIDI-OX and select Options > Midi Devices...
4. A new window will open with all of the devices you have available for MIDI input and output. For Midi Input select your keyboard, and for Midi output select the two ports you created in step 2.
5. After selecting OK you can test the connection by pressing keys on your keyboard. You should see the raw data coming through on the MIDI-OX - [Monitor - Output]
6. Now navigate to MidiReader.py and run the script. You may need to adjust the port in the initializer so that it matches the port you created in step 2. If you don't know how to do this then uncomment the print statement in the class constructor to see a list of all the ports. If `jacobs_ladder` is the third port in the list, then you would set port_name='jacobs_ladder 3' in the initializer. 
7. After running MidiReader.py, ensure that you are getting MIDI data printed to the console when you press keys on the keyboard
8. Now open up your software instrument and connect it to the port called software_instrument. At this stage you should see that your able to hear the output of the MIDI data in your software instrument.