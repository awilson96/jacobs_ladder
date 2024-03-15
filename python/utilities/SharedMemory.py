import numpy as np

def list_of_lists_to_numpy(data):

    max_length = max(len(sublist) for sublist in data)
    result = np.zeros((len(data), max_length), dtype=int)

    for i, sublist in enumerate(data):
        result[i, :len(sublist)] = sublist
    
    return result