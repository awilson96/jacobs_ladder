from DataClasses import Scale


# Major/Minor scales
C_Major = Scale("C Ionian", ["C", "D", "E", "F", "G", "A", "B"])
Db_Major = Scale("D\u266d Ionian", ["D\u266d", "E\u266d", "F", "G\u266d", "A\u266d", "B\u266d", "C"])
D_Major = Scale("D Ionian", ["D", "E", "G\u266d", "G", "A", "B", "D\u266d"])
Eb_Major = Scale("E\u266d Ionian", ["E\u266d", "F", "G", "A\u266d", "B\u266d", "C", "D"])
E_Major = Scale("E Ionian", ["E", "G\u266d", "A\u266d", "A", "B", "D\u266d", "E\u266d"])
F_Major = Scale("F Ionian", ["F", "G", "A", "B\u266d", "C", "D", "E"])
Gb_Major = Scale("G\u266d Ionian", ["G\u266d", "A\u266d", "B\u266d", "B", "D\u266d", "E\u266d", "F"])
G_Major = Scale("G Ionian", ["G", "A", "B", "C", "D", "E", "G\u266d"])
Ab_Major = Scale("A\u266d Ionian", ["A\u266d", "B\u266d", "C", "D\u266d", "E\u266d", "F", "G"])
A_Major = Scale("A Ionian", ["A", "B", "D\u266d", "D", "E", "G\u266d", "A\u266d"])
Bb_Major = Scale("B\u266d Ionian", ["B\u266d", "C", "D", "E\u266d", "F", "G", "A"])
B_Major = Scale("B Ionian", ["B", "D\u266d", "E\u266d", "E", "G\u266d", "A\u266d", "B\u266d"])

def get_major_scales():
    return [C_Major, Db_Major, D_Major, Eb_Major, E_Major, F_Major, 
            Gb_Major, G_Major, Ab_Major, A_Major, Bb_Major, B_Major]
    
def get_major_scales_dict():
    scales = get_major_scales()
    return {scale.name: scale.notes for scale in scales}