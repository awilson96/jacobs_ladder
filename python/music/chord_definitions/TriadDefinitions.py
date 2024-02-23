import numpy as np


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
        self.add2_1st_inv = self.determine_valid_interval_sets(intervals=[2, 8])
        self.add2_2nd_inv = self.determine_valid_interval_sets(intervals=[8, 2])
        self.diminished = self.determine_valid_interval_sets(intervals=[[3, 3], [6, 9]]) 
        self.augmented = self.determine_valid_interval_sets(intervals=[[4, 4], [8, 8]]) 
        self.eleven_sus4 = self.determine_valid_interval_sets(intervals=[[5, 5], [10, 7]]) 
        self.sus2 = self.determine_valid_interval_sets(intervals=[2, 5]) 
        self.nine_chord = self.determine_valid_interval_sets(intervals=[7, 7]) 
        self.sus4 = self.determine_valid_interval_sets(intervals=[5, 2]) 
        self.eleven_chord = self.determine_valid_interval_sets(intervals=[7, 10]) 
        self.dominant_no_third = self.determine_valid_interval_sets(intervals=[7, 3]) 
        self.dominant_no_third_1st_inv = self.determine_valid_interval_sets(intervals=[3, 2])
        self.dominant_no_third_2nd_inv = self.determine_valid_interval_sets(intervals=[2, 7])
        self.dominant_no_fifth = self.determine_valid_interval_sets(intervals=[4, 6])
        self.dominant_no_fifth_1st_inv = self.determine_valid_interval_sets(intervals=[6, 2])
        self.dominant_no_fifth_2nd_inv = self.determine_valid_interval_sets(intervals=[2, 4])
        self.min6 = self.determine_valid_interval_sets(intervals=[3, 6])
        self.min6_1st_inv = self.determine_valid_interval_sets(intervals=[6, 3])
        self.maj7_no_third = self.determine_valid_interval_sets(intervals=[7, 4])
        self.maj7_no_third_1st_inv = self.determine_valid_interval_sets(intervals=[4, 1])
        self.maj7_no_third_2nd_inv = self.determine_valid_interval_sets(intervals=[1, 7])
        self.maj7_no_fifth = self.determine_valid_interval_sets(intervals=[[4, 7], [11, 5]])
        self.maj7_no_fifth_1st_inv = self.determine_valid_interval_sets(intervals=[7, 1])
        self.maj7_no_fifth_2nd_inv = self.determine_valid_interval_sets(intervals=[1, 4])
        self.mush = self.determine_valid_interval_sets(intervals=[[1, 1], [1, 10], [10, 1], [11, 2], [2, 11], [11, 11], [9, 4]])
        self.maj7_add2 = self.determine_valid_interval_sets(intervals=[2, 9])
        self.maj7_add2_1st_inv = self.determine_valid_interval_sets(intervals=[9, 1])
        self.maj7_add2_2nd_inv = self.determine_valid_interval_sets(intervals=[1, 2])
        self.dim_maj7_no_fifth = self.determine_valid_interval_sets(intervals=[3, 8])
        self.dim_maj7_no_fifth_1st_inv = self.determine_valid_interval_sets(intervals=[8, 1])
        self.dim_maj7_no_fifth_2nd_inv = self.determine_valid_interval_sets(intervals=[1, 3])
        self.sus_maj47 = self.determine_valid_interval_sets(intervals=[5, 6])
        self.sus_maj47_1st_inv = self.determine_valid_interval_sets(intervals=[6, 1])
        self.sus_maj47_2nd_inv = self.determine_valid_interval_sets(intervals=[1, 5])
        self.maj7_flat5 = self.determine_valid_interval_sets(intervals=[6, 5])
        self.maj7_flat5_1st_inv = self.determine_valid_interval_sets(intervals=[5, 1])
        self.maj7_flat5_2nd_inv = self.determine_valid_interval_sets(intervals=[1, 6])
        self.majmin = self.determine_valid_interval_sets(intervals=[[3, 1], [4, 11]])
        self.aug_maj7_3rd_inv_no_third = self.determine_valid_interval_sets(intervals=[1, 8])
        self.aug_maj7_no_third = self.determine_valid_interval_sets(intervals=[8, 3])
        self.sus67 = self.determine_valid_interval_sets(intervals=[9, 2])
        self.min_add2_no_fifth = self.determine_valid_interval_sets(intervals=[2, 1])
        self.min_add2_no_fifth_1st_inv = self.determine_valid_interval_sets(intervals=[1, 9])
        self.min7_no5 = self.determine_valid_interval_sets(intervals=[[3, 7], [10, 5]])
        self.sus56 = self.determine_valid_interval_sets(intervals=[[7, 2], [8, 11]])
        self.min7_no5_2nd_inv = self.determine_valid_interval_sets(intervals=[2, 3])
        self.major_flat5 = self.determine_valid_interval_sets(intervals=[4, 2])
        self.major_flat5_1st_inv = self.determine_valid_interval_sets(intervals=[2, 6])
        self.major_flat5_2nd_inv = self.determine_valid_interval_sets(intervals=[6, 4])
        self.maj79 = self.determine_valid_interval_sets(intervals=[11, 3])
        self.maj79_1st_inv = self.determine_valid_interval_sets(intervals=[3, 10])
        self.maj79_2nd_inv = self.determine_valid_interval_sets(intervals=[10, 11])
        self.maj_flat9 = self.determine_valid_interval_sets(intervals=[4, 9])
        self.maj_flat9_1st_inv = self.determine_valid_interval_sets(intervals=[9, 11])
        self.maj_flat9_2nd_inv = self.determine_valid_interval_sets(intervals=[11, 4])
        self.maj_add9 = self.determine_valid_interval_sets(intervals=[4, 10])
        self.maj_add9_1st_inv = self.determine_valid_interval_sets(intervals=[10, 10])
        self.maj_add9_2nd_inv = self.determine_valid_interval_sets(intervals=[10, 4])
        self.maj7_flat13 = self.determine_valid_interval_sets(intervals=[11, 9])
        self.sus4_flat9 = self.determine_valid_interval_sets(intervals=[5, 8])
        self.sus49 = self.determine_valid_interval_sets(intervals=[5, 9])
        self.sus49_1st_inv = self.determine_valid_interval_sets(intervals=[9, 10])
        self.min_sus4 = self.determine_valid_interval_sets(intervals=[5, 10])
        self.dominant_no_third_var = self.determine_valid_interval_sets(intervals=[10, 9])
        self.six_nine = self.determine_valid_interval_sets(intervals=[9, 5])
        self.maj7_no_third_var = self.determine_valid_interval_sets(intervals=[11, 8])
        self.maj7_no_third_var_1st_inv = self.determine_valid_interval_sets(intervals=[8, 5])
        self.maj7_no_third_var_2nd_inv = self.determine_valid_interval_sets(intervals=[5, 11])
        self.sharp11_no_third = self.determine_valid_interval_sets(intervals=[7, 11])
        self.sharp11_no_third_1st_inv = self.determine_valid_interval_sets(intervals=[11, 6])
        self.sharp11_no_third_2nd_inv = self.determine_valid_interval_sets(intervals=[6, 7])
        self.dominant_no_fifth_var = self.determine_valid_interval_sets(intervals=[10, 6])
        self.dominant_no_fifth_var_1st_inv = self.determine_valid_interval_sets(intervals=[6, 8])
        self.dominant_no_fifth_var_2nd_inv = self.determine_valid_interval_sets(intervals=[8, 10])
        self.maj_flat5_var = self.determine_valid_interval_sets(intervals=[6, 10])
        self.maj_flat5_var_1st_inv = self.determine_valid_interval_sets(intervals=[10, 8])
        self.maj_flat5_var_2nd_inv = self.determine_valid_interval_sets(intervals=[8, 6])
        self.maj7_flat5_var = self.determine_valid_interval_sets(intervals=[11, 7])
        self.maj7_flat5_var_1st_inv = self.determine_valid_interval_sets(intervals=[7, 6])
        self.maj7_flat5_var_2nd_inv = self.determine_valid_interval_sets(intervals=[6, 11])
        self.min6_var = self.determine_valid_interval_sets(intervals=[9, 6])
        self.min6_var_2nd_inv = self.determine_valid_interval_sets(intervals=[9, 9])
        self.min9_no5 = self.determine_valid_interval_sets(intervals=[3, 11])
        self.min9_no5_1st_inv = self.determine_valid_interval_sets(intervals=[11, 10])
        self.min9_no5_2nd_inv = self.determine_valid_interval_sets(intervals=[10, 3])
        

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
        mask = np.all(valid_interval_set == np.array(interval_set), axis=1)
        return np.any(mask)
    
if __name__ == "__main__":
    td = TriadDefinitions()