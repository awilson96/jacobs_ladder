class Favorites:

    def __init__(self) -> None:
        self.keys = ["Rom1A 11-E.PIANO 1", "Mark V EP", "Met Before Our Time", "Classic Jun Keys", 
                     "Rom1B 01-PIANO 4", "Soft Harp", "Sustained Strings", "Book of Memories",
                     "Synthwave Split", "House in the Forest", "Ad Libernam", "American Old Radio", 
                     "Pagoda Dreams", "Horns for Hudson", "Ideologic Organ"]

    def display_options(self):
        for idx, key_instrument in enumerate(self.keys, start=1):
            print(f"{idx}. {key_instrument}")
    
if __name__ == "__main__":
    favs = Favorites()
    favs.display_options()
