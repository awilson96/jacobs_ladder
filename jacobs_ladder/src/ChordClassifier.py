"""
GeneralChordClassifier.py

Matches degree-N interval CSVs against corresponding canonical templates:
 - CHORD_TEMPLATES_4
 - CHORD_TEMPLATES_5
 - CHORD_TEMPLATES_6
 - CHORD_TEMPLATES_7
 - CHORD_TEMPLATES_8
You manually fill in these dictionaries.

Behavior:
 - Reads the CSV.
 - Determines degree (number of interval columns).
 - Looks up the matching dictionary for that degree.
 - Performs rotation matching exactly like the degree-4 script.
 - Outputs a file with "_named" suffix.

Output columns:
   intervals        : canonical (rotated) ordering
   notes            : note names computed from C for matched chords
   identification   : chord name or "Unknown"
"""

from pathlib import Path
import csv

# -----------------------------
# Note names
# -----------------------------
NOTE_NAMES = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]

# -----------------------------
# Canonical templates by degree
# You fill these in manually
# -----------------------------
CHORD_TEMPLATES_4 = {
    "Major7":                        [4,3,4,1],
    "Major7(no5)(add2)":             [2,2,7,1],
    "Major7(no3) #4":                [6,1,4,1],
    "Major7 b5":                     [4,2,5,1],
    "Major(add 4)":                  [4,1,2,5],
    "sus4 Maj7":                     [5,2,4,1],
    "7":                             [4,3,3,2],
    "Half-diminished(m7b5)":         [3,3,4,2],
    "MinorMajor7(mMaj7)":            [3,4,4,1],
    "MinorMajor7(no5)(add4)":        [3,2,6,1],
    "MinorMajor7 #5":                [3,5,3,1],
    "MinorMajor7 b5":                [3,3,5,1],
    "Augmented Major7":              [4,4,3,1],
    "Augmented(add 2)":              [2,2,4,4],
    "Minor7":                        [3,4,3,2],
    "Minor(add 2)":                  [2,1,4,5], 
    "Minor b2":                      [1,2,4,5],
    "Minor7(no5) b2":                [1,2,7,2],
    "7 b5":                          [4,2,4,2],
    "7(no5) b2":                     [1,3,6,2],
    "Fully diminished":              [3,3,3,3],
    "Diminished b2":                 [1,2,3,6],
    "Diminished(no5) b2":            [1,2,6,3],
    "Major(no5)(add 4) b2":          [1,3,1,7],
    "Crunch":                        [1,5,1,5],
    "Minor #4":                      [3,3,1,5],
    "Major #4":                      [4,2,1,5],
    "Half-Whole":                    [1,2,1,8],
    "7(no5) #2":                     [3,1,6,2],
    "Minor(no5)(add 2)(add 6)":      [2,1,6,3],
    "Major7(no5)(add 6)":            [7,2,2,1],
    "7(add 2)":                      [2,2,6,2],
    "Minor(add 4)":                  [3,2,2,5],
    "Major(add 2)":                  [2,2,3,5],
    "7sus4":                         [5,2,3,2]
}

CHORD_TEMPLATES_5 = {
    "Major(add 2)(add 6)":           [2,2,3,2,3],
    "Major(add 2) b6":               [2,2,3,1,4],
    "Augmented(add 2) #4":           [2,2,2,2,4],
    "MinorMajor7(add 6)":            [3,4,2,2,1],
    "7 b2":                          [1,3,3,3,2],
    "Major b2 b6":                   [1,3,3,1,4],
    "Major6 b2":                     [1,3,3,2,3],
    "7 #4":                          [4,2,1,3,2],
    "Minor7 #4":                     [3,3,1,3,2],
    "MinorMajor7(add 4)":            [3,2,2,4,1],
    "7(add 2)":                      [2,2,2,3,3],
    "Major(add 2) #4":               [2,2,2,1,5],
    "Major7(add 6)":                 [4,3,2,2,1],
    "Major7(add6) b5":               [4,2,3,2,1],
    "Major7 #4":                     [4,2,1,4,1],
    "Major #4 b2":                   [1,3,2,1,5],
    "Major7sus4 b6":                 [5,2,1,3,1],
    "Major7 b6":                     [4,3,1,3,1],
    "Major7 #2":                     [3,1,3,4,1],
    "Major7sus2(add 6)":             [2,5,2,2,1],
    "Major7 b5 #2":                  [3,1,2,5,1],
    "Minor7 #2":                     [1,2,4,3,2],
    "Minor6 #2":                     [1,2,4,2,3],
    "Major7(add 4)":                 [4,1,2,4,1],
    "Minor7 b5 #2":                  [1,2,3,4,2],
    "Fully diminished b2":           [1,2,3,3,3],
    "Major7sus2sus4":                [2,3,2,4,1],
    "Minor #4 b2":                   [1,2,3,1,5],
    "7sus2(add 6)":                  [2,5,2,1,2],
    "7 b6":                          [4,3,1,2,2],
    "Minor7 b6":                     [3,4,1,2,2],
    "Major7(add 2) b5":              [2,2,2,5,1],
    "Diminshed(add 4) b2":           [1,2,2,1,6],
    "Diminished(add 2,4)":           [2,1,2,1,6],
    "MinorMajor7(add 2) #5":         [2,1,5,3,1],
    "Augmented7(add6)":              [4,4,1,2,1],
    "Major(add b2,#2)":              [1,2,1,3,5],
    "Diminished(add b2,#2)":         [1,2,1,2,6]
}

CHORD_TEMPLATES_6 = {
    "Diminished Scale(no7,no8)":     [1,2,1,2,1,5],
    "Harmonic Minor(no6)":           [2,1,2,2,4,1],
    "Harmonic Minor(no5)":           [2,1,2,3,3,1],
    "Melodic Minor(no5)":            [2,1,2,4,2,1],
    "Harmonic Major(no2)":           [4,1,2,1,3,1],
    "Diminished Scale(no5,no8)":     [1,2,1,3,2,3],
    "-2Harmonic Major(rootless)":    [2,1,2,1,3,3],
    "Harmonic Minor(no4)":           [2,1,4,1,3,1],
    "Melodic Minor(no4)":            [2,1,4,2,2,1],
    "Major Scale(no6)":              [2,2,1,2,4,1],
    "Harmonic Major(no5)":           [2,2,1,3,3,1],
    "Major Scale(no5)":              [2,2,1,4,2,1],
    "Major Scale(no2)":              [4,1,2,2,2,1],
    "-2Melodic Minor(rootless)":     [1,2,2,2,2,3],
    "Melodic Minor(no7)":            [2,1,2,2,2,3],
    "Harmonic Major(no4)":           [2,2,3,1,3,1],
    "Major Scale(no7)":              [2,2,1,2,2,3],
    "Diminished Scale(no4,no8)":     [1,2,3,1,2,3],
    "Diminished Scale(no4,no7)":     [1,2,3,1,3,2],
    "Harmonic Major(no3)":           [2,3,2,1,3,1],
    "Major Scale(no3)":              [2,3,2,2,2,1],
    "Augmented scale":               [1,3,1,3,1,3],
    "Harmonic Minor(no2)":           [3,2,2,1,3,1],
    "Diminished Scale(no3,no7)":     [1,3,2,1,3,2],
    "Melodic Minor(no2)":            [3,2,2,2,2,1],
    "Whole Tone Scale":              [2,2,2,2,2,2]
}
CHORD_TEMPLATES_7 = {
    "Diminished Scale(no8)":         [1,2,1,2,1,2,3],
    "Diminished Scale(no7)":         [1,2,1,2,1,3,2],
    "Harmonic Minor":                [2,1,2,2,1,3,1],
    "Melodic Minor":                 [2,1,2,2,2,2,1],
    "Harmonic Major":                [2,2,1,2,1,3,1],
    "Major Scale":                   [2,2,1,2,2,2,1]
}
CHORD_TEMPLATES_8 = {
    "Diminished Scale":              [1,2,1,2,1,2,1,2]
}

TEMPLATES_BY_DEGREE = {
    4: CHORD_TEMPLATES_4,
    5: CHORD_TEMPLATES_5,
    6: CHORD_TEMPLATES_6,
    7: CHORD_TEMPLATES_7,
    8: CHORD_TEMPLATES_8,
}


def rotate(lst, n):
    return lst[n:] + lst[:n]

def all_rotations(lst):
    return [rotate(lst, i) for i in range(len(lst))]

def intervals_to_notes(intervals, root_pc=0):
    notes = [root_pc]
    s = root_pc
    for iv in intervals[:-1]:
        s = (s + iv) % 12
        notes.append(s)
    return [NOTE_NAMES[n] for n in notes]


def find_rotation_match(intervals, template_dict):
    """
    Try rotations of 'intervals' and check if any match a canonical template.
    Returns (rotated_intervals, template_name) or (None, None).
    """
    for rot in all_rotations(intervals):
        for name, canon in template_dict.items():
            if rot == canon:
                return rot, name
    return None, None


def classify_csv(path: Path):
    if not path.exists():
        raise SystemExit(f"File not found: {path}")

    # read CSV
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("Empty CSV")
        return

    # detect degree from column count
    degree = len(reader.fieldnames)

    if degree not in TEMPLATES_BY_DEGREE:
        raise ValueError(f"No template dictionary defined for degree {degree}")

    template_dict = TEMPLATES_BY_DEGREE[degree]

    # output file
    out_path = path.with_name(path.stem + "_named.csv")

    rows_out = []
    for row in rows:
        intervals = [int(row[c]) for c in reader.fieldnames]

        rot, name = find_rotation_match(intervals, template_dict)

        if name:
            notes = intervals_to_notes(rot, 0)
            rows_out.append({
                "intervals": ",".join(str(x) for x in rot),
                "notes": ",".join(notes),
                "identification": name
            })
        else:
            rows_out.append({
                "intervals": ",".join(str(x) for x in intervals),
                "notes": "",
                "identification": "Unknown"
            })

    # write output CSV
    with out_path.open("w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["intervals", "notes", "identification"])
        writer.writeheader()
        for r in rows_out:
            writer.writerow(r)

    print(f"Wrote {out_path}")

if __name__ == "__main__":
    input = Path("possible_scales/degree_4_interval_9_nco_0.csv")
    classify_csv(input)
    input = Path("possible_scales/degree_5_interval_9_nco_0.csv")
    classify_csv(input)
    input = Path("possible_scales/degree_6_interval_9_nco_0.csv")
    classify_csv(input)
    input = Path("possible_scales/degree_7_interval_9_nco_0.csv")
    classify_csv(input)
    input = Path("possible_scales/degree_8_interval_9_nco_0.csv")
    classify_csv(input)