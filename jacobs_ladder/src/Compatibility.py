import os
import pandas as pd
from .Dictionaries import get_midi_notes

class Compatibility:
    def __init__(self):
        degree8_file_path = os.path.join(os.path.dirname(__file__), 'possible_scales', 'degree_8_interval_9_nco_1.csv')
        self.degree8_data = pd.read_csv(degree8_file_path)
        degree7_file_path = os.path.join(os.path.dirname(__file__), 'possible_scales', 'degree_7_interval_9_nco_1.csv')
        self.degree7_data = pd.read_csv(degree7_file_path)
        degree6_file_path = os.path.join(os.path.dirname(__file__), 'possible_scales', 'degree_6_interval_9_nco_1.csv')
        self.degree6_data = pd.read_csv(degree6_file_path)
        degree5_file_path = os.path.join(os.path.dirname(__file__), 'possible_scales', 'degree_5_interval_9_nco_1.csv')
        self.degree5_data = pd.read_csv(degree5_file_path)
        degree4_file_path = os.path.join(os.path.dirname(__file__), 'possible_scales', 'degree_4_interval_9_nco_1.csv')
        self.degree4_data = pd.read_csv(degree4_file_path)
        degree3_file_path = os.path.join(os.path.dirname(__file__), 'possible_scales', 'degree_3_interval_9_nco_1.csv')
        self.degree3_data = pd.read_csv(degree3_file_path)
        self.int_note = get_midi_notes()

        self.ocatonic_scales = None
        self.ocatonic_scales_named = None
        self.heptatonic_scales = None
        self.heptatonic_scales_named = None
        self.hexatonic_scales = None
        self.hexatonic_scales_named = None
        self.pentatonic_scales = None
        self.pentatonic_scales_named = None
        self.tetrads = None
        self.tetrads_named = None
        self.triads = None
        self.triads_named = None

    def create_scale(self, starting_note: int, data: pd.DataFrame) -> None:
        """Create scales from the intervals in the data given a starting note and assign to appropriate class variables.

        Args:
            starting_note (int): the starting note of the scale
            data (pd.DataFrame): a DataFrame containing interval data for creating scales
        """
        scales = []
        names = []

        for _, row in data.iterrows():
            # Convert the row to a list of intervals
            intervals = row.values
            # Calculate the scale by taking the cumulative sum of intervals and adding starting note
            scale = [starting_note + sum(intervals[:i + 1]) for i in range(len(intervals))]
            scales.append(scale)
            # Generate the name string by concatenating interval values
            names.append("".join(map(str, intervals)))

        # Convert the resulting scales into a DataFrame
        result_df = pd.DataFrame(scales, columns=[f"Note_{i + 1}" for i in range(data.shape[1])])

        # Insert the starting note column as Note_0
        result_df.insert(0, 'Note_0', starting_note)

        # Drop the last column dynamically
        result_df = result_df.iloc[:, :-1]

        # Add the name column
        result_df['name'] = names

        # Check the number of columns and assign to the appropriate class variable
        num_columns = result_df.shape[1] - 1  # Exclude 'name' column
        if num_columns == 8:
            self.ocatonic_scales = result_df
            # print(f"Octatonic Scales:\n{self.ocatonic_scales}")
        if num_columns == 7:
            self.heptatonic_scales = result_df
            # print(f"Heptatonic Scales:\n{self.heptatonic_scales}")
        elif num_columns == 6:
            self.hexatonic_scales = result_df
            # print(f"Hexatonic Scales:\n{self.hexatonic_scales}")
        if num_columns == 5:
            self.pentatonic_scales = result_df
            # print(f"Pentatonic Scales:\n{self.pentatonic_scales}")
        elif num_columns == 4:
            self.tetrads = result_df
            # print(f"Tetrads:\n{self.tetrads}")
        elif num_columns == 3:
            self.triads = result_df
            # print(f"Triads:\n{self.triads}")

        
    def create_named_scale(self):
        """Convert scales in integer form to named scales using MIDI note mapping."""
        if self.ocatonic_scales is not None:
            self.ocatonic_scales_named = self.ocatonic_scales.copy()
            self.ocatonic_scales_named = self.ocatonic_scales_named.replace(self.int_note)
            # Add 'name' field by concatenating the note names (except for the last column)
            self.ocatonic_scales_named['name'] = self.ocatonic_scales_named.apply(
                lambda row: "".join([self.int_note.get(note, str(note)) for note in row[:-1]]), axis=1)
            # print(f"Octatonic Scales Named:\n{self.ocatonic_scales_named}")

        if self.heptatonic_scales is not None:
            self.heptatonic_scales_named = self.heptatonic_scales.copy()
            self.heptatonic_scales_named = self.heptatonic_scales_named.replace(self.int_note)
            # Add 'name' field by concatenating the note names (except for the last column)
            self.heptatonic_scales_named['name'] = self.heptatonic_scales_named.apply(
                lambda row: "".join([self.int_note.get(note, str(note)) for note in row[:-1]]), axis=1)
            # print(f"Heptatonic Scales Named:\n{self.heptatonic_scales_named}")

        if self.hexatonic_scales is not None:
            self.hexatonic_scales_named = self.hexatonic_scales.copy()
            self.hexatonic_scales_named = self.hexatonic_scales_named.replace(self.int_note)
            # Add 'name' field by concatenating the note names (except for the last column)
            self.hexatonic_scales_named['name'] = self.hexatonic_scales_named.apply(
                lambda row: "".join([self.int_note.get(note, str(note)) for note in row[:-1]]), axis=1)
            # print(f"Hexatonic Scales Named:\n{self.hexatonic_scales_named}")

        if self.pentatonic_scales is not None:
            self.pentatonic_scales_named = self.pentatonic_scales.copy()
            self.pentatonic_scales_named = self.pentatonic_scales_named.replace(self.int_note)
            # Add 'name' field by concatenating the note names (except for the last column)
            self.pentatonic_scales_named['name'] = self.pentatonic_scales_named.apply(
                lambda row: "".join([self.int_note.get(note, str(note)) for note in row[:-1]]), axis=1)
            # print(f"Pentatonic Scales Named:\n{self.pentatonic_scales_named}")

        if self.tetrads is not None:
            self.tetrads_named = self.tetrads.copy()
            self.tetrads_named = self.tetrads_named.replace(self.int_note)
            # Add 'name' field by concatenating the note names (except for the last column)
            self.tetrads_named['name'] = self.tetrads_named.apply(
                lambda row: "".join([self.int_note.get(note, str(note)) for note in row[:-1]]), axis=1)
            # print(f"Tetrads Named:\n{self.tetrads_named}")

        if self.triads is not None:
            self.triads_named = self.triads.copy()
            self.triads_named = self.triads_named.replace(self.int_note)
            # Add 'name' field by concatenating the note names (except for the last column)
            self.triads_named['name'] = self.triads_named.apply(
                lambda row: "".join([self.int_note.get(note, str(note)) for note in row[:-1]]), axis=1)
            # print(f"Triads Named:\n{self.triads_named}")

    def remove_rotated_duplicates(self, dfs):
        """Removes rows from dataframes that are rearranged versions of rows in other dataframes.
        
        Parameters:
            dfs (list of pd.DataFrame): List of dataframes to process. Each dataframe must
                                        have a "name" column and note columns (e.g., Note_0, Note_1, ...).
        
        Returns:
            list of pd.DataFrame: Dataframes with rearranged duplicates removed.
        """
        # Create a set to track unique normalized rows
        unique_rows = set()
        result_dfs = []
        
        for df in dfs:
            # Get only the note columns (exclude the "name" column)
            note_columns = df.columns[:-1]
            
            # Normalize rows by sorting the note values
            normalized_rows = df[note_columns].apply(lambda row: tuple(sorted(row)), axis=1)
            
            # Identify rows that are not duplicates
            non_duplicate_indices = [
                i for i, row in enumerate(normalized_rows) if row not in unique_rows
            ]
            
            # Add new unique rows to the set
            unique_rows.update(normalized_rows.iloc[non_duplicate_indices])
            
            # Filter the dataframe to keep only non-duplicate rows
            result_dfs.append(df.iloc[non_duplicate_indices].reset_index(drop=True))
        
        return result_dfs


    def determine_compatibility(self, scales_df, higher_degree_dfs, include_weak=False):
        """Determine compatible scales for a given scale in the provided DataFrame.
        Compatibility is based on whether all notes in the lower degree scale
        are contained within a higher degree scale from any of the DataFrames
        in the higher_degree_dfs list.

        Args:
            scales_df (pd.DataFrame): A DataFrame containing named lower degree scales to check compatibility.
            higher_degree_dfs (list of pd.DataFrame): A list of DataFrames containing named higher degree scales to compare against.
            include_weak (bool): If True, include weak compatibility scales (scales with only one missing note).
        
        Returns:
            dict: A dictionary where keys are scale names and values are lists of compatible scale names.
        """
        compatibility_dict = {}

        # Iterate over all the lower degree scales in the DataFrame
        for _, row in scales_df.iterrows():
            current_scale_notes = set(row[:-1])  # Get all note columns except 'name'
            current_scale_name = row['name']     # Get scale name

            # Initialize a list to hold compatible scales for the current scale
            compatible_scales = []

            # Compare with all higher degree scales from each DataFrame in higher_degree_dfs
            for higher_degree_df in higher_degree_dfs:
                for _, other_row in higher_degree_df.iterrows():
                    # Get the notes of the higher degree scale
                    other_scale_notes = set(other_row[:-1])  # Get all note columns except 'name'

                    print(f"{current_scale_notes}: {other_scale_notes}")

                    # Determine compatibility
                    if self.is_subset(current_scale_notes, other_scale_notes):
                        # If all notes of the current scale are contained in the higher scale (order doesn't matter)
                        compatible_scales.append(other_row['name'])
                    elif len(current_scale_notes - other_scale_notes) == 1 and include_weak:
                        # If all but 1 note of the current scale are contained in the higher scale, it's weak compatibility
                        compatible_scales.append(f"{other_row['name']}_weak")

            # Only add to dictionary if there are compatible scales
            if compatible_scales:
                compatibility_dict[current_scale_name] = compatible_scales

        for scale, compatibles in compatibility_dict.items():
            print(f"{scale}: {compatibles}\n")

        return compatibility_dict
    
    def determine_compatibility(self, scales_dict, higher_degree_dfs, include_weak=False):
        """
        Determine compatible scales for a given scale using a dictionary of lower degree scales.
        Compatibility is based on whether all notes in the lower degree scale
        are contained within a higher degree scale from any of the DataFrames
        in the higher_degree_dfs list.

        Args:
            scales_dict (dict): A dictionary where keys are scale names and values are lists of notes (e.g., {name: [A, B, C, D]}).
            higher_degree_dfs (list of pd.DataFrame): A list of DataFrames containing named higher degree scales to compare against.
            include_weak (bool): If True, include weak compatibility scales (scales with only one missing note).
        
        Returns:
            dict: A dictionary where keys are scale names and values are lists of compatible scale names.
        """
        compatibility_dict = {}

        # Iterate over all the scales in the dictionary
        for current_scale_name, current_scale_notes in scales_dict.items():
            current_scale_notes = set(current_scale_notes)  # Convert the list of notes to a set

            # Initialize a list to hold compatible scales for the current scale
            compatible_scales = []

            # Compare with all higher degree scales from each DataFrame in higher_degree_dfs
            for higher_degree_df in higher_degree_dfs:
                for _, other_row in higher_degree_df.iterrows():
                    # Get the notes of the higher degree scale
                    other_scale_notes = set(other_row[:-1])  # Get all note columns except 'name'

                    # Determine compatibility
                    if self.is_subset(current_scale_notes, other_scale_notes):
                        # If all notes of the current scale are contained in the higher scale (order doesn't matter)
                        compatible_scales.append(other_row['name'])
                    elif len(current_scale_notes - other_scale_notes) == 1 and include_weak:
                        # If all but 1 note of the current scale are contained in the higher scale, it's weak compatibility
                        compatible_scales.append(f"{other_row['name']}_weak")

            # Only add to dictionary if there are compatible scales
            if compatible_scales:
                compatibility_dict[current_scale_name] = compatible_scales

        return compatibility_dict


    def is_subset(self, current_scale_notes, other_scale_notes):
        """
        Check if all notes of current_scale_notes are contained in other_scale_notes (order doesn't matter).
        """
        return current_scale_notes.issubset(other_scale_notes)
    
    def reorder_chords(self, chord_dict):
        # Define valid characters for sorting
        valid_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 
                    'A♭', 'B♭', 'D♭', 'E♭', 'G♭']

        # Helper function to find and reorder a string
        def reorder_string(chord, start):
            # Find the starting substring in the chord
            for char in valid_chars:
                if chord.startswith(start + char):
                    return chord
            # If not found, find the starting note elsewhere in the string
            idx = chord.find(start)
            if idx != -1:
                return chord[idx:] + chord[:idx]
            return chord  # If no match, return as is

        # Iterate through the dictionary and process each key and list
        result_dict = {}
        for key, chords in chord_dict.items():
            start_note = key.split()[0]  # Extract the starting note (first part of the key)
            sorted_chords = [reorder_string(chord, start_note) for chord in chords]
            result_dict[key] = sorted_chords

        return result_dict


if __name__ == "__main__":
    C_compatibility = Compatibility()
    Db_compatibility = Compatibility()
    D_compatibility = Compatibility()
    Eb_compatibility = Compatibility()
    E_compatibility = Compatibility()
    F_compatibility = Compatibility()
    Gb_compatibility = Compatibility()
    G_compatibility = Compatibility()
    Ab_compatibility = Compatibility()
    A_compatibility = Compatibility()
    Bb_compatibility = Compatibility()
    B_compatibility = Compatibility()

    C_compatibility.create_scale(starting_note=60, data=C_compatibility.degree8_data)
    C_compatibility.create_scale(starting_note=60, data=C_compatibility.degree7_data)
    C_compatibility.create_scale(starting_note=60, data=C_compatibility.degree6_data)
    C_compatibility.create_scale(starting_note=60, data=C_compatibility.degree5_data)
    C_compatibility.create_scale(starting_note=60, data=C_compatibility.degree4_data)
    C_compatibility.create_scale(starting_note=60, data=C_compatibility.degree3_data)
    C_compatibility.create_named_scale()

    Db_compatibility.create_scale(starting_note=61, data=Db_compatibility.degree8_data)
    Db_compatibility.create_scale(starting_note=61, data=Db_compatibility.degree7_data)
    Db_compatibility.create_scale(starting_note=61, data=Db_compatibility.degree6_data)
    Db_compatibility.create_scale(starting_note=61, data=Db_compatibility.degree5_data)
    Db_compatibility.create_scale(starting_note=61, data=Db_compatibility.degree4_data)
    Db_compatibility.create_scale(starting_note=61, data=Db_compatibility.degree3_data)
    Db_compatibility.create_named_scale()

    D_compatibility.create_scale(starting_note=62, data=D_compatibility.degree8_data)
    D_compatibility.create_scale(starting_note=62, data=D_compatibility.degree7_data)
    D_compatibility.create_scale(starting_note=62, data=D_compatibility.degree6_data)
    D_compatibility.create_scale(starting_note=62, data=D_compatibility.degree5_data)
    D_compatibility.create_scale(starting_note=62, data=D_compatibility.degree4_data)
    D_compatibility.create_scale(starting_note=62, data=D_compatibility.degree3_data)
    D_compatibility.create_named_scale()

    Eb_compatibility.create_scale(starting_note=63, data=Eb_compatibility.degree8_data)
    Eb_compatibility.create_scale(starting_note=63, data=Eb_compatibility.degree7_data)
    Eb_compatibility.create_scale(starting_note=63, data=Eb_compatibility.degree6_data)
    Eb_compatibility.create_scale(starting_note=63, data=Eb_compatibility.degree5_data)
    Eb_compatibility.create_scale(starting_note=63, data=Eb_compatibility.degree4_data)
    Eb_compatibility.create_scale(starting_note=63, data=Eb_compatibility.degree3_data)
    Eb_compatibility.create_named_scale()

    E_compatibility.create_scale(starting_note=64, data=E_compatibility.degree8_data)
    E_compatibility.create_scale(starting_note=64, data=E_compatibility.degree7_data)
    E_compatibility.create_scale(starting_note=64, data=E_compatibility.degree6_data)
    E_compatibility.create_scale(starting_note=64, data=E_compatibility.degree5_data)
    E_compatibility.create_scale(starting_note=64, data=E_compatibility.degree4_data)
    E_compatibility.create_scale(starting_note=64, data=E_compatibility.degree3_data)
    E_compatibility.create_named_scale()

    F_compatibility.create_scale(starting_note=65, data=F_compatibility.degree8_data)
    F_compatibility.create_scale(starting_note=65, data=F_compatibility.degree7_data)
    F_compatibility.create_scale(starting_note=65, data=F_compatibility.degree6_data)
    F_compatibility.create_scale(starting_note=65, data=F_compatibility.degree5_data)
    F_compatibility.create_scale(starting_note=65, data=F_compatibility.degree4_data)
    F_compatibility.create_scale(starting_note=65, data=F_compatibility.degree3_data)
    F_compatibility.create_named_scale()

    Gb_compatibility.create_scale(starting_note=66, data=Gb_compatibility.degree8_data)
    Gb_compatibility.create_scale(starting_note=66, data=Gb_compatibility.degree7_data)
    Gb_compatibility.create_scale(starting_note=66, data=Gb_compatibility.degree6_data)
    Gb_compatibility.create_scale(starting_note=66, data=Gb_compatibility.degree5_data)
    Gb_compatibility.create_scale(starting_note=66, data=Gb_compatibility.degree4_data)
    Gb_compatibility.create_scale(starting_note=66, data=Gb_compatibility.degree3_data)
    Gb_compatibility.create_named_scale()

    G_compatibility.create_scale(starting_note=67, data=G_compatibility.degree8_data)
    G_compatibility.create_scale(starting_note=67, data=G_compatibility.degree7_data)
    G_compatibility.create_scale(starting_note=67, data=G_compatibility.degree6_data)
    G_compatibility.create_scale(starting_note=67, data=G_compatibility.degree5_data)
    G_compatibility.create_scale(starting_note=67, data=G_compatibility.degree4_data)
    G_compatibility.create_scale(starting_note=67, data=G_compatibility.degree3_data)
    G_compatibility.create_named_scale()

    Ab_compatibility.create_scale(starting_note=68, data=Ab_compatibility.degree8_data)
    Ab_compatibility.create_scale(starting_note=68, data=Ab_compatibility.degree7_data)
    Ab_compatibility.create_scale(starting_note=68, data=Ab_compatibility.degree6_data)
    Ab_compatibility.create_scale(starting_note=68, data=Ab_compatibility.degree5_data)
    Ab_compatibility.create_scale(starting_note=68, data=Ab_compatibility.degree4_data)
    Ab_compatibility.create_scale(starting_note=68, data=Ab_compatibility.degree3_data)
    Ab_compatibility.create_named_scale()

    A_compatibility.create_scale(starting_note=69, data=A_compatibility.degree8_data)
    A_compatibility.create_scale(starting_note=69, data=A_compatibility.degree7_data)
    A_compatibility.create_scale(starting_note=69, data=A_compatibility.degree6_data)
    A_compatibility.create_scale(starting_note=69, data=A_compatibility.degree5_data)
    A_compatibility.create_scale(starting_note=69, data=A_compatibility.degree4_data)
    A_compatibility.create_scale(starting_note=69, data=A_compatibility.degree3_data)
    A_compatibility.create_named_scale()

    Bb_compatibility.create_scale(starting_note=70, data=Bb_compatibility.degree8_data)
    Bb_compatibility.create_scale(starting_note=70, data=Bb_compatibility.degree7_data)
    Bb_compatibility.create_scale(starting_note=70, data=Bb_compatibility.degree6_data)
    Bb_compatibility.create_scale(starting_note=70, data=Bb_compatibility.degree5_data)
    Bb_compatibility.create_scale(starting_note=70, data=Bb_compatibility.degree4_data)
    Bb_compatibility.create_scale(starting_note=70, data=Bb_compatibility.degree3_data)
    Bb_compatibility.create_named_scale()

    B_compatibility.create_scale(starting_note=71, data=B_compatibility.degree8_data)
    B_compatibility.create_scale(starting_note=71, data=B_compatibility.degree7_data)
    B_compatibility.create_scale(starting_note=71, data=B_compatibility.degree6_data)
    B_compatibility.create_scale(starting_note=71, data=B_compatibility.degree5_data)
    B_compatibility.create_scale(starting_note=71, data=B_compatibility.degree4_data)
    B_compatibility.create_scale(starting_note=71, data=B_compatibility.degree3_data)
    B_compatibility.create_named_scale()

    dfs = C_compatibility.remove_rotated_duplicates(
        dfs=[
            C_compatibility.pentatonic_scales_named,
            # C_compatibility.hexatonic_scales_named, 
            # C_compatibility.heptatonic_scales_named, 
            # C_compatibility.ocatonic_scales_named,
            Db_compatibility.pentatonic_scales_named,
            # Db_compatibility.hexatonic_scales_named,
            # Db_compatibility.heptatonic_scales_named,
            # Db_compatibility.ocatonic_scales_named,
            D_compatibility.pentatonic_scales_named,
            # D_compatibility.hexatonic_scales_named,
            # D_compatibility.heptatonic_scales_named,
            # D_compatibility.ocatonic_scales_named,
            Eb_compatibility.pentatonic_scales_named,
            # Eb_compatibility.hexatonic_scales_named,
            # Eb_compatibility.heptatonic_scales_named,
            # Eb_compatibility.ocatonic_scales_named,
            E_compatibility.pentatonic_scales_named,
            # E_compatibility.hexatonic_scales_named,
            # E_compatibility.heptatonic_scales_named,
            # E_compatibility.ocatonic_scales_named,
            F_compatibility.pentatonic_scales_named,
            # F_compatibility.hexatonic_scales_named,
            # F_compatibility.heptatonic_scales_named,
            # F_compatibility.ocatonic_scales_named,
            Gb_compatibility.pentatonic_scales_named,
            # Gb_compatibility.hexatonic_scales_named,
            # Gb_compatibility.heptatonic_scales_named,
            # Gb_compatibility.ocatonic_scales_named,
            G_compatibility.pentatonic_scales_named,
            # G_compatibility.hexatonic_scales_named,
            # G_compatibility.heptatonic_scales_named,
            # G_compatibility.ocatonic_scales_named,
            Ab_compatibility.pentatonic_scales_named,
            # Ab_compatibility.hexatonic_scales_named,
            # Ab_compatibility.heptatonic_scales_named,
            # Ab_compatibility.ocatonic_scales_named,
            A_compatibility.pentatonic_scales_named,
            # A_compatibility.hexatonic_scales_named,
            # A_compatibility.heptatonic_scales_named,
            # A_compatibility.ocatonic_scales_named,
            Bb_compatibility.pentatonic_scales_named,
            # Bb_compatibility.hexatonic_scales_named,
            # Bb_compatibility.heptatonic_scales_named,
            # Bb_compatibility.ocatonic_scales_named,
            B_compatibility.pentatonic_scales_named,
            # B_compatibility.hexatonic_scales_named,
            # B_compatibility.heptatonic_scales_named,
            # B_compatibility.ocatonic_scales_named
        ]
    )

    comp_dict = C_compatibility.determine_compatibility(
        scales_dict={"A min7 3rd inv": ["G", "A", "C", "E"], 
                     "G\u266d min7\u266d5": ["G\u266d", "A", "C", "E"], 
                     "F min6: ": ["F", "A\u266d", "C", "D"], 
                     "E min7": ["E", "G", "B", "D"],
                     "E\u266d dim7": ["E\u266d", "G\u266d", "A", "C"], 
                     "D min7": ["D", "F", "A", "C"],
                     "G Dom7": ["G", "B", "D", "F"],
                     "C Maj7": ["C", "E", "G", "B"]},
        higher_degree_dfs=dfs,
        include_weak=False
    )

    reordered_comp_dict = C_compatibility.reorder_chords(comp_dict)

    for scale, compatibles in reordered_comp_dict.items():
        print(f"{scale}: {compatibles}\n")


