import pandas as pd
from itertools import product 


class ScaleTree:
    """Create obscure scales which meet certain criterion
    """
    
    def __init__(self, scale_length: int = 12):
        self.num_octave_divisions = scale_length
        
    def generate_combinations_dataframe(self, scale_degree: int, max_interval: int):
        """Generate all combinations of scales within a scale degree to some max interval size and return a dataframe.

        Args:
            scale_degree (int): Size of the scale in number of notes.
            max_interval (int): The max interval you wish to be present in the scale.

        Returns:
            pd.Dataframe: a dataframe with scales of degree scale_degree with data from 1 to max_interval whose rows must sum to 
            self.num_octave_divisions - 1.
        """

        column_combinations = product(range(1, max_interval + 1), repeat=scale_degree-1)
        df = pd.DataFrame(column_combinations, columns=[f'Column_{i+1}' for i in range(scale_degree-1)])
        
        mask = (df.sum(axis=1) < self.num_octave_divisions)
        valid_combinations_df = df[mask]

        return valid_combinations_df
    
    def list_num_scales_per_degree(self, max_degree: int, max_interval: int | list[int]):
        if max_degree < 2 or max_degree > 24:
            ValueError("Valid range for max_degree is 2-24")
            
        if type(max_interval) == int:
            for degree in range(2, max_degree + 1):
                df = self.generate_combinations_dataframe(scale_degree=degree, max_interval=max_interval)
                print(f"For scales of degree {degree} with max interval size {max_interval} there are {df.shape[0]} possible scales")
        elif type(max_interval) == list:
            for degree in range(2, max_degree + 1):
                print()
                for interval in max_interval:
                    df = self.generate_combinations_dataframe(scale_degree=degree, max_interval=interval)
                    print(f"For scales of degree {degree} with max interval size {interval} there are {df.shape[0]} possible scales")
        else:
            ValueError("max_interval must either be an integer or a list of integers")

if __name__ == "__main__":
    
    st = ScaleTree(9)
    df = st.generate_combinations_dataframe(scale_degree=5, max_interval=4)
    
    
    # Set option for viewing large df's without truncated console output
    pd.set_option('display.max_rows', None)
    
    st.list_num_scales_per_degree(max_degree=8, max_interval=4)
    print(df)
    

