from ...utilities.DataClasses import Scale


# Harmonic Major Scales
C_Harmonic_Major = Scale("C Harmonic Major", ["C", "D", "E", "F", "G", "Ab", "B"])
Db_Harmonic_Major = Scale("Db Harmonic Major", ["D\u266d", "E\u266d", "F", "G\u266d", "A\u266d", "A", "C"])
D_Harmonic_Major = Scale("D Harmonic Major", ["D", "E", "G\u266d", "G", "A", "B\u266d", "D\u266d"])
Eb_Harmonic_Major = Scale("Eb Harmonic Major", ["E\u266d", "F", "G", "A\u266d", "B\u266d", "B", "D"])
E_Harmonic_Major = Scale("E Harmonic Major", ["E", "G\u266d", "A\u266d", "A", "B", "C", "E\u266d"])
F_Harmonic_Major = Scale("F Harmonic Major", ["F", "G", "A", "B\u266d", "C", "D\u266d", "E"])
Gb_Harmonic_Major = Scale("Gb Harmonic Major", ["G\u266d", "A\u266d", "B\u266d", "B", "D\u266d", "D", "F"])
G_Harmonic_Major = Scale("G Harmonic Major", ["G", "A", "B", "C", "D", "E\u266d", "G\u266d"])
Ab_Harmonic_Major = Scale("Ab Harmonic Major", ["A\u266d", "B\u266d", "C", "D\u266d", "E\u266d", "E", "G"])
A_Harmonic_Major = Scale("A Harmonic Major", ["A", "B", "D\u266d", "D", "E", "F", "A\u266d"])
Bb_Harmonic_Major = Scale("Bb Harmonic Major", ["B\u266d", "C", "D", "E\u266d", "F", "G\u266d", "A"])
B_Harmonic_Major = Scale("B Harmonic Major", ["B", "D\u266d", "E\u266d", "E", "G\u266d", "G", "B\u266d"])


def get_harmonic_major_scales():
    return [C_Harmonic_Major, Db_Harmonic_Major, D_Harmonic_Major, Eb_Harmonic_Major, 
            E_Harmonic_Major, F_Harmonic_Major, Gb_Harmonic_Major, G_Harmonic_Major, 
            Ab_Harmonic_Major, A_Harmonic_Major, Bb_Harmonic_Major, B_Harmonic_Major]