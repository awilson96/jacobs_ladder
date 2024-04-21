import os

import pandas as pd

from ..utilities.DataClasses import Scale
from .ScaleTree import ScaleTree

# TODO: Read in dfs to classify scales according to mode.
# TODO: Create a mechanism of rotating scales through their length to produce all possible scales, then eliminate duplicates

class ScaleClassifier:
    
    def __init__(self):
        self.df_dict = self.read_csv_files()
    
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
    
    def convert_intervals(self, starting_note: int):
        scale_list = []
        for df_name, df in self.df_dict.items():
            for index, row in df.iterrows():
                remainder = list(map(lambda x: x + starting_note, list(row.cumsum())))
                scale = [starting_note]
                scale.extend(remainder)
                scale_list.append(scale)
                
        return scale_list
    
    def create_harmonized_scale(self, scale: list, num_voices: int):
        starting_note = scale[0]
        scale_original = scale.copy()
        scale_pattern = [note - starting_note for note in scale]
        extension = [scale[-1] + note for note in scale_pattern]
        scale.extend(extension[1:])
        
        chord_scale = []
        for index in range(len(scale_original)):
            chord = []
            for num_voc in range(0, int(num_voices)*2, 2):
                chord.append(scale[index+num_voc])
            chord_scale.append(chord)
            
        return chord_scale

if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    sc = ScaleClassifier()
    scales = sc.convert_intervals(starting_note=60)
    my_scale = scales[0]
    chord_scale = sc.create_harmonized_scale(scale=my_scale, num_voices=3)
    print(chord_scale)