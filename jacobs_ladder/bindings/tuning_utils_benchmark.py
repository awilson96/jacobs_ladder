from jacobs_ladder.bindings import tuning_utils
from jacobs_ladder.src.Utilities import generate_tunings
import time

start1 = time.time()
tunings1 = tuning_utils.generate_tunings([60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71], 0)
end1 = time.time()

for tuning in tunings1:
    print(tuning)

print(f"Time taken for Cython function: {end1 - start1}")

# start2 = time.time()
# tunings2 = generate_tunings([60, 62, 64, 67, 71, 72, 78], 0)
# end2 = time.time()  

# for tuning in tunings2:
#     print(tuning)

# print(f"Time taken for Python function: {end2 - start2}")