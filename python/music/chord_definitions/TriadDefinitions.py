import numpy as np


# TODO: Make a method which reduces the intervals to only the unique notes
class TriadDefinitions:
    
    def __init__(self):
        self.major_triad = self.determine_valid_interval_sets(intervals=[[4, 3], [7, 9]])
        self.major_triad_1st_inv = self.determine_valid_interval_sets(intervals=[3, 5])
        self.major_triad_1st_inv_var = self.determine_valid_interval_sets(intervals=[8, 7])
        self.major_triad_2nd_inv = self.determine_valid_interval_sets(intervals=[5, 4])
        self.major_triad_2nd_inv_var = self.determine_valid_interval_sets(intervals=[9, 8])
        self.minor_triad = self.determine_valid_interval_sets(intervals=[[3, 4], [7, 8]]) 
        self.minor_triad_1st_inv = self.determine_valid_interval_sets(intervals=[4, 5]) 
        self.minor_triad_1st_inv_var = self.determine_valid_interval_sets(intervals=[9, 7]) 
        self.minor_triad_2nd_inv = self.determine_valid_interval_sets(intervals=[5, 3]) 
        self.minor_triad_2nd_inv_var = self.determine_valid_interval_sets(intervals=[8, 9]) 
        self.add2 = self.determine_valid_interval_sets(intervals=[2, 2]) 
        self.diminished = self.determine_valid_interval_sets(intervals=[[3, 3], [6, 9]]) 
        self.augmented = self.determine_valid_interval_sets(intervals=[[4, 4], [8, 8]]) 
        self.eleven_sus4 = self.determine_valid_interval_sets(intervals=[[5, 5], [10, 7]]) 
        self.sus2 = self.determine_valid_interval_sets(intervals=[2, 5]) 
        self.nine_chord = self.determine_valid_interval_sets(intervals=[7, 7]) 
        self.sus4 = self.determine_valid_interval_sets(intervals=[5, 2]) 
        self.eleven_chord = self.determine_valid_interval_sets(intervals=[7, 10]) 
        
    
    def determine_valid_interval_sets(self, intervals: list[int]):
        """Determine all of the possible triad chord types given a first and second interval

        Args:
            intervals (int): list of intervals or list of lists of intervals representing the chord you are trying to classify

        Returns:
            np.ndarray: A 2-D array representing all possible valid triads 
        """
        
        LOWEST_NOTE = 21
        
        if isinstance(intervals, list):
            if all(isinstance(item, list) for item in intervals):
                
                interval_sets = []
                
                for interval_list in intervals:
                    
                    first_interval, second_interval = interval_list
                    potential_third_interval = first_interval
                    potential_second_interval = second_interval

                    valid_first_intervals = [first_interval]
                    valid_second_intervals = [second_interval]

                    while True:
                        potential_third_interval = potential_third_interval + 12
                        if LOWEST_NOTE + potential_third_interval + second_interval <= 108:
                            valid_first_intervals.append(potential_third_interval)
                        else:
                            break
                        
                    while True:
                        potential_second_interval = potential_second_interval + 12
                        if LOWEST_NOTE + first_interval + potential_second_interval <= 108:
                            valid_second_intervals.append(potential_second_interval)
                        else:
                            break

                    valid_interval_sets = []    

                    for valid_first_interval in valid_first_intervals:
                        for valid_second_interval in valid_second_intervals:
                            if LOWEST_NOTE + valid_first_interval + valid_second_interval <= 108:
                                valid_interval_sets.append((valid_first_interval, valid_second_interval))

                    interval_sets.append(np.array(valid_interval_sets))
                
                total_interval_set = np.concatenate(interval_sets, axis=0)
                return total_interval_set
                
            else:
                first_interval, second_interval = intervals
                potential_third_interval = first_interval
                potential_second_interval = second_interval

                valid_first_intervals = [first_interval]
                valid_second_intervals = [second_interval]

                while True:
                    potential_third_interval = potential_third_interval + 12
                    if LOWEST_NOTE + potential_third_interval + second_interval <= 108:
                        valid_first_intervals.append(potential_third_interval)
                    else:
                        break
                    
                while True:
                    potential_second_interval = potential_second_interval + 12
                    if LOWEST_NOTE + first_interval + potential_second_interval <= 108:
                        valid_second_intervals.append(potential_second_interval)
                    else:
                        break

                valid_interval_sets = []    

                for valid_first_interval in valid_first_intervals:
                    for valid_second_interval in valid_second_intervals:
                        if LOWEST_NOTE + valid_first_interval + valid_second_interval <= 108:
                            valid_interval_sets.append((valid_first_interval, valid_second_interval))

                return np.array(valid_interval_sets)
        else:
            ValueError(f"Expecting type list[int] or list[list[int]]. Got type {type(intervals)}")
        
        
    
    def query(self, interval_set, valid_interval_set):
        """Check if a specific interval set is a member of the valid interval sets

        Args:
            interval_set (tuple): The interval set to check.
            valid_interval_sets (np.ndarray): 2-D array of valid interval sets.

        Returns:
            bool: True if the interval set is a member, False otherwise.
        """
        return tuple(interval_set) in map(tuple, valid_interval_set)
    
if __name__ == "__main__":
    td = TriadDefinitions()