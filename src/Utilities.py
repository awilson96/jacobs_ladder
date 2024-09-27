import math

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

if __name__ == "__main__":
    cents_offset = calculate_cents_offset_from_interval(8/7)
    pitch_wheel_value = calculate_analog_pitch_wheel_value_from_cents_offset(cents_offset=cents_offset)
    print(pitch_wheel_value)