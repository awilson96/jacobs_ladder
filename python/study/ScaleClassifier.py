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
        # Get the directory of the script using __file__
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the CSV files directory
        csv_directory = os.path.join(script_directory, "possible_scales")

        # Initialize an empty dictionary to store dataframes
        dfs = {}

        # Loop through all files in the directory
        for filename in os.listdir(csv_directory):
            if filename.endswith(".csv"):
                # Construct the full path to the CSV file
                file_path = os.path.join(csv_directory, filename)

                # Read the CSV file into a dataframe
                df = pd.read_csv(file_path)

                # Check if the dataframe has any data
                if not df.empty:
                    # Remove the file extension to get the dataframe name
                    df_name = os.path.splitext(filename)[0]

                    # Add the dataframe to the dictionary
                    dfs[df_name] = df

        return dfs.keys()

if __name__ == "__main__":
    
    sc = ScaleClassifier()
    dataframes_dict = sc.read_csv_files()
    print(dataframes_dict.__sizeof__())