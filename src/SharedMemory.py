import numpy as np

def list_of_lists_to_numpy(data):
    """Convert a list of lists to a numpy 2d array for the purpose of sharing messages using a shared memory buffer 

    Args:
        data (list[list]): raw data representing messages

    Returns:
        np.array: a 2D array representing the messages 
    """
    max_length = max(len(sublist) for sublist in data)
    result = np.zeros((len(data), max_length), dtype=int)

    for i, sublist in enumerate(data):
        result[i, :len(sublist)] = sublist
    
    return result