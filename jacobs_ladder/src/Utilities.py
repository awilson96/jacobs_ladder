import json
import math
import os
import sys
import yaml

from itertools import product
from .Enums import NoteDivisions

def determine_octave(message_heap: list, note: int):
    """Determine if the current note is an octave of any of the currently active notes.

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

def parse_midi_controller_config(config_path: str, print_config=False) -> dict:
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
    tuning_configuration = config.get('tuning_configuration', {})
    player = tuning_configuration.get('player', 'User')
    tuning_mode = tuning_configuration.get('tuning_mode', 'none')
    tuning_config = tuning_configuration.get('tuning_config', '5-limit-ratios')
    tuning_pref = tuning_configuration.get('tuning_pref', '5-limit-pref')
    tuning = tuning_configuration.get('tuning', None)

    valid_modes = ('static', 'dynamic', 'just-intonation', 'none', None)
    if tuning_mode not in valid_modes:
        print(f"Error: Invalid tuning_mode '{tuning_mode}'. Must be one of {valid_modes}.")
        sys.exit(1)

    if tuning_mode in ('static', 'dynamic') and not tuning:
        print("Error: 'tuning_mode' is static or dynamic, but no 'tuning' provided.")
        sys.exit(1)

    formatted_tuning_config = {
        'tuning_config': {
            'player': player,
            'tuning': tuning,
            'tuning_mode': tuning_mode,
            'tuning_config': tuning_config,
            'tuning_pref': tuning_pref
        }
    }

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
        **formatted_tuning_config
    }

    if print_config:
        print("Initializing MidiController with parameters:")
        print(json.dumps(kwargs, indent=4))

    return kwargs

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
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "configuration", "yaml", "default_config.yaml")
    config = parse_midi_controller_config(config_path=path)
    print(json.dumps(config, indent=4))
    
    