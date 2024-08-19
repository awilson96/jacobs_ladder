from .MusicTheory import MusicTheory


mt = MusicTheory(shared_memory_index=2, print_chords=False)
cDb = mt.determine_key([[60, 0, 144, 100], [61, 0, 144, 100]])
print(f"{cDb=}")

cD = mt.determine_key([[60, 0, 144, 100], [62, 0, 144, 100]])
print(f"{cD=}")

cEb = mt.determine_key([[60, 0, 144, 100], [63, 0, 144, 100]])
print(f"{cEb=}")

cE = mt.determine_key([[60, 0, 144, 100], [64, 0, 144, 100]])
print(f"{cE=}")

cF = mt.determine_key([[60, 0, 144, 100], [65, 0, 144, 100]])
print(f"{cF=}")

cGb = mt.determine_key([[60, 0, 144, 100], [66, 0, 144, 100]])
print(f"{cGb=}")

cG = mt.determine_key([[60, 0, 144, 100], [67, 0, 144, 100]])
print(f"{cG=}")

cAb = mt.determine_key([[60, 0, 144, 100], [68, 0, 144, 100]])
print(f"{cAb=}")

cA = mt.determine_key([[60, 0, 144, 100], [69, 0, 144, 100]])
print(f"{cA=}")

cBb = mt.determine_key([[60, 0, 144, 100], [70, 0, 144, 100]])
print(f"{cBb=}")

cB = mt.determine_key([[60, 0, 144, 100], [71, 0, 144, 100]])
print(f"{cB=}")
