from .DataClasses import DisplayNote, NoteProcessResult
from .Enums import Algorithm, PlayMode

class NoteMap:
    def __init__(self, name: str, octaveNoteMap: dict, algorithm: Algorithm, active: bool, keyCenter: int = 60) -> None:
        self.name = name
        self.octaveNoteMap = octaveNoteMap
        self.noteMapping = [0] * 88
        self.algorithm = algorithm
        self.active = active
        self.keyCenter = keyCenter
        self.__midiRange__ = range(21,109,1)

        if not self.__validate__():
            raise RuntimeError(f"octaveNoteMaps must have a length less than 12, and all keys/values must be in the midi range: {self.__midiRange__[0]}-{self.__midiRange__[-1]}\n")
        
        self.intervalMap = self.__createOctaveIntervalMap__()
        self.__calculateNoteMappings__()
        
    def editOctaveNoteMap(self, key: int, value: int) -> bool:
        """Update or add a new key value pair to the octaveNoteMap so long as the note map is less than length 12

        Args:
            key (int): the key you want to add or update
            value (int): the value for that corresponding key you wish to update 

        Returns:
            bool: True on successful update, False otherwise
        """
        pitch_class = key % 12

        if len(self.octaveNoteMap) > 11 and pitch_class not in self.octaveNoteMap:
            return False

        self.octaveNoteMap[pitch_class] = value

        self.intervalMap = self.__createOctaveIntervalMap__()
        self.__calculateNoteMappings__()

        return True

    def getName(self) -> str:
        """Get the name of the NoteMap

        Returns:
            str: name
        """
        return self.name
    
    def getNegativeHarmonyNote(self, note: int) -> int:
        """Get the negative harmony version of your note if your NoteMap is active and return the same note back otherwise 

        Args:
            note (int): a Midi note represented as an int [21-108]

        Returns:
            int: negative harmony version of your note if NoteMap is active and your original note otherwise
        """
        if not self.active:
            return None

        if note not in self.__midiRange__:
            return None

        return self.noteMapping[note - self.__midiRange__[0]]
        
    def isActive(self) -> bool:
        """Check if the current NoteMap is active

        Returns:
            bool: True if active, False otherwise
        """
        return self.active
    
    def setActive(self, active: bool) -> None:
        """Set the NoteMap instance to active for getting negative harmony notes

        Args:
            active (bool): True if you want NoteMap to be active and False otherwise
        """
        self.active = active
        return

    def setAlgorithm(self, algorithm: Algorithm) -> None:
        """Sets the algorithm and updates the Interval and Note Maps based on the new algorithm

        Args:
            algorithm (Algorithm): a negative harmony algorithm for deciding how notes should be transformed
        """
        self.algorithm = algorithm
        self.intervalMap = self.__createOctaveIntervalMap__()
        self.__calculateNoteMappings__()
        return
    
    def setKeyCenter(self, keyCenter: int) -> None:
        """Sets the key center and re-calculates the note mappings if the algorithm is of type FIXED_AXIS

        Args:
            keyCenter (int): the Midi note representation of the current key center [21-108]
        """
        self.keyCenter = keyCenter
        if self.algorithm == Algorithm.FIXED_AXIS:
            self.__calculateNoteMappings__()
    
    def __calculateNoteMappings__(self) -> None:
        """Creates the noteMapping list used to transform notes to negative harmony handling both fixed and non-fixed axis note transformations"""
        for index, note in enumerate(self.__midiRange__):
            if self.algorithm == Algorithm.FIXED_AXIS:
                self.noteMapping[index] = self.__mapFixedAxisNote__(note)
            else:
                interval = self.__mapNonFixedAxisInterval__(note)
                mapped_note = note + interval

                if mapped_note not in self.__midiRange__:
                    mapped_note = self.__wrapToPianoRange__(mapped_note)

                self.noteMapping[index] = mapped_note

    def __createOctaveIntervalMap__(self) -> dict:
        """Creates the interval map used to calculate the note mappings and post-proccesses the interval map using the selected algorithm

        Raises:
            RuntimeError: if either this function is run with algorithm=FIXED_AXIS or a non recognized algorithm type is selected for the NoteMap class

        Returns:
            dict: an interval map the length of an octave
        """
        octaveIntervalMap = {}
        for key, value in self.octaveNoteMap.items():
            pitch_class = key % 12
            interval = value - key

            normalized_interval = ((interval + 6) % 12) - 6
            octaveIntervalMap[pitch_class] = normalized_interval

            match self.algorithm:
                case Algorithm.CLOSEST_OCTAVE:
                    self.__mapClosestOctave__(octaveIntervalMap, pitch_class)
                case Algorithm.FIXED_AXIS:
                    pass
                case Algorithm.LOWER_OCTAVE:
                    self.__mapLowerOctave__(octaveIntervalMap, pitch_class)
                case Algorithm.UPPER_OCTAVE:
                    self.__mapUpperOctave__(octaveIntervalMap, pitch_class)
                case _:
                    raise RuntimeError(f"Unexpected algorithm type {self.algorithm}")

        return octaveIntervalMap      

    def __mapNonFixedAxisInterval__(self, note: int) -> int:
        """Map a note to an interval based on a non fixed axis approach

        Args:
            note (int): Midi note in range [21-108]

        Returns:
            int: interval derrived from algorithm type
        """
        return self.intervalMap[note % 12]

    def __mapFixedAxisNote__(self, note: int) -> int:
        """Map a note to a new note based on a fixed axis approach

        Args:
            note (int): Midi note in range [21-108]

        Raises:
            RuntimeError: if either note or self.keyCenter are in an invalid state

        Returns:
            int: a Midi note in range [21-108]
        """
        if note == self.keyCenter:
            return note
        elif note > self.keyCenter:
            newNote = self.keyCenter - (note - self.keyCenter)
            if newNote in self.__midiRange__:
                return newNote
            else:
                return self.__wrapToPianoRange__(note=newNote)
        elif note < self.keyCenter:
            newNote = self.keyCenter + (self.keyCenter - note)
            if newNote in self.__midiRange__:
                return newNote
            else:
                return self.__wrapToPianoRange__(note=newNote)
        raise RuntimeError("Either note or self.keyCenter are in an invalid state.")
    
    def __mapClosestOctave__(self, octaveIntervalMap: dict, pitchClass: int) -> None:
        """Helper function for mapping intervals to their closest octave considering the key as the center about which the interval has the shortest absolute intervallic distance

        Args:
            octaveIntervalMap (dict): an octaveIntervalMap you wish to modify using CLOSEST_OCTAVE algorithm
            pitchClass (int): the pitch class you wish to modify in the interval map
        """
        if octaveIntervalMap[pitchClass] > 6:
            octaveIntervalMap[pitchClass] -= 12
        elif octaveIntervalMap[pitchClass] < -6:
            octaveIntervalMap[pitchClass] += 12
        return

    def __mapLowerOctave__(self, octaveIntervalMap: dict, pitchClass: int) -> None:
        """Helper function for mapping intervals to their lower octave by mapping all positive intervals to their negative counterparts by subtracting 12 from them

        Args:
            octaveIntervalMap (dict): an octaveIntervalMap you wish to modify using LOWER_OCTAVE algorithm
            pitchClass (int): the pitch class you wish to modify in the interval map
        """
        if octaveIntervalMap[pitchClass] > 0:
            octaveIntervalMap[pitchClass] -=  12
        return

    def __mapUpperOctave__(self, octaveIntervalMap: dict, pitchClass: int) -> None:
        """Helper function for mapping intervals to their upper octave by mapping all negative intervals to their positive counterparts by adding 12 to them

        Args:
            octaveIntervalMap (dict): an octaveIntervalMap you wish to modify using UPPER_OCTAVE algorithm
            pitchClass (int): the pitch class you wish to modify in the interval map
        """
        if octaveIntervalMap[pitchClass] < 0:
            octaveIntervalMap[pitchClass] += 12
        return
        
    def __repr__(self) -> str:
        """Structured representation of the class for debugging purposes

        Returns:
            str: a stringified representation of the NoteMap class
        """
        return f"{self.name}: {self.noteMapping}"

    def __wrapToPianoRange__(self, note: int) -> int:
        """Wrap notes which get transformed to outside of the midi range to their nearest octave within the midi range [21-108]

        Args:
            note (int): Midi note (not necessarily in the traditional Midi range [21-108])

        Raises:
            RuntimeError: if note is within the traditional Midi range [21-108]

        Returns:
            int: Midi note within the traditional Midi range [21-108]
        """
        if note > self.__midiRange__[-1]:
            while note > self.__midiRange__[-1]:
                note -= 12
            return note
        elif note < self.__midiRange__[0]:
            while note < self.__midiRange__[0]:
                note += 12
            return note
        raise RuntimeError(f"Note is within the inclusive range of {self.__midiRange__[0]}-{self.__midiRange__[-1]} and must be outside of this range for this function call to be valid")

    def __validate__(self) -> bool:
        """Called on construction to verify that both the length of the octaveNoteMap is correct and that the keys and values within the map are within the traditional Midi note range [21-108]

        Returns:
            bool: True on successful validation, False otherwise
        """
        if len(self.octaveNoteMap.keys()) > 12:
            return False
        for key, value in self.octaveNoteMap.items():
            if key not in self.__midiRange__:
                return False
            elif value not in self.__midiRange__:
                return False
        return True
    
class NegativeHarmony:

    def __init__(self, playMode: PlayMode = PlayMode.SUBSTITUTE):
        self.play_mode = playMode
        self.maps = []

    def addNoteMapping(self, noteMap: NoteMap) -> None:
        """Add a new NoteMap to the NagativeHarmony class

        Args:
            map (NoteMap): a note mapping which can be used to map notes to their revolved or reflected variants
        """
        if noteMap.getName() not in [name.getName() for name in self.maps]:
            self.maps.append(noteMap)

    def editMapNote(self, name: str, key: int, value: int):
        for map in self.maps:
            if map.getName() == name:
                return map.editOctaveNoteMap(key, value)

    def getMaps(self) -> list[NoteMap]:
        return self.maps
    
    def getPlayMode(self) -> PlayMode:
        return self.play_mode

    def processNoteOn(self, note: int) -> NoteProcessResult:

        if self.playMode == PlayMode.ORIGINAL_ONLY:
            return NoteProcessResult(
                display=[DisplayNote("Original", note)],
                play=[note]
            )

        display_notes = []
        mapped_notes = []

        for note_map in self.maps:

            if not note_map.isActive():
                continue

            mapped_note = note_map.getNegativeHarmonyNote(note)

            if mapped_note is None:
                continue

            display_notes.append(DisplayNote(note_map.getName(), mapped_note))
            mapped_notes.append(mapped_note)

        if self.playMode == PlayMode.SUBSTITUTE:
            play_notes = mapped_notes

        elif self.playMode == PlayMode.LAYERED:
            display_notes.insert(0, DisplayNote("Original", note))
            play_notes = [note] + mapped_notes

        else:
            play_notes = [note]

        return NoteProcessResult(
            display=display_notes,
            play=play_notes
        )
    
    def processNoteOff(self, note: int) -> list:
        
        if self.playMode == PlayMode.ORIGINAL_ONLY:
            return [note]

        mapped_notes = []

        for note_map in self.maps:
            if note_map.isActive():
                mapped = note_map.getNegativeHarmonyNote(note)
                if mapped is not None:
                    mapped_notes.append(mapped)

        if self.playMode == PlayMode.SUBSTITUTE:
            return mapped_notes

        elif self.playMode == PlayMode.LAYERED:
            return [note] + mapped_notes

        return [note]

    def removeNoteMapping(self, name: str) -> None:
        """Remove a map from the Negative Harmony class

        Args:
            name (str): the name of the map to remove
        """
        for map in self.maps:
            if map.getName() == name:
                self.maps.remove(map)
                break

    def setMapActive(self, name: str, active: bool) -> None:
        for map in self.maps:
            if map.getName() == name:
                map.setActive(active)
                return
    
    def setMapAlgorithm(self, name: str, algorithm: Algorithm) -> None:
        for map in self.maps:
            if map.getName() == name:
                map.setAlgorithm(algorithm)
                return

    def setMapKeyCenter(self, name: str, keyCenter: int) -> None:
        for map in self.maps:
            if map.getName() == name:
                map.setKeyCenter(keyCenter)
                return
            
    def setPlayMode(self, playMode: PlayMode) -> None:
        self.play_mode = playMode
        return
        
if __name__ == "__main__":
    cg_reflected = {60: 67, 61: 66, 62: 65, 63: 64, 64: 63, 65: 62, 66: 61, 67: 60, 68: 71, 69: 70, 70: 69, 71: 68}
    c_revolved = {60: 60, 61: 71, 62: 70, 63: 69, 64: 68, 65: 67, 66: 66, 67: 65, 68: 64, 69: 63, 70: 62, 71: 61}
    noteMapCGReflected = NoteMap(name="C-G reflected", octaveNoteMap=cg_reflected, algorithm=Algorithm.LOWER_OCTAVE, active=True, keyCenter=60)
    noteMapCRevolved = NoteMap(name="C revolved", octaveNoteMap=c_revolved, algorithm=Algorithm.LOWER_OCTAVE, active=True, keyCenter=60)
    print(noteMapCGReflected)
    print(noteMapCRevolved)

