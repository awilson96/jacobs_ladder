import json
import math
import os

from itertools import product
from fractions import Fraction

def __calculate_cents_from_interval__(interval: float):
    return math.log2(interval) * 1200

def calculate_cents_offset_from_interval(interval: float):
    cents = __calculate_cents_from_interval__(interval=interval)
    nearest_interval_cents_value = round(cents, -2)
    return cents - nearest_interval_cents_value

def calculate_analog_pitch_wheel_value_from_cents_offset(cents_offset: float):
    return int(round(cents_offset * 8192 / 200 + 8192, 0))

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

def prime_factors(n):
    """Returns the prime factors of n as a set."""
    i = 2
    factors = set()
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.add(i)
    if n > 1:
        factors.add(n)
    return factors

def generate_ratios(limit, max_exponent=2):
    """Generates all possible frequency ratios using only prime factors <= limit. max_exponent controls the range 
    of powers used. Filters out ratios where floor division >= 2.
    """
    primes = [p for p in range(2, limit + 1) if len(prime_factors(p)) == 1]
    
    # Generate all possible products of primes up to max_exponent
    numerators = set()
    for exponents in product(range(max_exponent + 1), repeat=len(primes)):
        num = 1
        for base, exp in zip(primes, exponents):
            num *= base ** exp
        numerators.add(num)
    
    # Generate ratios as fractions and filter based on floor division
    ratios = {Fraction(n, d) for n in numerators for d in numerators if n >= d and (n // d) < 2 and n < 1000}
    ratios.discard(Fraction(1, 1))

    return sorted(ratios)

def determine_interval_based_on_ratio(ratio: Fraction | list[Fraction]) -> int | list[int]:
    """Determine the interval based on a fractional value between 0-2 inclusive. Returns a single interval if a
    single Fraction is entered as input and returns a list of intervals if a list of Fractions are provided.

    Args:
        ratio (Fraction | list[Fraction]): A Fraction or list of Fractions whose decimal value evaluates to a
                                           number between 0 and 2 inclusive

    Returns:
        float | list[float]: a single interval or list of intervals between -12 and 12 inclusive
    """
    if isinstance(ratio, list):
        interval_list = []
        for rat in ratio:
            interval_list.append(__get_interval_from_ratio__(ratio=rat))
        return interval_list

    elif isinstance(ratio, Fraction):
        return __get_interval_from_ratio__(ratio=ratio)
    else:
        return TypeError("Unknown ratio data type. Expected either a Fration of list[Fraction]")
    
def __get_interval_from_ratio__(ratio: Fraction) -> int:
    """Given a ratio as a Fraction in the range from 0-2 inclusive, determine the interval from -12 to 12 inclusive 
    assuming that all intervals surpassing the plus or minus 1 octave boundary are mapped to intervals within the 
    boundary (i.e. a major 10th is mapped to a major 3rd).

    Args:
        ratio (Fraction): A fraction whose decimal value evaluates to a number between 0 and 2

    Returns:
        int: an interval between -12 and 12 inclusive
    """
    # Convert the fraction to a decimal value
    ratio_float = float(ratio)
    
    # Compute frequency ratios for semitones 1 through 11 and
    up_ratios = [1.0] + [2 ** (n / 12) for n in range(1, 12)] + [2.0]
    down_ratios = [1.0] + [2 ** (-n / 12) for n in range(1, 12)] + [0.0]
    direction = None

    # Choose the correct set of boundaries
    if ratio_float >= 1:
        ratios = up_ratios
        direction = 1
    else:
        ratios = down_ratios
        direction = -1

    # If we are ascending in interval relative to the base tone
    if direction == 1:
        # Range is from 1 to 10 inclusive since we are using index plus 1 logic to compare ratio at i against 
        # the ratio at i + 1
        for i in range(11):
            if ratios[i] <= ratio_float < ratios[i + 1]:
                # If the ratio is closer to the ith element than the ith plus 1 element chose the ith interval
                if ratio_float - ratios[i] < ratios[i + 1] - ratio_float:
                    return direction * i
                # Otherwise chose the ith plus 1 interval
                else:
                    return direction * (i + 1)
        # If the ratio is not in the interval range assume an octave relationship since this function is
        # only ever supposed to be used in the range of plus or minus 1 octave
        return 12
    # If we are descending in interval relative to the base tone
    else:
        # Range is from 1 to 10 inclusive since we are using index plus 1 logic to compare ratio at i against 
        # the ratio at i + 1
        for i in range(11):
            if ratios[i + 1] <= ratio_float < ratios[i]:
                # Note that since ratios are descending from index 0 to index 11 the inequality is reversed
                # when compared to the if direction == 1 case. If the ratio is closer to the i + 1 element
                # then chose the ith plus 1 element as the interval
                if ratio_float - ratios[i + 1] < ratios[i] - ratio_float:
                    return direction * (i + 1)
                # Otherwise chose the ith element as the interval
                else:
                    return direction * i
        # If the ratio is not in the interval range assume an octave relationship since this function is
        # only ever supposed to be used in the range of plus or minus 1 octave
        return -12
    
def create_tuning_config(ratios: list[Fraction], intervals: list[int], name: str) -> None:
    """Create a tuning config for a list of n-limit just intonation intervals ordered by interval. The config is
    of the form {interval: [ratio: {cents offset: <val>, analog pitch value offset: <val>}]}.

    Args:
        ratios (list[Fraction]): a list of Fractions between 1 and 2 representing n-limit JI musical intervals
        intervals (list[int]): a list of positive or negative  interval values (measured in half steps)
        name (str): a name for the output json file (do not include the extension)
    """
    assert ".json" not in name
    tuning_config = {}
    for ratio, interval in zip(ratios, intervals):
        if interval not in tuning_config.keys():
            tuning_config[interval] = []
        if "-"+ str(interval) not in tuning_config.keys():
            tuning_config["-" + str(interval)] = []
        cents_offset = calculate_cents_offset_from_interval(float(ratio))
        cents_offset_inverse = calculate_cents_offset_from_interval(float(ratio.denominator / ratio.numerator))
        analog_pitch_wheel_value_offset = calculate_analog_pitch_wheel_value_from_cents_offset(cents_offset) - 8192
        analog_pitch_wheel_value_offset_inverse = calculate_analog_pitch_wheel_value_from_cents_offset(cents_offset_inverse) - 8192
        positive_ratio = f"{ratio.numerator}/{ratio.denominator}"
        negative_ratio = f"{ratio.denominator}/{ratio.numerator}"
        postive_metadata = {positive_ratio: {"cents offset": round(cents_offset, 3), 
                                             "analog pitch wheel value offset": analog_pitch_wheel_value_offset}}
        negative_metadata = {negative_ratio: {"cents offset": round(cents_offset_inverse, 3), 
                                              "analog pitch wheel value offset": analog_pitch_wheel_value_offset_inverse}}
        tuning_config[interval].append(postive_metadata)
        tuning_config["-" + str(interval)].append(negative_metadata)

    filename = os.path.join("jacobs_ladder", "configuration", "json", "pitch", f"{name}.json")
    with open(filename, "w") as json_file:
        json.dump(tuning_config, json_file, indent=4)

    print(f"Writing tuning configuration \"{filename}\"")

def read_tuning_config(name: str) -> dict:
    """Read an  n-limit tuning config 

    Args:
        name (str): The name of the tuning config (do not include the extension)

    Returns:
        dict: a dictionary representing the json config
    """
    filename = os.path.join("jacobs_ladder", "configuration", "json", "pitch", f"{name}.json") 
    with open(filename, "r") as json_file:
        tuning_config = json.load(json_file)
    return tuning_config

if __name__ == "__main__":
    # Example usage
    limit = 7
    ratios = generate_ratios(limit)
    intervals = determine_interval_based_on_ratio(ratio=ratios)
    print(f"There are {len(ratios)} {limit}-limit ratios")
    create_tuning_config(ratios=ratios, intervals=intervals, name="7-limit-ratios")

    cents_offset = calculate_cents_offset_from_interval(8/7)
    pitch_wheel_value = calculate_analog_pitch_wheel_value_from_cents_offset(cents_offset=cents_offset)
    print(pitch_wheel_value)

    tunings = []
    tunings.extend(generate_tunings([60, 64, 67], root=0))
    tunings.extend(generate_tunings([60, 64, 67], root=1))
    tunings.extend(generate_tunings([60, 64, 67], root=2))

    tuning_config = read_tuning_config(name="5-limit-ratios")