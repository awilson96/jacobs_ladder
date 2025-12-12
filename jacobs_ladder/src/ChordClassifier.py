"""
identify_chords_rotations.py

For each interval sequence:
1. Rotate intervals to see if it matches a canonical root-position chord template.
2. If found, set intervals to root-position sequence, compute notes from C.
3. If not found, intervals unchanged, identification Unknown, notes empty.
"""

from pathlib import Path
import csv

# -----------------------
# Config / Templates
# -----------------------
INPUT_CSV = Path("possible_scales/degree_4_interval_9_nco_0.csv")
OUTPUT_CSV = INPUT_CSV.with_name(INPUT_CSV.stem + "_root_rotated.csv")

NOTE_NAMES = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]

# canonical intervals in root position
CHORD_TEMPLATES = {
    "Major7":                        [4,3,4,1],
    "Major7(no5)(add2)":             [2,2,7,1],
    "Major7(no3) #4":                [6,1,4,1],
    "Major7 b5":                     [4,2,5,1],
    "Major(add 4)":                  [4,1,2,5],
    "sus4 Maj7":                     [5,2,4,1],
    "Dominant7":                     [4,3,3,2],
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
    "Dominant7 b5":                  [4,2,4,2],
    "Dominant7(no5) b2":             [1,3,6,2],
    "Fully diminished":              [3,3,3,3],
    "Diminished b2":                 [1,2,3,6],
    "Diminished(no5) b2":            [1,2,6,3],
    "Stacked chromatic major 3rds":  [1,3,1,7],
    "Crunch":                        [1,5,1,5],
    "Minor #4":                      [3,3,1,5],
    "Major #4":                      [4,2,1,5],
    "Half-Whole":                    [1,2,1,8],
    "Dominant7(no5) #2":             [3,1,6,2],
    "Minor(no5)(add 2)(add 6)":      [2,1,6,3],
    "Major7(no5)(add 6)":            [7,2,2,1],
    "Dominant7(add 2)":              [2,2,6,2],
    "Minor(add 4)":                  [3,2,2,5],
    "Major(add 2)":                  [2,2,3,5],
    "Dominant7(sus4)":               [5,2,3,2]
}

def rotate(lst, n):
    """Rotate list lst by n steps to the left"""
    return lst[n:] + lst[:n]

def intervals_to_notes(intervals, root_pc=0):
    """Given a root PC (default C=0) and intervals in root position,
    compute notes (ignore last interval, which just closes the octave)"""
    notes = [root_pc]
    s = root_pc
    for iv in intervals[:-1]:
        s = (s + iv) % 12
        notes.append(s)
    return [NOTE_NAMES[n] for n in notes]

def find_root_position_match(intervals):
    """Try all rotations to see if it matches a canonical root-position chord"""
    n = len(intervals)
    for i in range(n):
        rotated = rotate(intervals, i)
        for chord_name, canon_intervals in CHORD_TEMPLATES.items():
            if rotated == canon_intervals:
                return rotated, chord_name
    return None, None

def main():
    if not INPUT_CSV.exists():
        raise SystemExit(f"Input file not found: {INPUT_CSV}")

    rows_out = []
    with INPUT_CSV.open(newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            intervals_input = [int(row[col]) for col in reader.fieldnames]

            # find root-position rotation
            intervals_root, chord_name = find_root_position_match(intervals_input)

            if chord_name:
                # compute notes from C
                notes = intervals_to_notes(intervals_root, root_pc=0)
                identification = chord_name
            else:
                intervals_root = intervals_input
                notes = [""] * len(intervals_input)
                identification = "Unknown"

            rows_out.append({
                "intervals": ",".join(str(i) for i in intervals_root),
                "notes": ",".join(notes),
                "identification": identification
            })

    # write output CSV
    with OUTPUT_CSV.open("w", newline='') as out_f:
        fieldnames = ["intervals", "notes", "identification"]
        writer = csv.DictWriter(out_f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows_out:
            writer.writerow(r)

    print(f"Wrote results to: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
