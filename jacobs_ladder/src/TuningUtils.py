from itertools import product
from fractions import Fraction

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
            interval_list.append(get_interval_from_ratio(ratio=rat))
        return interval_list

    elif isinstance(ratio, Fraction):
        return get_interval_from_ratio(ratio=ratio)
    else:
        return TypeError("Unknown ratio data type. Expected either a Fration of list[Fraction]")
    
def get_interval_from_ratio(ratio: Fraction) -> int:
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

if __name__ == "__main__":
    # Example usage
    limit = 7
    ratios = generate_ratios(limit)
    for r in ratios:
        print(r)

    intervals = determine_interval_based_on_ratio(ratio=ratios)

    for interval, ratio in zip(intervals, ratios):
        print(f"Ratio: {ratio} Interval: {interval}")

    print(f"There are {len(ratios)} {limit}-limit ratios")