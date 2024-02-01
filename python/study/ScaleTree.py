from itertools import product

import pandas as pd
import os


class ScaleTree:
    """Create obscure scales which meet certain criterion
    """
    
    def __init__(self, scale_length: int = 12):
        self.scale_length = scale_length
        self.filepath = os.path.join(os.path.dirname(__file__), "possible_scales")
        
    def generate_combinations_dataframe(self, scale_degree: int, max_interval: int):
        """Generate all combinations of scales within a scale degree to some max interval size and return a dataframe.

        Args:
            scale_degree (int): Size of the scale in number of notes.
            max_interval (int): The max interval you wish to be present in the scale.

        Returns:
            pd.Dataframe: a dataframe with scales of degree scale_degree with data from 1 to max_interval whose rows must sum to 
            self.scale_length - 1.
        """

        column_combinations = product(range(1, max_interval + 1), repeat=scale_degree-1)
        df = pd.DataFrame(column_combinations, columns=[f'Column_{i+1}' for i in range(scale_degree-1)])
        
        mask = (df.sum(axis=1) < self.scale_length)
        valid_combinations_df = df[mask]

        return valid_combinations_df
    
    def generate_scales(self, max_degree: int, max_interval: int | list[int], num_consecutive_ones: None | int = None, disp=False):
        """Given a max degree, and a max interval list all possible scales from degree 2 to max degree with interval
        sizes which range from 1 to max interval. Optionally display the number of rows as output by setting disp to True.
        Output is piped to named csv files in the ~/Jacobs-Ladder/python/study/possible_scales directory.

        Args:
            max_degree (int): The max number of notes in the scale you want to generate csv files for
            max_interval (int | list[int]): The largest interval you would ever want in your scale.
            disp (bool, optional): If true display ouput otherwise don't. Defaults to False.
        """
        
        if max_degree < 2 or max_degree > 24:
            ValueError("Valid range for max_degree is 2-24")
            
        if type(max_interval) == int:
            for degree in range(2, max_degree + 1):
                df = self.generate_combinations_dataframe(scale_degree=degree, max_interval=max_interval)
                
                if num_consecutive_ones is not None:
                    # Create a mask to exclude rows with more than num_consecutive_ones consecutive ones while accounting for wrap-around effect
                    consecutive_ones_mask = df.apply(lambda row: (sum('11' in ''.join(map(str, row[i:i+2])) 
                                                     for i in range(len(row)-1))) <= num_consecutive_ones, axis=1)
                    df = df[consecutive_ones_mask].reset_index(drop=True)
                    
                df.to_csv(f"./possible_scales/md_2-{degree}_mi_1-{max_interval}_nco_{num_consecutive_ones}.csv", ",", index=False)
                if disp: 
                    print(f"For scales of degree {degree} with max interval size {max_interval} there are {df.shape[0]} possible scales")
                
        elif type(max_interval) == list:
            for interval in max_interval:
                if disp: print()
                for degree in range(3, max_degree + 1):
                    df = self.generate_combinations_dataframe(scale_degree=degree, max_interval=interval)
                    
                    if num_consecutive_ones is not None:
                        consecutive_ones_mask = df.apply(lambda row: (sum('11' in ''.join(map(str, row[i:i+2])) 
                                                         for i in range(len(row)-1))) <= num_consecutive_ones, axis=1)
                        wrap_around_mask = df.apply(lambda row: sum(row) == self.scale_length-1 and row[0] == 1, axis=1)
                        wrap_around_mask2 = df.apply(lambda row: sum(row) == self.scale_length-1 and row[-1] == 1, axis=1)
                        max_interval_mask = df.apply(lambda row: self.scale_length - sum(row) > interval, axis=1) 
                        
                        
                        mask = consecutive_ones_mask & ~wrap_around_mask & ~wrap_around_mask2 & ~max_interval_mask
                        df = df.loc[mask]
                    
                    filepath = os.path.join(self.filepath, f"degree_{degree}_interval_{interval}_nco_{num_consecutive_ones}.csv")
                    df.to_csv(filepath, ",", index=False)
                    if disp:
                        print(f"For scales of degree {degree} with max interval size {interval} there are {df.shape[0]} possible scales") 
        else:
            ValueError("max_interval must either be an integer or a list of integers")

if __name__ == "__main__":
    
    st = ScaleTree(scale_length=12)
    st.generate_scales(max_degree=8, max_interval=[2, 3, 4, 5, 6], num_consecutive_ones=2, disp=True)

    

