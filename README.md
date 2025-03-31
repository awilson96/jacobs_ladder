# Setup
To setup the software, a few programs are required:
1. MIDI-OX
2. loopMIDI

MIDI-OX is the interface used to setup your Midi IO. 
loopMIDI is a program used to setup virtual ports for routing Jacobs-Ladder and software instruments together.

To get started with running MidiManager.py do the following:
1. Download MIDI-OX and loopMIDI
2. Setup two virtual ports in loopMIDI. This is done by creating a name for the port and pressing the plus sign.  Name the first port `jacobs_ladder` and the second port `jacob`. 
3. Next you will need to make 12 output ports labelled [0, 1, 2, ... 23]. This creates tweleve output ports per MidiController instance as you need one output port for every unique note per instance (12 unique notes times 2 instances). 
4. You can close out of the loopMIDI program as the ports stay up after the application is closed.  To stop the connection you must click on the port in loopMIDI and then click the minus sign.
5. Now open up MIDI-OX and select Options > Midi Devices...
6. A new window will open with all of the devices you have available for MIDI input and output. For Midi Input select your keyboard, and for Midi output select the ports you created in step 2 called `jacobs_ladder`
5. After selecting OK you can test the connection by pressing keys on your keyboard. You should see the raw data coming through on the MIDI-OX - [Monitor - Output]
6. Now navigate to MidiManager.py and run the script. 
7. After running MidiManager.py, ensure that you are getting MIDI data printed to the User.log file when you press keys on the keyboard.
8. Now open up your software instrument and connect it to the 24 output ports you created in step 3. Note that you will need a separate software instrument for each output port for a total of 24 software instruments (i.e. software instrument 0 would be mapped to index 0 and so on). At this stage you should see that your able to hear the output of the MIDI data in your software instrument.  Note that your software instrument should play nothing if the script is not running.
9. See the usage section for further flags you can use to enhance how the script is run.

# Environment
To create an anaconda environment with all of the required dependencies, run the following line of code in the terminal.
- `conda env create -f environment.yaml`

# Usage:
```
usage: MidiManager.py [-h] [-p] [-t]

Initialize the MidiController with specific settings.

options:
  -h, --help    show this help message and exit
  -p, --print   Enable printing to the console.
  -t, --tuning  Enable tuning.
```

# Cython compilation
`cd ~/jacobs_ladder/`
`python -m bindings.compile build_ext --inplace`

# Pybind build
Clean and Rebuild
`Remove-Item -Path .\cpp_build\ -Recurse -Force; mkdir cpp_build; cd cpp_build; $PYBIND_DIR = python -c "import pybind11; print(pybind11.get_cmake_dir())"; cmake .. -Dpybind11_DIR="$PYBIND_DIR"; cmake --build .; cd ..`
 

# Future Work
1. Multiple instances of Jacob with different instrument configurations
2. Quick setup of the MidiController and Jacob with mappings to software instruments
3. Recording capabilities with scripts to automate creating midi data for each tuning channel.
4. Creation of Midi files from recordings
5. Just Intonation
    - Compensation for pitch drift
    - Dynamic tuning according to key
    - Incremental note transition tuning model
    - Minimum pitch drift model
    - Configurable tuning allowing the user to select whih intervals to use
    - Create default tuning configs
    - Create static tuning capability with no pitch drift
6. Accurate key determination
    - Only change key when it results in a better tuning
    - Keep the key the same if the key is still in the list
    - Only keep track of the major keys until major keys no longer describe the notes being played
7. Rhythem generators capable of creating complex rhythems for Jacob to play
    - Individual note rhythem
    - Chord rhythem
    - Auto tempo discovery
    - Polyrhythems
    - Static tempo configuration
8. Lick database
    - Commonly used motifs
    - Key independance
    - Tempo independance
    - Lick identification