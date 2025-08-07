import math
import sys
import yaml

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

def generate_tunings(notes: list[int], root: int = None) -> list[list[tuple]]:
    """Given a list of notes, generate all possible tunings based on the intervals between the notes.

    Args:
        notes (list[int]): a list of MIDI note numbers

    Returns:
        list[list[tuple]]: a list of potential ways to tune that note sequence
    """
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
        
        tunings_cycles_removed = remove_cycles(tunings=tunings, root=root)
        tunings_sign_editted = __edit_sign__(tunings=tunings_cycles_removed)

    return tunings_sign_editted

def parse_midi_controller_config(config_path: str) -> dict:
    """Parse the MidiController yaml config and do some light field validation

    Args:
        config_path (str): path to the yaml config

    Returns:
        dict: the kwargs used to instantiate the MidiController
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File {config_path} not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Could not parse YAML file: {e}")
        sys.exit(1)

    # --- MIDI ports ---
    input_port = config.get('input_port', 'jacobs_ladder')
    output_ports = config.get('output_ports', [f"jacobs_ladder_{i}" for i in range(12)])

    # --- Print behavior ---
    print_config = config.get('print', {})
    print_msgs = print_config.get('print_msgs', False)
    print_key = print_config.get('print_key', False)
    print_avoid_notes_only = print_config.get('print_avoid_notes_only', False)
    print_scales = print_config.get('print_scales', False)
    scale_includes = print_config.get('scale_includes', [])

    # --- Timing ---
    tempo = config.get('tempo', 120)
    time_signature = config.get('time_signature', "4/4")

    # --- Tuning ---
    tuning_mode = config.get('tuning_mode', None)
    tuning = config.get('tuning', None)

    valid_modes = ('static', 'dynamic', 'just-intonation', 'none', None)
    if tuning_mode not in valid_modes:
        print(f"Error: Invalid tuning_mode '{tuning_mode}'. Must be one of {valid_modes}.")
        sys.exit(1)

    if tuning_mode in ('static', 'dynamic') and not tuning:
        print("Error: 'tuning_mode' is static or dynamic, but no 'tuning' provided.")
        sys.exit(1)

    if tuning:
        print("Tuning settings:")
        for interval, value in tuning.items():
            print(f"  {interval:<25}: {value}")

    print(f"Tuning mode: {tuning_mode}")
    print(f"print_msgs: {print_msgs}")

    kwargs = {
        'input_port': input_port,
        'output_ports': output_ports,
        'print_msgs': print_msgs,
        'print_key': print_key,
        'print_avoid_notes_only': print_avoid_notes_only,
        'print_scales': print_scales,
        'scale_includes': scale_includes,
        'tempo': tempo,
        'time_signature': time_signature,
        'tuning_mode': tuning_mode if tuning_mode != 'none' else None,
        'tuning': tuning
    }

    return kwargs

def reaches_root(root: int, tuning: list[tuple], idx: int, visited: set) -> bool:
    """Recursive function which determines if a given tuning (list of tuples of (index, root, interval)) 
    reaches the global root or if it has a cycle. It does this by adding each parent to the visited set
    and detecting if there are cycles by ensuring that the next parent is not in the visited list, with a 
    termination condition on either reaching the root (returns True) for cycles (returns False)

    Args:
        root (int): The global root we wish to reach for each node in the graph
        tuning (list[tuple]): a list of tuples representing (index, root, interval) describing a particular 
                              tuning configuration.
        idx (int): the index of the current tuple under consideration (NOTE: a single tuple represents a single note
                   with its relationship(s) to the other notes currently being played)
        visited (set): a set of parent nodes that have already been visited when recursively searching the space

    Returns:
        bool: returns True if we reach the global root and false otherwise
    """
    # Index eventually terminates in a root
    if idx == root:
        return True
    # Cycle detected, index does not terminate in a root
    if idx in visited:
        return False  
    visited.add(idx)
    next_idx = tuning[idx][1]
    return reaches_root(root, tuning, next_idx, visited)

def remove_cycles(tunings: list[list[tuple]], root: int) -> list[list[tuple]]:
    """Remove cycles from a list of potential tunings by checking recursively to see if any tunings
    do not terminate in a root. 

    Args:
        tunings (list[list[tuple]]): A list of potential tunings for a given list of sorted notes
        root (int): the root note about which other notes should be tuned (does not need to be the lowest note)

    Returns:
        list[list[tuple]]: a list of tunings with no cyclic tunings present
    """
    valid_tunings = []
    for tuning in tunings:
        # If all of the notes are tuned in reference to another note which recursively eventually results 
        # in tuning relative to the root, then append that tuning to the list of valid tunings
        if all(reaches_root(root, tuning, i, set()) for i in range(len(tuning))):
            valid_tunings.append(tuning)

    return valid_tunings

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
    
    return 

def __edit_sign__(tunings: list[list[tuple[int]]]) -> list[tuple[int]]:
    """Takes in a list of tunings and changes the sign of the relative interval in each if it needs to be tuned down 
    relative to the root. Otherwise the relative interval in each tuning is positive.

    Args:
        tuning (list[tuple[int]]): a list of tuples representing a tuning where the tuple 
                                   represents (idx, ref, interval)

    Returns:
        list[list[tuple[int]]]: modified tunings which contain the sign associated with the relative intervals
    """
    final_result = []
    for tuning in tunings:
        result = []
        for idx, ref, interval in tuning:
            # Make sure it's negative
            if idx < ref:
                interval = -abs(interval)
            # Keep it positive
            else:
                interval = abs(interval)
            result.append((idx, ref, interval))
        final_result.append(result)
    return final_result

def get_cents_offset_from_tuning(root: int, notes: list[int], tuning: list[tuple[int]], mask: list[int]=[]) -> list[int]:
    assert len(notes) == len(tuning)
    assert root >= 0 and root < len(tuning)

    if not mask:
        mask = [1] * len(notes)
    else:
        assert len(notes) == len(mask)

    cents_offsets = []
    for relationship, msk in zip(tuning, mask):
        index, reference, relative_interval = relationship
        if msk == 0 or index == reference and relative_interval == 0:
            cents_offsets.append(0)
        else:
            cents_offsets.append(1)

    return cents_offsets

if __name__ == "__main__":
    cents_offset = calculate_cents_offset_from_interval(8/7)
    pitch_wheel_value = calculate_analog_pitch_wheel_value_from_cents_offset(cents_offset=cents_offset)
    print(pitch_wheel_value)



    tunings = []
    tunings.extend(generate_tunings([60, 64, 67], root=0))
    tunings.extend(generate_tunings([60, 64, 67], root=1))
    tunings.extend(generate_tunings([60, 64, 67], root=2))

    cents_offset = get_cents_offset_from_tuning(root=0, notes=[60, 64, 67], tuning=tunings[0])
    
    for tuning in tunings:
        print(tuning)

    print(f"tuning {tunings[0]} cents offset: {cents_offset}")

    
    