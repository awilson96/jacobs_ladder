from jacobs_ladder.src.cython import tuning_utils
from jacobs_ladder.src.Utilities import generate_tunings
import time

start1 = time.time()
tunings = tuning_utils.generate_tunings([60, 64, 67, 71, 72, 74], 0)
end1 = time.time()

print(f"Time taken for Cython function: {end1 - start1}")

start2 = time.time()
tunings = generate_tunings([60, 64, 67, 71, 72, 74], 0)
end2 = time.time()  

print(f"Time taken for Python function: {end2 - start2}")