from enum import Enum


class Pitch(Enum):
    """The pitchwheel enum is meant to abstract away the just intervals after thay have been converted into analog
    values.  The analog values represent how far away from the equally tempered value to bend the pitch in order to
    make it a just interval

    Args:
        Enum (int): The analog pitch value between 0 and 16383 where 8192 represents no tuning, 0 down a whole step and
        16383 represents going up a whole step.
    """
    minor_second_up = 8192                  # 16/15   9153
    major_second_up = 8512                  # 9/8
    minor_third_up = 9473                   # 6/5
    major_third_up = 7070                   # 5/4
    perfect_fourth_up = 8031                # 4/3
    tritone_up = 7391                       # 45/32
    perfect_fifth_up = 8352                 # 3/2
    minor_sixth_up = 9313                   # 8/5
    major_sixth_up = 6911                   # 5/3
    minor_seventh_up = 9633                 # 9/5
    minor_harmonic_seventh_up = 5638        # 7/4
    major_seventh_up = 7231                 # 15/8

    minor_second_down = 7231                # 15/16
    major_second_down = 7872                # 8/9
    minor_third_down = 6911                 # 5/6
    major_third_down = 9313                 # 4/5
    perfect_fourth_down = 8352              # 3/4
    tritone_down = 8993                     # 32/45
    perfect_fifth_down = 8032               # 2/3
    minor_sixth_down = 7071                 # 5/8
    major_sixth_down = 9473                 # 3/5
    minor_seventh_down = 6751               # 5/9
    minor_harmonic_seventh_down = 10746     # 7/4
    major_seventh_down = 9153               # 8/15
    octave = 8192                           # 2/1 | 1/2