import os

import pandas as pd

from ..utilities.DataClasses import Scale
from .ScaleTree import ScaleTree

# TODO: Read in dfs to classify scales according to mode.
# TODO: It may make sense to make an optional argument to the Scale dataclass which is called mode to further classify the scale

class ScaleClassifier:
    
    def __init__(self):
        pass
    
    def read_csv_files(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        csv_directory = os.path.join(script_directory, "possible_scales")
        
        dfs = {}
        for filename in os.listdir(csv_directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(csv_directory, filename)
                df = pd.read_csv(file_path)

                if not df.empty:
                    df_name = os.path.splitext(filename)[0]
                    dfs[df_name] = df
                    
                else:
                    os.remove(file_path)

        return dfs.keys()

if __name__ == "__main__":
    
    sc = ScaleClassifier()
    dataframes_dict = sc.read_csv_files()
    print(dataframes_dict.__sizeof__())