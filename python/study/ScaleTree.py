from itertools import product

import pandas as pd
import os
import shutil


class ScaleTree:
    """Create obscure scales which meet certain criterion
    """
    
    def __init__(self, scale_length: int = 12):
        self.scale_length = scale_length
        self.filepath = os.path.join(os.path.dirname(__file__), "possible_scales")
        if os.path.exists(self.filepath):
            for filename in os.listdir(self.filepath):
                if filename != ".gitignore":
                    path = os.path.join(self.filepath, filename)
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
        else:
            os.makedirs(self.filepath)
            
    def create_shifted_copies(self, row: list):
        shifted_copies = []
        for _ in range(len(row)):
            end = row.pop()
            row.insert(0, end)
            shifted_copies.append(tuple(row))
            
        shifted_copies = list(set(shifted_copies))
        shifted_copies = [list(shifted_row) for shifted_row in shifted_copies if list(shifted_row) != row]
        return shifted_copies
        
    def generate_combinations_dataframe(self, scale_degree: int, max_interval: int, max_consecutive_ones: int):
        """Generate all combinations of scales within a scale degree to some max interval size and return a dataframe.

        Args:
            scale_degree (int): Size of the scale in number of notes.
            max_interval (int): The max interval you wish to be present in the scale.

        Returns:
            pd.Dataframe: a dataframe with scales of degree scale_degree with data from 1 to max_interval whose rows must sum to 
            self.scale_length - 1.
        """
        pd.set_option("display.max_rows", None)

        column_combinations = product(range(1, max_interval + 1), repeat=scale_degree-1)
        df = pd.DataFrame(column_combinations, columns=[f'Column_{i+1}' for i in range(scale_degree-1)])
        df[f"Column_{scale_degree}"] = df.sum(axis=1)
        
        scale_len_mask = (df.iloc[:, -1] < self.scale_length)
        valid_scale_length_df = df[scale_len_mask].reset_index(drop=True)
        valid_scale_length_df.iloc[:, -1] = self.scale_length - valid_scale_length_df.iloc[:, -1]
        
        valid_max_interval_mask = (valid_scale_length_df.max(axis=1) <= max_interval)
        valid_max_interval_df = valid_scale_length_df[valid_max_interval_mask].reset_index(drop=True)
        
        valid_max_interval_list = valid_max_interval_df.values.tolist()
        valid_max_interval_list_str = [''.join(map(str, sublist)) for sublist in valid_max_interval_list]
        valid_max_interval_list_str = [s + s[0] for s in valid_max_interval_list_str]
        for scale in valid_max_interval_list_str.copy():
            counts = 0
            for i in range(len(scale)-1):
                if scale[i] == scale[i+1] and scale[i] == "1":
                    counts += 1
            if counts > max_consecutive_ones:
                valid_max_interval_list_str.remove(scale)
                
        valid_max_interval_list_str = [val[0:-1] for val in valid_max_interval_list_str]
        valid_max_interval_list_char = [list(string) for string in valid_max_interval_list_str]
        valid_max_interval_list_ints = [[int(char) for char in char_list] for char_list in valid_max_interval_list_char]
        
        
        seen = set()
        for row in valid_max_interval_list_ints.copy():
            copies = self.create_shifted_copies(row)
            if copies:
                for copy in copies:
                    if copy in valid_max_interval_list_ints:
                        if tuple(copy) not in seen:
                            valid_max_interval_list_ints.remove(copy)
                        seen.add(tuple(row))
        
        if valid_max_interval_list_ints:
            final_df = pd.DataFrame(valid_max_interval_list_ints, columns=[f"Column_{i+1}" for i in range(scale_degree)])
            return final_df
                        
        return valid_max_interval_df
    
    def generate_scales(self, max_degree: int, max_interval: int | list[int], num_consecutive_ones: int = 0, disp=False):
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
                df = self.generate_combinations_dataframe(scale_degree=degree, max_interval=max_interval, max_consecutive_ones=num_consecutive_ones)
                filepath = os.path.join(self.filepath, f"degree_{degree}_interval_{max_interval}_nco_{num_consecutive_ones}.csv")
                    
                if df.shape[0] > 0:
                    df.to_csv(filepath, ",", index=False)
                if disp: 
                    print(f"For scales of degree {degree} with max interval size {max_interval} there are {df.shape[0]} possible scales")
                
        elif type(max_interval) == list:
            for interval in max_interval:
                if disp: print()
                for degree in range(3, max_degree + 1):
                    df = self.generate_combinations_dataframe(scale_degree=degree, max_interval=interval, max_consecutive_ones=num_consecutive_ones)
                    filepath = os.path.join(self.filepath, f"degree_{degree}_interval_{interval}_nco_{num_consecutive_ones}.csv")
                    
                    if df.shape[0] > 0:
                        df.to_csv(filepath, ",", index=False)
                    if disp:
                        print(f"For scales of degree {degree} with max interval size {interval} there are {df.shape[0]} possible scales") 
        else:
            ValueError("max_interval must either be an integer or a list of integers")

if __name__ == "__main__":
    st = ScaleTree(scale_length=12)
    st.generate_scales(max_degree=8, max_interval=4, num_consecutive_ones=0, disp=True)

