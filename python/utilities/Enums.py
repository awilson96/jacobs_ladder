from enum import Enum


class Pitch(Enum):
    """The pitchwheel enum is meant to abstract away the just intervals after thay have been converted into analog
    values.  The analog values represent how far away from the equally tempered value to bend the pitch in order to
    make it a just interval

    Args:
        Enum (int): The analog pitch value between 0 and 16383 where 8192 represents no tuning, 0 down a whole step and
        16383 represents going up a whole step.
    """
    minor_second = 8712     # 16/15
    major_second = 8352     # 9/8
    minor_third = 8860      # 6/5
    major_third = 7619      # 5/4
    perfect_fourth = 8110   # 4/3
    tritone = 7791          # 45/32
    perfect_fifth = 8270    # 3/2
    minor_sixth = 8753      # 8/5
    major_sixth = 7553      # 5/3
    minor_seventh = 8032    # 9/5
    major_seventh = 7713    # 15/8
    octave = 8192           # 2/1
    # minor_ninth = 1
    # major_ninth = 1
    # minor_tenth = 1
    # major_tenth = 1
    # major_eleventh = 1
    # sharp_eleventh = 1
    # minor_thirtenth = 1
    # major_thirtenth = 1