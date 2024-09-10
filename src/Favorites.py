class Favorites:

    def __init__(self) -> None:
        self.keys = ["Rom1A 11-E.PIANO 1", "Mark V EP", "Met Before Our Time"]


    def display_options(self):
        for idx, key_instrument in enumerate(self.keys, start=1):
            print(f"{idx}. {key_instrument}")
            
    # Favorites:
    #   Rom1A 11-E.PIANO 1
    #   Mark V EP
    #   Grand Piano 1
    #   Classic Jun Keys
    #   Pianos
    #   Dark Flute
    #   Lightway
    #   Rom1B 01-PIANO 4
    #   Rom1B 06-PIANO 5THS
    #   80's Bit
    #   Cathedral Lead
    #   Hacker