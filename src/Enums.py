from enum import Enum


class Pitch(Enum):
    """The pitchwheel enum is meant to abstract away the just intervals after thay have been converted into analog
    values.  The analog values represent how far away from the equally tempered value to bend the pitch in order to
    make it a just interval

    Args:
        Enum (int): The analog pitch value between 0 and 16383 where 8192 represents no tuning, 0 down a whole step and
        16383 represents going up a whole step.
    """
    minor_second_up = 8673                  # 16/15 = +11.731  c
    major_second_up = 8352                  # 9/8   = +3.910   c
    major_second_harmonic_up = 9469         # 8/7   = +31.173  c
    major_second_flat_up = 7471             # 10/9  = -17.596  c
    major_second_half_flat_up = 6355        # 35/32 = -55.140  c
    minor_third_up = 8833                   # 6/5   = +15.641  c
    minor_third_harmonic_up = 6835          # 7/6   = -33.129  c
    major_third_up = 7631                   # 5/4   = -13.686  c
    perfect_fourth_up = 8112                # 4/3   = -1.955   c
    perfect_fourth_sharp_up = 8993          # 27/20 = +19.551  c
    tritone_up = 7792                       # 45/32 = -9.776   c
    tritone_sharp_up = 8592                 # 64/45 = +9.776   c
    perfect_fifth_up = 8272                 # 3/2   = +1.955   c
    minor_sixth_up = 8753                   # 8/5   = +13.686  c
    major_sixth_up = 7551                   # 5/3   = -15.641  c
    major_sixth_sharp_up = 8432             # 27/16 = +5.865   c
    major_sixth_half_flat_up = 6435         # 105/64 = +57.095 c
    minor_seventh_up = 8913                 # 9/5   = +17.596  c
    minor_harmonic_seventh_up = 6915        # 7/4   = -31.173  c
    minor_seventh_symetric_up = 8032        # 16/9  = -3.910   c
    major_seventh_up = 7711                 # 15/8  = -11.731  c

    minor_second_down = 7711                # 15/16 = -11.731  c        
    major_second_down = 8032                # 8/9   = -3.910   c  
    major_second_harmonic_down = 6915       # 7/8   = -31.173  c
    major_second_flat_down = 8913           # 9/10  = +17.596  c 
    major_second_half_flat_down = 10029     # 32/35 = +55.140  c   
    minor_third_down = 7551                 # 5/6   = -15.641  c   
    minor_third_harmonic_down = 9549        # 6/7   = +33.129  c   
    major_third_down = 8753                 # 4/5   = +13.686  c      
    perfect_fourth_down = 8272              # 3/4   = +1.955   c   
    perfect_fourth_sharp_down = 7391        # 20/27 = -19.551  c   
    tritone_down = 8592                     # 32/45 = +9.776   c 
    tritone_sharp_down = 7792               # 45/64 = -9.776   c       
    perfect_fifth_down = 8112               # 2/3   = -1.955   c      
    minor_sixth_down = 7631                 # 5/8   = -13.686  c      
    major_sixth_down = 8833                 # 3/5   = +15.641  c   
    major_sixth_sharp_down = 7952           # 16/27 = -5.865   c 
    major_sixth_half_flat_down = 9949       # 64/105 = -57.095 c  
    minor_seventh_down = 7471               # 5/9   = -17.596  c      
    minor_harmonic_seventh_down = 9469      # 4/7   = +31.173  c   
    minor_seventh_symetric_down = 8352      # 9/16  = +3.910   c   
    major_seventh_down = 9153               # 8/15  = +11.731  c       

    octave = 8192                           # 2/1 | 1/2         