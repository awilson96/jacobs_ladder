# Setup
To setup the software, a few programs are required:
1. MIDI-OX
2. loopMIDI

MIDI-OX is the interface used to setup your Midi IO. 
loopMIDI is a program used to setup virtual ports for routing Jacobs-Ladder and software instruments together.

To get started with running MidiManager.py do the following:
1. Download MIDI-OX and loopMIDI
2. Setup two virtual ports in loopMIDI. This is done by creating a name for the port and pressing the plus sign.  Name the first port `jacobs_ladder` and the second port `jacob`. 
3. Next you will need to make 12 output ports labelled [0, 1, 2, ... 23]. This creates twelve output ports per MidiController instance as you need one output port for every unique note per instance (12 unique notes times 2 instances). 
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
`Remove-Item -Path .\build\ -Recurse -Force; mkdir build; cd build; $PYBIND_DIR = python -c "import pybind11; print(pybind11.get_cmake_dir())"; cmake .. -Dpybind11_DIR="$PYBIND_DIR"; cmake --build .; cd ..`
 

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
    - Configurable tuning allowing the user to select which intervals to use
6. Accurate key determination
    - Only change key when it results in a better tuning
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
    - Lick 
9. Come up with a chord annotation scheme that makes sense and look into algos that can do this automatically
10. Create a GUI for the overall system
11. Integrate RhythmPatterns, VelocityPatterns, and HarmonicPatterns together to produce musical output using some form of Midi generation (cpp implimentation)
12. Design a plan() method for fitting the pattern(s) within a target time frame (i.e one measure, 4 measures, 2 measures and 3 eigth notes, etc.)
13. Create a Midi database creation tool from source separated audio files (start with bass). Impliment an FFT for extracting the midi data for multiple frequency registers and instruments.
14. Create a genre determination algorithm (ML)
15. Create LLM like architecture for creating a musical `meaning` space and use it for performing unsupervised learning, music research tasks, classification of good vs bad based on specific user interactions.
16. Create a negative harmony conversion option
17. Integrate tuning selection into JI from TuningUtils.py and add support to determine the list of possible tunings for roots which are not present in the current list of held down notes

## Midi Database sources
- https://soundsoft.de/
- Freemidi.org
- https://www.midi-hits.com/

## Music scores sources
- https://imslp.org/ (classical, paid)
- https://www.pianostreet.com/?q=Mozart&size=n_20_n (classical, paid)
- http://sheetmusicinternational.com/login (classical, paid, but watermarked downloads are free)
- http://pop-sheet-music.com/home.html (free pop)

## Textbooks
Music similarity and retreival: an introduction to audio and web based strategies

## Youtube
https://www.youtube.com/watch?v=SRrQ_v-OOSg&list=PL-wATfeyAMNqIee7cH3q1bh4QJFAaeNv0&index=7