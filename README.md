# About
JacobsLadder is an opens source Music AI project which conveys music theory insights to piano players in real time. The eventual goal of this product is to create music AI tools for musicians to more deeply explore music in all of its permutations and possibilities. The current capabilities include a python based MIDI parser, a C++ based real-time note scheduler, and a Dart/Flutter based UI. The parser establishes the necessary hardware abstraction layer for turning MIDI signals coming from the users keyboard into virtual midi ports. The data is read off the virtual midi ports and transformed into music descriptor words (MDWs). These MDWs are transmitted to the front end UI to provide color visualization superimposed on the keyboard. The UI also displays the full list of compatible scales with the currently selected (or held down notes) on the keyboard. This gives the user the knowledge of what scales are *compatible* which the current chord changes and provides insight into their musical options for every possible harmonic context. There are several toggleable filters available including Major Scales, Harmonic Minor Scales, Harmonic Major Scales, and Melodic Minor Scales. This enables to user to focus on a subsection of scales at a time so see how these options fit within their chord changes. Several research tools have also been created. In the file ScaleTree.py, the user can list all of the possible scales in the ether which match the constraints. These configurable constraints are that scales must end on the note they start on, they must not exceed steps of major thirds, they must not have consecutive half steps. The max step size and the max number of consecutive half steps are configurable. The ScaleTree program creates a CSV file containing all of the scales generated for each scale length from 3 note scales (triads) to 8 note scales (optotonic). This is because nine note scales all violate the rule that scales must end on the note where the begin. This program gives way to several novel and interesting scales which have not been studied by the broader music theory community. The python backend also supports real time just intonation. This works by splitting the data by note letter name on the incoming MIDI port into twelve separate MIDI ports acting as individual octave channels. These channels can then be tuned using the pitch wheel inidvidually without affecting the other octave channels. This gives the program single note manipulation abilities. The user can specify the intervals they prefer to use by selecting a pitch config when running the program. Examples can be found in <project_root>/configurations/json/pitch/. The repo also has a file called PolyRhythms.py where users can create PolyRhythm melodies by scheduling alternating melodies at different rhythmic cadences.  This gives the user the ability to experiment around with how perfectly played alternating melodies played simultaneously sound.

# Missing Dependencies
1. pyyaml
2. cython
3. pybind11
4. cmake (for MacOS be sure to install the compiler toolchain via `xcode-select --install` or compilations will fail at later steps)
5. dart/flutter (for MacOS you will need to install xcode from the app store and accept the licensing agreement.)
6. On MacOS `brew install aubio libsndfile fftw libsamplerate`. TODO: either bring everything back to 3.11 or give instructions for setting up a separate conda env for the Tuner functionality to work correctly.

# Setup

## MacOS


## Windows
**TODO: update setup to use setup script instead of manual instructions**
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
To run the MidiManager (the backend), run:

```bash
python -m jacobs_ladder.src.MidiManager ./jacobs_ladder/configuration/yaml/default_config.yaml
```

Navigate the the default_config.yaml for more details on what fields are configurable. 

# Cython compilation

## MacOS
1. Change directories to `cd jacobs_ladder/jacobs_ladder/` and run the following command: `python -m bindings.compile build_ext --inplace`
2. This will produce a file called `tuning_utils.cpython-312-darwin.so`. Copy this file to `jacobs_ladder/jacobs_ladder/`.

## Windows
1. Change directories to `cd jacobs_ladder/jacobs_ladder/` and run the following command: `python -m bindings.compile build_ext --inplace`
2. This will produce a file called <TODO: Name this file>.pyd. Copy this file to `jacobs_ladder/jacobs_ladder/`.


# Pybind/C++ build

## MacOS
Change directories to `jacobs_ladder/jacobs_ladder/cpp/` and run the following command:
```bash
rm -rf build \
&& mkdir build \
&& cd build \
&& PYBIND_DIR=$(python -c "import pybind11; print(pybind11.get_cmake_dir())") \
&& cmake .. -Dpybind11_DIR="$PYBIND_DIR" \
&& cmake --build . \
&& cd ..
```
Note that currently (as of 12/15/25) the only binary which is supported is `RhythmPatternTest` as the `MidiScheduler` relies on `QpcUtils` currently which is a Windows specific timing driver. Also the `VirtualMidiPortScript` is unnecessary for MacOS and Linux since these operating systems can create virtual Midi ports directly in Rtmidi where this API is not supported in Windows due to hardware incompatibility.  

## Windows
Change directories to `jacobs_ladder/jacobs_ladder/cpp` and run the following command: 
```Powershell
Remove-Item -Path .\build\ -Recurse -Force; mkdir build; cd build; $PYBIND_DIR = python -c "import pybind11; print(pybind11.get_cmake_dir())"; cmake .. -Dpybind11_DIR="$PYBIND_DIR"; cmake --build .; cd ..
```

The following binaries are supported for the following tasks:
1. MidiSchedulerExample: Schedules a simple C–E–G chord sequence, repeats the sequence 3 times with proper timing, then waits a few seconds so the notes can play. (see cpp/test/MidiSchedulerExample.cpp for implementation details)
2. MidiSchedulerTest: A more comprehensive suite of MidiScheduler test cases which excerise the various functionalities of the MidiScheduler. (see cpp/test/MidiSchedulerTest.cpp for test case details)
3. QpcUtilsTest: A simple timing test of the various capabilities of the query performance counter based timer. This test excersises the primary functionalities of the QpcUtils class.
4. RhythmPatternTest: Simple test to ensure that RhythmPatterns can be repeatable.
5. VirtualMidiPortScript: Parses a JSON file specifying virtual MIDI port names and counts (see jacobs_ladder/configuration/json/port_configuration/default.json for details). It then creates virtual MIDI ports using the teVirtualMIDI driver and registers a callback to handle incoming MIDI messages for all ports. Then it waits for the user to press Enter while the ports remain active. On close, all virtual ports cleanly before exiting.

Note that the VirtualMidiPortScript **IS REQUIRED** for the MidiManager to work correctly on Windows.

Note: Don't try to compile while any of the cpp binaries are running or you will get copy errors in windows. 

Note: Don't try to compile while any of the cpp binaries are running or you will get copy errors in windows. 

# Dart/Flutter build

## MacOS
1. Install the dart sdk, flutter, ruby, and CocoaPods
```bash
brew install dart-sdk
brew install flutter
brew install ruby
gem install cocoapods
```
2. Change directories to `cd jacobs_ladder/jacobs_ladder/ladder` and run `flutter run`

## Windows
1. Install the flutter sdk from `https://docs.flutter.dev/get-started` and extract it to `C:\flutter\`
2. Add the `C:\flutter\bin\` to the path environmental variable to make the `flutter`/`dart` command globally accessible.
3. Change directories to `cd jacobs_ladder/jacobs_ladder/ladder/` and run `flutter run`
4. Select the desktop 

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
17. Add support to determine the list of possible tunings for roots which are not present in the current list of held down notes

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
