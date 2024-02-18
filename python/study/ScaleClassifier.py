import os

import pandas as pd

from ..utilities.DataClasses import Scale
from .ScaleTree import ScaleTree

# TODO: Read in dfs to classify scales according to mode.
# TODO: Create a mechanism of rotating scales through their length to produce all possible scales, then eliminate duplicates

class ScaleClassifier:
    
    def __init__(self):
        pass
    
    def read_csv_files(self):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.csv_directory = os.path.join(self.script_directory, "possible_scales")
        
        dfs = {}
        for filename in os.listdir(self.csv_directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(self.csv_directory, filename)
                df = pd.read_csv(file_path)

                if not df.empty:
                    df_name = os.path.splitext(filename)[0]
                    dfs[df_name] = df
                    
                else:
                    os.remove(file_path)

        return dfs

if __name__ == "__main__":
    
    sc = ScaleClassifier()
    dataframes_dict = sc.read_csv_files()
    df = dataframes_dict["degree_4_interval_4_nco_0"]