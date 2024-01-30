import pandas as pd
from itertools import product 


class ScaleTree:
    """Create obscure scales which meet certain criterion
    """
    
    def __init__(self):
        self.num_octave_divisions = 12
        
    def generate_combinations_dataframe(self, scale_degree: int, max_interval: int):
        """Generate all combinations of scales within a scale degree to some max interval size and return a dataframe

        Args:
            scale_degree (int): Size of the scale in number of notes
            max_interval (int): The max interval you wish to be present in the scale

        Returns:
            _type_: _description_
        """

        column_combinations = product(range(1, max_interval + 1), repeat=scale_degree-1)
        df = pd.DataFrame(column_combinations, columns=[f'Column_{i+1}' for i in range(scale_degree-1)])
        
        mask = (df.sum(axis=1) < self.num_octave_divisions)
        valid_combinations_df = df[mask]

        return valid_combinations_df

if __name__ == "__main__":
    
    st = ScaleTree()
    df = st.generate_combinations_dataframe(scale_degree=7, max_interval=4)
    # Set option for viewing large df's without truncated console output
    pd.set_option('display.max_rows', None)
    print(df.to_string(index=False))
    print(df.shape)

