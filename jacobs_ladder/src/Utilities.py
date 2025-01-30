import math
from itertools import product

from .Enums import NoteDivisions

def determine_octave(message_heap: list, note: int):
    """
    Determine if the current note is an octave of any of the currently active notes.

    Args:
        note (int): an active note to check against self.message_heap

    Returns:
        int: returns the instance index if the current note is an octave multiple of an active note and None otherwise
    """
    notes= list(map(lambda sublist: sublist[0], message_heap))
    instance= list(map(lambda sublist: sublist[1], message_heap))

    if note in notes:
        return instance[notes.index(note)]

    octaves= [octave for octave in range(note + 12, 109, 12)]
    octaves += [octave for octave in range(note - 12, 20, -12)]

    for active_note in notes:
        if active_note in octaves:
            return instance[notes.index(active_note)]
    return None
    
def calculate_cents_from_interval(interval: float):
    return math.log2(interval) * 1200

def calculate_cents_offset_from_interval(interval: float):
    cents = calculate_cents_from_interval(interval=interval)
    nearest_interval_cents_value = round(cents, -2)
    return cents - nearest_interval_cents_value

def calculate_analog_pitch_wheel_value_from_cents_offset(cents_offset: float):
    return int(round(cents_offset * 8192 / 200 + 8192, 0))

def division_to_dt(division: str, tempo: int) -> int:
    """Convert a rhythmic division to a time delay (dt) in milliseconds.

    Args:
        division (str): The rhythmic division (e.g., 'WHOLE', 'HALF', 'QUARTER', 'EIGHTH', 'SIXTEENTH').

    Returns:
        int: The delay time in milliseconds.
    """
    try:
        division_ms = abs(NoteDivisions[division.upper()].value)
    except KeyError:
        raise ValueError(f"Invalid division: {division}")
    
    return int(division_ms * (60 / tempo))

def get_root_from_letter_note(letter_note: str):
    match letter_note:
        case "A\u266d":
            return 68
        case "A":
            return 69
        case "B\u266d":
            return 70
        case "B":
            return 71
        case "C":
            return 60
        case "D\u266d":
            return 61
        case "D":
            return 62
        case "E\u266d":
            return 63
        case "E":
            return 64
        case "F":
            return 65
        case "G\u266d":
            return 66
        case "G":
            return 67
        
"""Given a list of notes, generate all possible tunings based on the intervals between the notes.

    Args:
        notes (list[int]): a list of MIDI note numbers

    Returns:
        list[list[tuple]]: a list of potential ways to tune that note sequence
    """

from itertools import product

def generate_tunings(notes: list[int], root: int = None) -> list[list[tuple]]:
    notes.sort()  # Ensure the notes are sorted
    n = len(notes)
    tunings = []
    seen_intervals = set()

    for ref_points in product(*(range(n) for _ in range(1, n+1))):
        count = 0
        for index, ref in enumerate(ref_points):
            if count > 1:
                break
            if ref == index:
                count += 1
        if count > 1:
            continue

        tuning = []
        for index, ref in enumerate(ref_points):
            tuning.append((index, ref, (abs(notes[ref] - notes[index])) % 12))
            
        tunings.append(tuning)

        interval_signature = tuple(sorted(interval for _, _, interval in tuning))
        valid_tunings = False
        for index, ref, _ in tunings[-1]:
            if index == ref and index == root:
                valid_tunings = True
                break
        if not valid_tunings:
            tunings.pop()
        elif interval_signature not in seen_intervals:
            seen_intervals.add(interval_signature)
        else:
            tunings.pop()

    return tunings

def remove_equivalent_tunings(tunings: list[list[tuple]]) -> list[list[tuple]]:
    for tuning in tunings:
        for index, ref, interval in tuning:
            print(index, ref, interval)

def remove_harmonically_redundant_intervals(message_heap: list[list[int]]):
    """Take in a message heap and return a sorted message heap with redundant harmonies excluded 

    Args:
        message_heap (list[list[int]]): a message heap of the form [[note, instance_index, status, velocity], ...]

    Returns:
        list[list[int]]: a sorted message heap with redundant harmonies removed
    """
    
    # Sort the message heap by note (first element)
    sorted_message_heap = sorted(message_heap, key=lambda x: x[0])
    
    # To keep track of instances we've already seen
    unique_instances = set()
    
    # Final message heap with redundant harmonies removed
    harmonically_unique_message_heap = []
    
    for entry in sorted_message_heap:
        instance = entry[1]
        # Only add this entry if its instance has not been seen before
        if instance not in unique_instances:
            harmonically_unique_message_heap.append(entry)
            unique_instances.add(instance)
    
    return harmonically_unique_message_heap

if __name__ == "__main__":
    cents_offset = calculate_cents_offset_from_interval(8/7)
    pitch_wheel_value = calculate_analog_pitch_wheel_value_from_cents_offset(cents_offset=cents_offset)
    print(pitch_wheel_value)

    generate_tunings([60, 61, 62], root=0)