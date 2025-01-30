from .MusicTheory import MusicTheory


mt = MusicTheory(print_msgs=False)
cDb = mt.determine_key([[60, 0, 144, 100], [61, 0, 144, 100]], True)
print(f"{cDb=}\n")

cD = mt.determine_key([[60, 0, 144, 100], [62, 0, 144, 100]], True)
print(f"{cD=}\n")

cEb = mt.determine_key([[60, 0, 144, 100], [63, 0, 144, 100]], True)
print(f"{cEb=}\n")

cE = mt.determine_key([[60, 0, 144, 100], [64, 0, 144, 100]], True)
print(f"{cE=}\n")

cF = mt.determine_key([[60, 0, 144, 100], [65, 0, 144, 100]], True)
print(f"{cF=}\n")

cGb = mt.determine_key([[60, 0, 144, 100], [66, 0, 144, 100]], True)
print(f"{cGb=}\n")

cG = mt.determine_key([[60, 0, 144, 100], [67, 0, 144, 100]], True)
print(f"{cG=}\n")

cAb = mt.determine_key([[60, 0, 144, 100], [68, 0, 144, 100]], True)
print(f"{cAb=}\n")

cA = mt.determine_key([[60, 0, 144, 100], [69, 0, 144, 100]], True)
print(f"{cA=}\n")

cBb = mt.determine_key([[60, 0, 144, 100], [70, 0, 144, 100]], True)
print(f"{cBb=}\n")

cB = mt.determine_key([[60, 0, 144, 100], [71, 0, 144, 100]], True)
print(f"{cB=}\n")
