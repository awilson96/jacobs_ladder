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
    """
    Generates all possible frequency ratios using only prime factors <= limit.
    max_exponent controls the range of powers used.
    Filters out ratios where floor division >= 2.
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

if __name__ == "__main__":
    # Example usage
    limit = 7
    ratios = generate_ratios(limit)
    for r in ratios:
        print(r)

    print(f"There are {len(ratios)} {limit}-limit ratios")