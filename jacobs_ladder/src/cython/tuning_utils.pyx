from itertools import product
from typing import List, Tuple
from cython cimport boundscheck, wraparound

@boundscheck(False)  # Disable bounds checking for performance
@wraparound(False)   # Disable negative index wrapping for performance
def generate_tunings(List[int] notes, int root = 0) -> List[List[Tuple[int, int, int]]]:
    notes.sort()  # Ensure the notes are sorted
    cdef int n = len(notes)
    cdef List[List[Tuple[int, int, int]]] tunings = []
    cdef set seen_intervals = set()
    
    # Declare variables before loop
    cdef int count, index, ref
    cdef List[Tuple[int, int, int]] tuning
    cdef bint valid_tunings
    cdef tuple interval_signature

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
        for index, ref, _ in tunings[len(tunings)-1]:
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
