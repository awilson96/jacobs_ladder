Midi Reader: 
*Requirements:
    *Reads Midi data in real time
    *Read static Midi files
    
Midi Writer:
*Requirements:
    *Writes Midi data in real time
    *Writes Midi data upon request
    
Midi Data Interface:
*Requirements:
    *Contains all possible Midi notes & operations
    *Table of all Midi Notes
    *Table of all Midi Operations
    *Contains a mapping from Midi notes to GUI notes
    *Contains a mapping from Midi notes to letter notes (for debugging)
    *Contains all possible scales database
    *Contains all possible range (m : n) note chords where m=2 and n=16 (16 channels)
    
Graphical User Interface:
*Requirements:
    *Create GUI for chord/note display
    *Integrate Synthesia into GUI
    *Integrate sheet music style display 
    *Integrate slash chord style display
    *Create suggestions section
    *Makes right hand scale suggestions based on left hand chord (chord-suggest)
    *Makes left hand chord suggestions based on right hand notes (scale-suggest)
    
LED Array Hardware:
*Requirements:
    *Purchase four hundred color programable LEDs in order to cover an 88-key piano four different times.
    *Create a circuit that will trigger the LEDs according to the correct color based on LED Array Software
    *Purchase or create clear piano keys so that LEDs can shine through
    *Create an initial design in CAD
    *Purchase a micro-controller used to program the LEDs
    *Determine best way to fasten keys to keyboard (since they are see-through)

LED Array Software:
*Requirements:
    *Determine a way of passing in the suggestions section of the GUI as input
    *Use chord suggest to highlight up to four different suggestions using different colors of light
    *Use scale suggest to highlight up to four different suggestions for scales
    
Trainer:
*Requirements:
    *Create help functions for the user to quickly learn things they are not aware of
    *For Example:
    *`help superlocrian bb7 -Bb` (scales)
    *`help dominant7b9` (chords)
    *Align these helper functions with the LED Array Software
    *Create help menu functions:
    *Please choose a key:
    *A, Bb, B, C …
    *Please select:
    *Scales
    *Chords
    *If scales -> Please select:
    *1) {key} Major/Ionian
    *2) {key} Dorian
    *3) {key} Phrygian
    *.
    *.
    *.
    *If chords -> Please select:
    *1) {key} Major
    *2) {key} Minor
    *3) {key} Diminished
    *.
    *.
    *.
    *Example selection A Major/Ionian
    *A B C# D E F# G# A
    *All of these notes light up in a certain color on the piano
    *Sheet Music notes are displayed on GUI
    *All 7 chords for this scale are displayed in a table
    *Example selection A Major
    *A C# E
    *All of these notes light up in a certain color on the piano
    *Sheet Music notes are displayed on GUI
    *All derivative/related chords are displayed in a table
    *Create video tutorial discussing all of the functionality with time stamps so users can click around. 
    
Containerize:
*Requirements:
    *Build the code inside of a C++ container
    *Determine whether to use Linux or PC
    *Determine what languages to use within the container
    *Retune:
*Requirements:
    *This module must retune the notes played by the user to the justly tuned intervals found in nature
    *This module must be configurable as it is in Scala
    *The module should have an option to adjust for pitch drift
    *This module should have the option to be standalone so that it can be 
    *Create a startup menu that asks the user what device they would like to connect to
    *This midi writer should be sending notes to the output device of the users choosing, not some natively build sound by Windows or Linux.

Jacob:
*Requirements:
    *Jacob is an AI that is able to build musical phrases based on user input.
    *Jacob is a trainer as well as a musician.
    *Jacob is able to talk to any of the various submodules
    *He can highlight information in the GUI
    *Controls the LEDs on the keyboard
    *Read Midi data from the user
    *Write Midi data to the user (in the form of him playing for the user)
    *Read text from the user in order to 
    *He is able to communicate difficult processes and explain how they work.
    *Jacob can collaborate with other musicians by injecting musical notes into your jam session.
    *Jacob is trained on chords, scales, phrase libraries, harmonic structures, music theory, and just intonation principles.
    *Jacob will be composed of several different submodules to form his musical knowledge.
    *Rhythm
    *Tempo
    *Time Signatures
    *Space
    *Polyrhythms
    *Melody
    *Repetition
    *Contour
    *Conjunct
    *Disjunct
    *Harmony
    *Voicings
    *Open
    *Closed
    *Scales perspective
    *Chords perspective
    *Drop 2
    *Key determination
    *Style
    *Jacob needs to have a library of Midi sequences from certain musicians
    *If it does not have access to this information, there must be a way to add this information to his library
    *Users should be able to say play music in the style of “Alex Wilson” and Jacob should be able to grab music from that person and emulate that style
    *Jacob should also be able to generally play, for example: Jacob play me some jazz.  Jacob could then play from a library of music classified as jazz. 
    *The main purpose of Jacob is to create novel music, not for him to reproduce another person’s music.
    *Jacob will have the functionality to just play back certain famous songs upon request but that is not the first priority.
    *More to come
