from .DataClasses import Scale

# --- Octatonic Scales ---

# Diminished Scale (Half-Whole version) Note: Only three scales are needed because others are shifted copies of one another harmonically speaking
C_Diminished = Scale("C Diminished", ["C", "D\u266d", "E\u266d", "E", "G\u266d", "G", "A", "B\u266d"])
Db_Diminished = Scale("D\u266d Diminished", ["D\u266d", "D", "E", "F", "G", "A\u266d", "B\u266d", "B"])
D_Diminished = Scale("D Diminished", ["D", "E\u266d", "F", "G\u266d", "A\u266d", "A", "B", "C"])

# --- Heptatonic Scales ---

# Major/Minor scales
C_Major = Scale("C Major", ["C", "D", "E", "F", "G", "A", "B"])
Db_Major = Scale("D\u266d Major", ["D\u266d", "E\u266d", "F", "G\u266d", "A\u266d", "B\u266d", "C"])
D_Major = Scale("D Major", ["D", "E", "G\u266d", "G", "A", "B", "D\u266d"])
Eb_Major = Scale("E\u266d Major", ["E\u266d", "F", "G", "A\u266d", "B\u266d", "C", "D"])
E_Major = Scale("E Major", ["E", "G\u266d", "A\u266d", "A", "B", "D\u266d", "E\u266d"])
F_Major = Scale("F Major", ["F", "G", "A", "B\u266d", "C", "D", "E"])
Gb_Major = Scale("G\u266d Major", ["G\u266d", "A\u266d", "B\u266d", "B", "D\u266d", "E\u266d", "F"])
G_Major = Scale("G Major", ["G", "A", "B", "C", "D", "E", "G\u266d"])
Ab_Major = Scale("A\u266d Major", ["A\u266d", "B\u266d", "C", "D\u266d", "E\u266d", "F", "G"])
A_Major = Scale("A Major", ["A", "B", "D\u266d", "D", "E", "G\u266d", "A\u266d"])
Bb_Major = Scale("B\u266d Major", ["B\u266d", "C", "D", "E\u266d", "F", "G", "A"])
B_Major = Scale("B Major", ["B", "D\u266d", "E\u266d", "E", "G\u266d", "A\u266d", "B\u266d"])

# Harmonic Minor Scales
C_Harmonic_Minor = Scale("C Harmonic Minor", ["C", "D", "E\u266d", "F", "G", "A\u266d", "B"])
Db_Harmonic_Minor = Scale("D\u266d Harmonic Minor", ["D\u266d", "E\u266d", "E", "G\u266d", "A\u266d", "A", "C"])
D_Harmonic_Minor = Scale("D Harmonic Minor", ["D", "E", "F", "G", "A", "B\u266d", "D\u266d"])
Eb_Harmonic_Minor = Scale("E\u266d Harmonic Minor", ["E\u266d", "F", "G\u266d", "A\u266d", "B\u266d", "B", "D"])
E_Harmonic_Minor = Scale("E Harmonic Minor", ["E", "G\u266d", "G", "A", "B", "C", "E\u266d"])
F_Harmonic_Minor = Scale("F Harmonic Minor", ["F", "G", "A\u266d", "B\u266d", "C", "D\u266d", "E"])
Gb_Harmonic_Minor = Scale("G\u266d Harmonic Minor", ["G\u266d", "A\u266d", "A", "B", "D\u266d", "D", "F"])
G_Harmonic_Minor = Scale("G Harmonic Minor", ["G", "A", "B\u266d", "C", "D", "E\u266d", "G\u266d"])
Ab_Harmonic_Minor = Scale("A\u266d Harmonic Minor", ["A\u266d", "B\u266d", "B", "D\u266d", "E\u266d", "E", "G"])
A_Harmonic_Minor = Scale("A Harmonic Minor", ["A", "B", "C", "D", "E", "F", "A\u266d"])
Bb_Harmonic_Minor = Scale("B\u266d Harmonic Minor", ["B\u266d", "C", "D\u266d", "E\u266d", "F", "G\u266d", "A"])
B_Harmonic_Minor = Scale("B Harmonic Minor", ["B", "D\u266d", "D", "E", "G\u266d", "G", "B\u266d"])

# Harmonic Major Scales
C_Harmonic_Major = Scale("C Harmonic Major", ["C", "D", "E", "F", "G", "A\u266d", "B"])
Db_Harmonic_Major = Scale("D\u266d Harmonic Major", ["D\u266d", "E\u266d", "F", "G\u266d", "A\u266d", "A", "C"])
D_Harmonic_Major = Scale("D Harmonic Major", ["D", "E", "G\u266d", "G", "A", "B\u266d", "D\u266d"])
Eb_Harmonic_Major = Scale("E\u266d Harmonic Major", ["E\u266d", "F", "G", "A\u266d", "B\u266d", "B", "D"])
E_Harmonic_Major = Scale("E Harmonic Major", ["E", "G\u266d", "A\u266d", "A", "B", "C", "E\u266d"])
F_Harmonic_Major = Scale("F Harmonic Major", ["F", "G", "A", "B\u266d", "C", "D\u266d", "E"])
Gb_Harmonic_Major = Scale("G\u266d Harmonic Major", ["G\u266d", "A\u266d", "B\u266d", "B", "D\u266d", "D", "F"])
G_Harmonic_Major = Scale("G Harmonic Major", ["G", "A", "B", "C", "D", "E\u266d", "G\u266d"])
Ab_Harmonic_Major = Scale("A\u266d Harmonic Major", ["A\u266d", "B\u266d", "C", "D\u266d", "E\u266d", "E", "G"])
A_Harmonic_Major = Scale("A Harmonic Major", ["A", "B", "D\u266d", "D", "E", "F", "A\u266d"])
Bb_Harmonic_Major = Scale("B\u266d Harmonic Major", ["B\u266d", "C", "D", "E\u266d", "F", "G\u266d", "A"])
B_Harmonic_Major = Scale("B Harmonic Major", ["B", "D\u266d", "E\u266d", "E", "G\u266d", "G", "B\u266d"])

# Melodic Minor Scales
C_Melodic_Minor = Scale("C Melodic Minor", ["C", "D", "E\u266d", "F", "G", "A", "B"])
Db_Melodic_Minor = Scale("D\u266d Melodic Minor", ["D\u266d", "E\u266d", "E", "G\u266d", "A\u266d", "B\u266d", "C"])
D_Melodic_Minor = Scale("D Melodic Minor", ["D", "E", "F", "G", "A", "B", "D\u266d"])
Eb_Melodic_Minor = Scale("E\u266d Melodic Minor", ["E\u266d", "F", "G\u266d", "A\u266d", "B\u266d", "C", "D"])
E_Melodic_Minor = Scale("E Melodic Minor", ["E", "G\u266d", "G", "A", "B", "D\u266d", "E\u266d"])
F_Melodic_Minor = Scale("F Melodic Minor", ["F", "G", "A\u266d", "B\u266d", "C", "D", "E"])
Gb_Melodic_Minor = Scale("G\u266d Melodic Minor", ["G\u266d", "A\u266d", "A", "B", "D\u266d", "E\u266d", "F"])
G_Melodic_Minor = Scale("G Melodic Minor", ["G", "A", "B\u266d", "C", "D", "E", "G\u266d"])
Ab_Melodic_Minor = Scale("A\u266d Melodic Minor", ["A\u266d", "B\u266d", "B", "D\u266d", "E\u266d", "F", "G"])
A_Melodic_Minor = Scale("A Melodic Minor", ["A", "B", "C", "D", "E", "G\u266d", "A\u266d"])
Bb_Melodic_Minor = Scale("B\u266d Melodic Minor", ["B\u266d", "C", "D\u266d", "E\u266d", "F", "G", "A"])
B_Melodic_Minor = Scale("B Melodic Minor", ["B", "D\u266d", "D", "E", "G\u266d", "A\u266d", "B\u266d"])

# Diminished Blues Scales
C_Diminished_Blues = Scale("C Diminished Blues", ["C", "D\u266d", "E\u266d", "E", "G\u266d", "G", "B\u266d"])
Db_Diminished_Blues = Scale("D\u266d Diminished Blues", ["D\u266d", "D", "E", "F", "G", "A\u266d", "B"])
D_Diminished_Blues = Scale("D Diminished Blues", ["D", "E\u266d", "F", "G\u266d", "A\u266d", "A", "C"])
Eb_Diminished_Blues = Scale("E\u266d Diminished Blues", ["E\u266d", "E", "G\u266d", "G", "A", "B\u266d", "D\u266d"])
E_Diminished_Blues = Scale("E Diminished Blues", ["E", "F", "G", "A\u266d", "B\u266d", "B", "D"])
F_Diminished_Blues = Scale("F Diminished Blues", ["F", "G\u266d", "A\u266d", "A", "B", "C", "E\u266d"])
Gb_Diminished_Blues = Scale("G\u266d Diminished Blues", ["G\u266d", "G", "A", "B\u266d", "C", "D\u266d", "E"])
G_Diminished_Blues = Scale("G Diminished Blues", ["G", "A\u266d", "B\u266d", "B", "D\u266d", "D", "F"])
Ab_Diminished_Blues = Scale("A\u266d Diminished Blues", ["A\u266d", "A", "B", "C", "D", "E\u266d", "G\u266d"])
A_Diminished_Blues = Scale("A Diminished Blues", ["A", "B\u266d", "C", "D\u266d", "E\u266d", "E", "G"])
Bb_Diminished_Blues = Scale("B\u266d Diminished Blues", ["B\u266d", "B", "D\u266d", "D", "E", "F", "A\u266d"])
B_Diminished_Blues = Scale("B Diminished Blues", ["B", "C", "D", "E\u266d", "F", "G\u266d", "A"])

# Diminsished Harmonic Scales
C_Diminished_Harmonic = Scale("C Diminished Harmonic", ["C", "D\u266d", "E\u266d", "E", "G\u266d", "G", "A"])
Db_Diminished_Harmonic = Scale("D\u266d Diminished Harmonic", ["D\u266d", "D", "E", "F", "G", "A\u266d", "B\u266d"])
D_Diminished_Harmonic = Scale("D Diminished Harmonic", ["D", "E\u266d", "F", "G\u266d", "A\u266d", "A", "B"])
Eb_Diminished_Harmonic = Scale("E\u266d Diminished Harmonic", ["E\u266d", "E", "G\u266d", "G", "A", "B\u266d", "C"])
E_Diminished_Harmonic = Scale("E Diminished Harmonic", ["E", "F", "G", "A\u266d", "B\u266d", "B", "D\u266d"])
F_Diminished_Harmonic = Scale("F Diminished Harmonic", ["F", "G\u266d", "A\u266d", "A", "B", "C", "D"])
Gb_Diminished_Harmonic = Scale("G\u266d Diminished Harmonic", ["G\u266d", "G", "A", "B\u266d", "C", "D\u266d", "E\u266d"])
G_Diminished_Harmonic = Scale("G Diminished Harmonic", ["G", "A\u266d", "B\u266d", "B", "D\u266d", "D", "E"])
Ab_Diminished_Harmonic = Scale("A\u266d Diminished Harmonic", ["A\u266d", "A", "B", "C", "D", "D", "F"])
A_Diminished_Harmonic = Scale("A Diminished Harmonic", ["A", "B\u266d", "C", "D\u266d", "E\u266d", "E", "G\u266d"])
Bb_Diminished_Harmonic = Scale("B\u266d Diminished Harmonic", ["B\u266d", "B", "D\u266d", "D", "E", "F", "G"])
B_Diminished_Harmonic = Scale("B Diminished Harmonic", ["B", "C", "D", "E\u266d", "F", "G\u266d", "A\u266d"])

# --- Hexatonic Scales ---

# Whole Tone Scales: Note: There are only two because all other whole tone scales are shifted copies of the original two
C_Whole_Tone = Scale("C Whole Tone", ["C", "D", "E", "G\u266d", "A\u266d", "B\u266d"])
Db_Whole_Tone = Scale("D\u266d Whole Tone", ["D\u266d", "E\u266d", "F", "G", "A", "B"])

# --- Pentatonic Scales --- 

# Pure Pentatonic Scale
C_Pentatonic = Scale("C Pentatonic", ["C", "D", "E", "G", "A"])
Db_Pentatonic = Scale("D\u266d Pentatonic", ["D\u266d", "E\u266d", "F", "A\u266d", "B\u266d"])
D_Pentatonic = Scale("D Pentatonic", ["D", "E", "G\u266d", "A", "B"])
Eb_Pentatonic = Scale("E\u266d Pentatonic", ["E\u266d", "F", "G", "B\u266d", "C"])
E_Pentatonic = Scale("E Pentatonic", ["E", "G\u266d", "A\u266d", "B", "D\u266d"])
F_Pentatonic = Scale("F Pentatonic", ["F", "G", "A", "C", "D"])
Gb_Pentatonic = Scale("G\u266d Pentatonic", ["G\u266d", "A\u266d", "B\u266d", "D\u266d", "E\u266d"])
G_Pentatonic = Scale("G Pentatonic", ["G", "A", "B", "D", "E"])
Ab_Pentatonic = Scale("A\u266d Pentatonic", ["A\u266d", "B\u266d", "C", "E\u266d", "F"])
A_Pentatonic = Scale("A Pentatonic", ["A", "B", "D\u266d", "E", "G\u266d"])
Bb_Pentatonic = Scale("B\u266d Pentatonic", ["B\u266d", "C", "D", "F", "G"])
B_Pentatonic = Scale("B Pentatonic", ["B", "D\u266d", "E\u266d", "G\u266d", "A\u266d"])

def get_diminished_scales() -> list[Scale]:
    """Getter function for retrieving a list of all possible diminished scale objects

    Returns:
        list[Scale]: a list of diminished scale objects
    """
    return [C_Diminished, Db_Diminished, D_Diminished]

def get_diminished_scales_dict():
    """Getter function for retrieving scale objects as a dictionary 

    Returns:
        dict: a dictionary of name: list of notes pairs 
    """
    scales = get_diminished_scales()
    return {scale.name: scale.notes for scale in scales}

def get_major_scales():
    """Getter function for retrieving a list of all possible major scale objects

    Returns:
        list[Scale]: a list of major scale objects
    """
    return [C_Major, Db_Major, D_Major, Eb_Major, E_Major, F_Major, 
            Gb_Major, G_Major, Ab_Major, A_Major, Bb_Major, B_Major]
    
def get_major_scales_dict():
    """Getter function for retrieving scale objects as a dictionary 

    Returns:
        dict: a dictionary of name: list of notes pairs 
    """
    scales = get_major_scales()
    return {scale.name: scale.notes for scale in scales}

def get_harmonic_minor_scales():
    """Getter function for retrieving a list of all possible harmonic minor scale objects

    Returns:
        list[Scale]: a list of harmonic minor scale objects
    """
    return [C_Harmonic_Minor, Db_Harmonic_Minor, D_Harmonic_Minor, Eb_Harmonic_Minor, 
            E_Harmonic_Minor, F_Harmonic_Minor, Gb_Harmonic_Minor, G_Harmonic_Minor, 
            Ab_Harmonic_Minor, A_Harmonic_Minor, Bb_Harmonic_Minor, B_Harmonic_Minor]
    
def get_harmonic_minor_scales_dict():
    """Getter function for retrieving scale objects as a dictionary 

    Returns:
        dict: a dictionary of name: list of notes pairs 
    """
    scales = get_harmonic_minor_scales()
    return {scale.name: scale.notes for scale in scales}

def get_harmonic_major_scales():
    """Getter function for retrieving a list of all possible harmonic major scale objects

    Returns:
        list[Scale]: a list of harmonic major scale objects
    """
    return [C_Harmonic_Major, Db_Harmonic_Major, D_Harmonic_Major, Eb_Harmonic_Major, 
            E_Harmonic_Major, F_Harmonic_Major, Gb_Harmonic_Major, G_Harmonic_Major, 
            Ab_Harmonic_Major, A_Harmonic_Major, Bb_Harmonic_Major, B_Harmonic_Major]
    
def get_harmonic_major_scales_dict():
    """Getter function for retrieving scale objects as a dictionary 

    Returns:
        dict: a dictionary of name: list of notes pairs 
    """
    scales = get_harmonic_major_scales()
    return {scale.name: scale.notes for scale in scales}

def get_melodic_minor_scales():
    """Getter function for retrieving a list of all possible melodic minor scale objects

    Returns:
        list[Scale]: a list of melodic minor scale objects
    """
    return [C_Melodic_Minor, Db_Melodic_Minor, D_Melodic_Minor, Eb_Melodic_Minor, E_Melodic_Minor, F_Melodic_Minor, 
            Gb_Melodic_Minor, G_Melodic_Minor, Ab_Melodic_Minor, A_Melodic_Minor, Bb_Melodic_Minor, B_Melodic_Minor]

def get_melodic_minor_scales_dict():
    """Getter function for retrieving scale objects as a dictionary 

    Returns:
        dict: a dictionary of name: list of notes pairs 
    """
    scales = get_melodic_minor_scales()
    return {scale.name: scale.notes for scale in scales}

def get_diminished_blues_scales():
    """Getter function for retrieving a list of all possible diminished blues scale objects

    Returns:
        list[Scale]: a list of diminished blues scale objects
    """
    return [C_Diminished_Blues, Db_Diminished_Blues, D_Diminished_Blues, Eb_Diminished_Blues, E_Diminished_Blues, F_Diminished_Blues,
            Gb_Diminished_Blues, G_Diminished_Blues, Ab_Diminished_Blues, A_Diminished_Blues, Bb_Diminished_Blues, B_Diminished_Blues]

def get_diminished_blues_scales_dict():
    """Getter function for retrieving scale objects as a dictionary 

    Returns:
        dict: a dictionary of name: list of notes pairs 
    """
    scales = get_diminished_blues_scales()
    return {scale.name: scale.notes for scale in scales}

def get_diminished_harmonic_scales():
    """Getter function for retrieving a list of all possible diminished harmonic scale objects

    Returns:
        list[Scale]: a list of diminished harmonic scale objects
    """
    return [C_Diminished_Harmonic, Db_Diminished_Harmonic, D_Diminished_Harmonic, Eb_Diminished_Harmonic, E_Diminished_Harmonic, F_Diminished_Harmonic,
            Gb_Diminished_Harmonic, G_Diminished_Harmonic, Ab_Diminished_Harmonic, A_Diminished_Harmonic, Bb_Diminished_Harmonic, B_Diminished_Harmonic]

def get_diminished_harmonic_scales_dict():
    """Getter function for retrieving scale objects as a dictionary 

    Returns:
        dict: a dictionary of name: list of notes pairs 
    """
    scales = get_diminished_harmonic_scales()
    return {scale.name: scale.notes for scale in scales}

def get_whole_tone_scales():
    """Getter function for retrieving a list of all possible whole tone scale objects

    Returns:
        list[Scale]: a list of whole tone scale objects
    """
    return [C_Whole_Tone, Db_Whole_Tone]

def get_whole_tone_scales_dict():
    """Getter function for retrieving scale objects as a dictionary 

    Returns:
        dict: a dictionary of name: list of notes pairs 
    """
    scales = get_whole_tone_scales()
    return {scale.name: scale.notes for scale in scales}

def get_pentatonic_scales():
    """Getter function for retrieving a list of all possible pentatonic scale objects

    Returns:
        list[Scale]: a list of pentatonic scale objects
    """
    return [C_Pentatonic, Db_Pentatonic, D_Pentatonic, Eb_Pentatonic, E_Pentatonic, F_Pentatonic,
            Gb_Pentatonic, G_Pentatonic, Ab_Pentatonic, A_Pentatonic, Bb_Pentatonic, B_Pentatonic]

def get_pentatonic_scales_dict():
    """Getter function for retrieving scale objects as a dictionary 

    Returns:
        dict: a dictionary of name: list of notes pairs 
    """
    scales = get_pentatonic_scales()
    return {scale.name: scale.notes for scale in scales}