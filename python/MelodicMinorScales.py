from Utilities import Scale


# Melodic Minor Scales
C_Melodic_Minor = Scale("C Melodic Minor", ["C", "D", "E\u266d", "F", "G", "A", "B"])
Db_Melodic_Minor = Scale("Db Melodic Minor", ["D\u266d", "E\u266d", "E", "G\u266d", "A\u266d", "B\u266d", "C"])
D_Melodic_Minor = Scale("D Melodic Minor", ["D", "E", "F", "G", "A", "B", "D\u266d"])
Eb_Melodic_Minor = Scale("Eb Melodic Minor", ["E\u266d", "F", "G\u266d", "A\u266d", "B\u266d", "C", "D"])
E_Melodic_Minor = Scale("E Melodic Minor", ["E", "G\u266d", "G", "A", "B", "D\u266d", "E\u266d"])
F_Melodic_Minor = Scale("F Melodic Minor", ["F", "G", "A\u266d", "B\u266d", "C", "D", "E"])
Gb_Melodic_Minor = Scale("Gb Melodic Minor", ["G\u266d", "A\u266d", "A", "B", "D\u266d", "E\u266d", "F"])
G_Melodic_Minor = Scale("G Melodic Minor", ["G", "A", "B\u266d", "C", "D", "E", "G\u266d"])
Ab_Melodic_Minor = Scale("Ab Melodic Minor", ["A\u266d", "B\u266d", "B", "D\u266d", "E\u266d", "F", "G"])
A_Melodic_Minor = Scale("A Melodic Minor", ["A", "B", "C", "D", "E", "G\u266d", "A\u266d"])
Bb_Melodic_Minor = Scale("Bb Melodic Minor", ["B\u266d", "C", "D\u266d", "E\u266d", "F", "G", "A"])
B_Melodic_Minor = Scale("B Melodic Minor", ["B", "D\u266d", "D", "E", "G\u266d", "A\u266d", "B\u266d"])

def get_melodic_minor_scales():
    return [C_Melodic_Minor, Db_Melodic_Minor, D_Melodic_Minor, Eb_Melodic_Minor, E_Melodic_Minor, F_Melodic_Minor, 
            Gb_Melodic_Minor, G_Melodic_Minor, Ab_Melodic_Minor, A_Melodic_Minor, Bb_Melodic_Minor, B_Melodic_Minor]

