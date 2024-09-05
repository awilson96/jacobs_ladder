class Favorites:

    def __init__(self) -> None:
        self.keys = ["Rom1A 11-E.PIANO 1", "Mark V EP", "Met Before Our Time"]


    def display_options(self):
        for idx, key_instrument in enumerate(self.keys, start=1):
            print(f"{idx}. {key_instrument}")