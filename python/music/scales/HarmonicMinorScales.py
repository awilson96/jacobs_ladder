from ...utilities.DataClasses import Scale


# Harmonic Minor Scales
C_Harmonic_Minor = Scale("C Harmonic Minor", ["C", "D", "E\u266d", "F", "G", "A\u266d", "B"])
Db_Harmonic_Minor = Scale("Db Harmonic Minor", ["D\u266d", "E\u266d", "E", "G\u266d", "A\u266d", "A", "C"])
D_Harmonic_Minor = Scale("D Harmonic Minor", ["D", "E", "F", "G", "A", "B\u266d", "D\u266d"])
Eb_Harmonic_Minor = Scale("Eb Harmonic Minor", ["E\u266d", "F", "G\u266d", "A\u266d", "B\u266d", "B", "D"])
E_Harmonic_Minor = Scale("E Harmonic Minor", ["E", "G\u266d", "G", "A", "B", "C", "E\u266d"])
F_Harmonic_Minor = Scale("F Harmonic Minor", ["F", "G", "A\u266d", "B\u266d", "C", "D\u266d", "E"])
Gb_Harmonic_Minor = Scale("Gb Harmonic Minor", ["G\u266d", "A\u266d", "A", "B", "D\u266d", "D", "F"])
G_Harmonic_Minor = Scale("G Harmonic Minor", ["G", "A", "B\u266d", "C", "D", "E\u266d", "G\u266d"])
Ab_Harmonic_Minor = Scale("Ab Harmonic Minor", ["A\u266d", "B\u266d", "B", "D\u266d", "E\u266d", "E", "G"])
A_Harmonic_Minor = Scale("A Harmonic Minor", ["A", "B", "C", "D", "E", "F", "A\u266d"])
Bb_Harmonic_Minor = Scale("Bb Harmonic Minor", ["B\u266d", "C", "D\u266d", "E\u266d", "F", "G\u266d", "A"])
B_Harmonic_Minor = Scale("B Harmonic Minor", ["B", "D\u266d", "D", "E", "G\u266d", "G", "B\u266d"])

def get_harmonic_minor_scales():
    return [C_Harmonic_Minor, Db_Harmonic_Minor, D_Harmonic_Minor, Eb_Harmonic_Minor, 
            E_Harmonic_Minor, F_Harmonic_Minor, Gb_Harmonic_Minor, G_Harmonic_Minor, 
            Ab_Harmonic_Minor, A_Harmonic_Minor, Bb_Harmonic_Minor, B_Harmonic_Minor]