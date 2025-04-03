import time
from jacobs_ladder import qpc_utils

timer = qpc_utils.QpcUtils()

frequency = timer.qpcGetFrequency()
print(f"Query Performance Clock Frequency: {frequency} Hz")

# Example High Resolution Timing of the time.sleep() function
start_time = timer.qpcGetTicks()
time.sleep(2)
end_time = timer.qpcGetTicks()

# Display elapsed time in different units
elapsed_time_ns = timer.qpcPrintTimeDiffNs(start_time, end_time)
elapsed_time_us = timer.qpcPrintTimeDiffUs(start_time, end_time)
elapsed_time_ms = timer.qpcPrintTimeDiffMs(start_time, end_time)
print(f"Elapsed time in nanoseconds: {elapsed_time_ns} ns")
print(f"Elapsed time in microseconds: {elapsed_time_us} us")
print(f"Elapsed time in milliseconds: {elapsed_time_ms} ms")

for i in range(10):
    timer.qpcSleepMs(200)
    print(f"{i}: Slept for 200 ms")

for i in range(10):
    timer.qpcSleepUs(100000)
    print(f"{i}: Slept for 100000 us")

for i in range(100):
    timer.qpcSleepNs(3000000)
    print(f"{i}: Slept for 30000000 ns")

durations = []
for i in range(100):
    start_time = timer.qpcGetTicks()
    timer.qpcSleepMs(10)
    end_time = timer.qpcGetTicks()
    durations.append(end_time - start_time)

(mean, median, mode, standard_deviation) = timer.qpcDisplayStatistics(durations)

print(f"\nStatistics of sleep durations (values returned to python):")
print(f"Mean: {mean} ns")
print(f"Median: {median} ns")
print(f"Mode: {mode} ns")
print(f"Standard Deviation: {standard_deviation} ns\n")

expected_value = 10 * 10**6

print(f"Calculate the percent error of the mean: \n")
precision = timer.qpcCalculatePercentError(expected_value, mean)

print(f"Conclusions: \nThe resolution of the QPC timer is {standard_deviation:.2f} ns or {standard_deviation / 1e3:.2f} us.")
print(f"The timer has a precision of {precision:.2f} %, meaning that the timer on average is off by ± {abs(expected_value - mean)/1000:.2f} us")
print(f"It should be noted that if you exclude the timer.qpcGetTicks() calls and print statements from the loop, the precision will be much better.")
print(f"That said, the qpc timer is not a real time clock and after the python overhead, the precision is typically around tens of microseconds level accuracy.")
print(f"For most music scheduling algorithms, this is more than sufficient as the minimum time resolution needed is typically in the tens of milliseconds.")