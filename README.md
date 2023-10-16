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
4. A new window will open with all of the devices you have available for MIDI input and output. For Midi Input select your keyboard, and for Midi output select the ports you created in step 2 called jacobs_ladder
5. After selecting OK you can test the connection by pressing keys on your keyboard. You should see the raw data coming through on the MIDI-OX - [Monitor - Output]
6. Now navigate to MidiReader.py and run the script. You may need to adjust the port in the initializer so that it matches the port you created in step 2. If you don't know how to do this then uncomment the print statement in the class constructor to see a list of all the ports. If `jacobs_ladder` is the third port in the list, then you would set port_name='jacobs_ladder 3' in the initializer. 
7. After running MidiReader.py, ensure that you are getting MIDI data printed to the console when you press keys on the keyboard
8. Now open up your software instrument and connect it to the port called software_instrument. At this stage you should see that your able to hear the output of the MIDI data in your software instrument.  Note that your software instrument should play nothing if the script is not running.

# Next Steps
The current progress is that I got each note to be sent out on different channels which will be useful for just intonation
There are a few things that need to be done:
1. The code should be refactored:
  - The variable names should be renamed so that they do not get confused, in one loop there is n note and notes all in the same place making it unclear which is which
2. I need to think about what happens once I add a sustain pedal into the mix, and how that will change things. Specifically, what happens when the number of channels runs out when holding the sustain pedal? Does the ocatave optimization mostly save us from this pitfall or is there a need to setup a second output port and route two outut ports into the software instrument
3. What is the most effecient way to track the state of things. The status byte may need to go somewhere else in the note_heap since the heap is sorted according to the first parameter that is put into the heap. The note is the main data that will be accessed therefore having it already sorted will save a lot of time and effort if we don't need to rely on sorting given the heap state. 
4. I need to build a pitch shift function which takes as params the status byte (from which the channel can be extracted) and the number of cents need to be shifted up or down (minus for down + for positive) It may be more effecient to store the self.available_channels_heap as hex instead of decimal so that there is no need of conversion. The only problem then is how do I add and subtract numbers in hex? May need to see if thisis worth it. 
5. I need a class variable called self.fulcrum which will act as the place from which all other notes will be tuned from. However fulcrum may not be a single note it may need to be a list of the most recently played notes.  Most recently will need to be determined using dt, but also may need to be based on which notes are still active.  This choice will be very difficult and will proabably need to be handled on a case by case basis.
6. It may also be useful to create a class variable called self.key which records the key of the music we are currently playing in.  This variable will be set by a method called set_key() and will also likely need some history to determine what key we are actually in. 
7. There is currently a bug in the software when I play C E G B C E G A and then any note after that makes no tone