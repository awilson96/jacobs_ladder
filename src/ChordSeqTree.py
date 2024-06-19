import itertools

class ChordSeqTree:
    """
    List the possible combinations of a group of chords.  This study utility is useful for iterating through the 
    possible chord combinations that are possible for a given list of chords.
    """
    
    def __init__(self):
        pass
    
    def generate_chord_sequences(self, chords: list, choices: int):
        combinations = list(itertools.combinations(chords, choices))
        print(f"With {len(chords)} possible chords and {choices} choices: \nThere are {len(combinations)} possible chord sequences\n")
        
        return combinations
    

if __name__ == "__main__":
    cst = ChordSeqTree()
    
    chords = ["I Major 7", "I Dominant 7", "I Minor 7", 
              "bII Major 7", "bII Dominant 7", 
              "II Minor 7", "II Dominant 7", "II Minor 7 b5", 
              "bIII Major 7", "bIII Diminished", 
              "III Minor 7", "III Dominant 7", 
              "IV Major 7", "IV Minor 7", "IV Minor 7 b5", 
              "bV Minor 7 b5",
              "V Dominant", "V Minor 7", 
              "bVI Diminshed", "bVI Major 7", "bVI Dominant", 
              "VI Minor 7", "VI Dominant 7",
              "bVII Dominant", "bVII Minor 7",
              "VII Diminished", "VII Minor 7 b5"]
    
    cst.generate_chord_sequences(chords=chords, choices=2)
    cst.generate_chord_sequences(chords=chords, choices=3)
    cst.generate_chord_sequences(chords=chords, choices=4)