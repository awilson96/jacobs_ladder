from enum import Enum


class Pitch(Enum):
    """The pitchwheel enum is meant to abstract away the just intervals after thay have been converted into analog
    values.  The analog values represent how far away from the equally tempered value to bend the pitch in order to
    make it a just interval

    Args:
        Enum (int): The analog pitch value between 0 and 16383 where 8192 represents no tuning, 0 down a whole step and
        16383 represents going up a whole step.
    """
    minor_second_up = 9153                  # 16/15 = +11.731  c
    major_second_up = 8512                  # 9/8   = +3.910   c
    major_second_harmonic_up = 0            # 8/7   = +31.173  c
    major_second_flat_up = 0                # 10/9  = -17.596  c
    major_second_half_flat_up = 0           # 35/32 = -55.140  c
    minor_third_up = 9473                   # 6/5   = +15.641  c
    minor_third_harmonic_up = 0             # 7/6   = -33.129  c
    major_third_up = 7070                   # 5/4   = -13.686  c
    perfect_fourth_up = 8031                # 4/3   = -1.955   c
    perfect_fourth_sharp_up = 0             # 27/20 = +19.551  c
    tritone_up = 7391                       # 45/32 = -9.776   c
    tritone_sharp_up = 0                    # 64/45 = +9.776   c
    perfect_fifth_up = 8352                 # 3/2   = +1.955   c
    minor_sixth_up = 9313                   # 8/5   = +13.686  c
    major_sixth_up = 6911                   # 5/3   = -15.641  c
    major_sixth_sharp_up = 0                # 27/16 = +5.865   c
    major_sixth_half_flat_up = 0            # 105/64 = +57.095 c
    minor_seventh_up = 9633                 # 9/5   = +17.596  c
    minor_harmonic_seventh_up = 5638        # 7/4   = -31.173  c
    minor_seventh_symetric_up = 0           # 16/9  = -3.910   c
    major_seventh_up = 7231                 # 15/8  = -11.731  c

    minor_second_down = 7231                # 15/16 = -11.731  c        
    major_second_down = 7872                # 8/9   = -3.910   c  
    major_second_harmonic_down = 0          # 7/8   = -31.173  c
    major_second_flat_down = 0              # 9/10  = +17.596  c 
    major_second_half_flat_down = 0         # 35/32 = +55.140  c   
    minor_third_down = 6911                 # 5/6   = -15.641  c   
    minor_third_harmonic_down = 0           # 7/6   = +33.129  c   
    major_third_down = 9313                 # 4/5   = +13.686  c      
    perfect_fourth_down = 8352              # 3/4   = +1.955   c   
    perfect_fourth_sharp_down = 0           # 20/27 = -19.551  c   
    tritone_down = 8993                     # 32/45 = +9.776   c 
    tritone_sharp_down = 0                  # 45/64 = -9.776   c       
    perfect_fifth_down = 8032               # 2/3   = -1.955   c      
    minor_sixth_down = 7071                 # 5/8   = -13.686  c      
    major_sixth_down = 9473                 # 3/5   = +15.641  c   
    major_sixth_sharp_down = 0              # 16/27 = -5.865   c 
    major_sixth_half_flat_down = 0          # 64/105 = -57.095 c  
    minor_seventh_down = 6751               # 5/9   = -17.596  c      
    minor_harmonic_seventh_down = 10746     # 7/4   = +31.173  c   
    minor_seventh_symetric_down = 0         # 16/9  = +3.910   c   
    major_seventh_down = 9153               # 8/15  = +11.731  c       

    octave = 8192                           # 2/1 | 1/2         