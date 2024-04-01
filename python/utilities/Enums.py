from enum import Enum


class Pitch(Enum):
    """The pitchwheel enum is meant to abstract away the just intervals after thay have been converted into analog
    values.  The analog values represent how far away from the equally tempered value to bend the pitch in order to
    make it a just interval

    Args:
        Enum (int): The analog pitch value between 0 and 16383 where 8192 represents no tuning, 0 down a whole step and
        16383 represents going up a whole step.
    """
    minor_second_up = 8712     # 16/15
    major_second_up = 8352     # 9/8
    minor_third_up = 8860      # 6/5
    major_third_up = 7619      # 5/4
    perfect_fourth_up = 8110   # 4/3
    tritone_up = 7791          # 45/32
    perfect_fifth_up = 8270    # 3/2
    minor_sixth_up = 8753      # 8/5
    major_sixth_up = 7553      # 5/3
    minor_seventh_up = 8032    # 9/5
    major_seventh_up = 7713    # 15/8
    
    minor_second_down = 8712     # 15/16
    major_second_down = 8352     # 8/9
    minor_third_down = 8860      # 5/6
    major_third_down = 7619      # 4/5
    perfect_fourth_down = 8110   # 3/4
    tritone_down = 7791          # 32/45
    perfect_fifth_down = 8270    # 2/3
    minor_sixth_down = 8753      # 5/8
    major_sixth_down = 7553      # 3/5
    minor_seventh_down = 8032    # 5/9
    major_seventh_down = 7713    # 8/15
    octave = 8192                # 2/1 | 1/2