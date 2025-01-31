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
    cdef bint valid_tuning
    cdef tuple interval_signature

    # Helper function for DFS traversal
    def dfs(v, graph, visited):
        visited[v] = True
        for u in graph[v]:
            if not visited[u]:
                dfs(u, graph, visited)

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
        graph = [[] for _ in range(n)]  # Graph to store connections
        for index, ref in enumerate(ref_points):
            tuning.append((index, ref, (abs(notes[ref] - notes[index])) % 12))
            # Build the graph of connections
            graph[index].append(ref)
            graph[ref].append(index)

        # Interval signature and validity check
        interval_signature = tuple(sorted(interval for _, _, interval in tuning))
        valid_tuning = False
        for index, ref, _ in tuning:
            if index == root and ref == root:
                valid_tuning = True
                break
        
        if not valid_tuning:
            continue  # Skip this tuning if the root is not present

        # Perform DFS to check if all nodes are connected to the root
        visited = [False] * n
        dfs(root, graph, visited)
        
        # Ensure all notes are connected to the root
        if not all(visited):
            continue  # Skip this tuning if any note is not connected to the root

        # Add the tuning if it's valid and the interval signature hasn't been seen
        if interval_signature not in seen_intervals:
            seen_intervals.add(interval_signature)
            tunings.append(tuning)

    return tunings
