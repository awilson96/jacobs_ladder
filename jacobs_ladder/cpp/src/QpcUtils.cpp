// Project includes
#include "QpcUtils.h"

// System includes
#include <thread>
#include <iostream>
#include <iomanip>
#include <cmath>
#include <map>
#include <numeric>
#include <algorithm>
#include <chrono>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

QpcUtils::QpcUtils() {
    // Set system timer resolution to 1 ms using windows multimedia API
    timeBeginPeriod(1);

    // Initialize frequency and precision
    qpcSetFrequency(false);

    // Set thread affinity to a single CPU core for better timing accuracy
    mPreviousMask = SetThreadAffinityMask(GetCurrentThread(), 1);
    // Set process priority to Real-Time
    SetPriorityClass(GetCurrentProcess(), REALTIME_PRIORITY_CLASS);
    // Set thread priority to Time-Critical
    SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_TIME_CRITICAL);
}

QpcUtils::~QpcUtils() {
    // Restore default timer resolution
    timeEndPeriod(1);

    // Restore previous thread affinity
    SetThreadAffinityMask(GetCurrentThread(), mPreviousMask);
}

long long QpcUtils::qpcGetTicks() const {
    LARGE_INTEGER ticks;
    if (QueryPerformanceCounter(&ticks)) {
        return ticks.QuadPart;
    } else {
        std::cerr << "Error: Unable to query performance counter.\n";
        return -1;
    }
}

void QpcUtils::qpcSetFrequency(bool printMsgs) {
    LARGE_INTEGER frequency;
    
    if (QueryPerformanceFrequency(&frequency)) {
        mFrequencyHz = frequency.QuadPart;
        if (printMsgs)
            std::cout << "Performance Counter Frequency: " << mFrequencyHz << " Hz\n";
    }
    else {
        if (printMsgs)
            std::cerr << "Error: Unable to query performance counter frequency.\n";
    }
}

void QpcUtils::qpcCoarseSleep(long long ms) {
    // Sleep for the specified number of milliseconds using coarse sleep (1 ms resolution since we used winmm function timeBeginPeriod(1))
    std::this_thread::sleep_for(std::chrono::milliseconds(ms));
}

void QpcUtils::qpcSleep(int option, long long dimmensionlessTime) {
    long long dimensionlessTimeInNs;
    long long conversionFactor;
    // If option is 0, convert the time to nanoseconds
    if (option == 0) {
        dimensionlessTimeInNs = dimmensionlessTime;
        conversionFactor = 1'000'000'000LL;
    }
    // If option is 1, convert the time to microseconds
    else if (option == 1) {
        dimensionlessTimeInNs = dimmensionlessTime * 1'000LL;
        conversionFactor = 1'000'000LL;
    }
    // If option is 2, convert the time to milliseconds
    else if (option == 2) {
        dimensionlessTimeInNs = dimmensionlessTime * 1'000'000LL;
        conversionFactor = 1'000LL;
    }
    // Invalid option, print error message and return
    else {
        std::cerr << "Error: Invalid option. Use 0 for ns, 1 for us, or 2 for ms.\n";
        return;
    }

    // Get the current performance counter value
    LARGE_INTEGER start, now;

    if (QueryPerformanceCounter(&start)) {
        // Calculate target QPC value (absolute time)
        long long targetTicks = start.QuadPart + (dimmensionlessTime * mFrequencyHz) / conversionFactor;
        
        // If the requested sleep time is greater than 2 times mPrecisionNs, use coarse sleep
        long long threshold = 5 * mPrecisionNs;
        if (dimensionlessTimeInNs > threshold) {
            // Coarse sleep for the requested time minus 2 times the course time resolution 
            long long coarseSleepTime = static_cast<long long>(dimensionlessTimeInNs - threshold);
            std::this_thread::sleep_for(std::chrono::nanoseconds(coarseSleepTime));
        }

        do {
            QueryPerformanceCounter(&now);
        } while (now.QuadPart < targetTicks);
    } 
    else {
        std::cerr << "Error: Unable to query performance counter.\n";
    }
}

void QpcUtils::qpcSleepNs(long long ns) {
    qpcSleep(0, ns);
}

void QpcUtils::qpcSleepUs(long long us) {
    qpcSleep(1, us);
}

void QpcUtils::qpcSleepMs(long long ms) {
    qpcSleep(2, ms);
}

void QpcUtils::qpcPrintTimeDiff(int option, long long start, long long end) const {
    if (start < 0 || end < 0 || option < 0 || option > 2) {
        std::cerr << "Error: Invalid start or end time.\n";
        return;
    }

    long long conversionFactor;
    std::string units;
    // If option is 0, convert the time to nanoseconds
    if (option == 0) {
        conversionFactor = 1'000'000'000LL; 
        units = "ns";
    }
    // If option is 1, convert the time to microseconds
    else if (option == 1) {
        conversionFactor = 1'000'000LL;
        units = "us";
    }
    // If option is 2, convert the time to milliseconds
    else if (option == 2) {
        conversionFactor = 1'000LL; 
        units = "ms";
    }

    // Calculate elapsed time in nanoseconds correctly
    long long elapsedNs = (end - start) * conversionFactor / mFrequencyHz;

    // Force decimal notation with no scientific output
    std::cout << std::fixed << std::setprecision(0)
              << "Elapsed time: " << elapsedNs << " " << units << "\n";
}

void QpcUtils::qpcPrintTimeDiffNs(long long start, long long end) const {
    qpcPrintTimeDiff(0, start, end);
}

void QpcUtils::qpcPrintTimeDiffUs(long long start, long long end) const {
    qpcPrintTimeDiff(1, start, end);
}

void QpcUtils::qpcPrintTimeDiffMs(long long start, long long end) const {
    qpcPrintTimeDiff(2, start, end);
}

std::tuple<double, double, long long, double> QpcUtils::qpcDisplayStatistics(const std::vector<long long>& durations) const {
    if (durations.empty()) {
        std::cerr << "Error: Empty duration vector passed to displayStatistics.\n";
        return std::make_tuple(0.0, 0.0, 0LL, 0.0);
    }

    // Convert the raw ticks to nanoseconds
    std::vector<long long> durationsInNs;
    for (long long duration : durations) {
        long long durationInNs = static_cast<long long>((duration * 1.0 / mFrequencyHz) * 1e9);
        durationsInNs.push_back(durationInNs);
    }

    // Mean Calculation
    long long sum = std::accumulate(durationsInNs.begin(), durationsInNs.end(), 0LL);
    double mean = static_cast<double>(sum) / durationsInNs.size();

    // Median Calculation
    std::vector<long long> sortedDurations = durationsInNs;
    std::sort(sortedDurations.begin(), sortedDurations.end());
    double median;
    size_t n = sortedDurations.size();
    if (n % 2 == 0) {
        median = (sortedDurations[n / 2 - 1] + sortedDurations[n / 2]) / 2.0;
    } else {
        median = sortedDurations[n / 2];
    }

    // Mode Calculation
    std::map<long long, int> frequencyMap;
    for (long long duration : durationsInNs) {
        frequencyMap[duration]++;
    }

    long long mode = durationsInNs[0];
    int maxCount = 0;
    for (const auto& entry : frequencyMap) {
        if (entry.second > maxCount) {
            mode = entry.first;
            maxCount = entry.second;
        }
    }

    // Standard Deviation Calculation
    double variance = 0.0;
    for (long long duration : durationsInNs) {
        variance += std::pow(duration - mean, 2);
    }
    variance /= durationsInNs.size();
    double stdDev = std::sqrt(variance);

    // Output the statistics
    std::cout << "Statistics:\n" << std::fixed << std::setprecision(2)
              << "Mean: " << mean << " ns\n"
              << "Median: " << median << " ns\n"
              << "Mode: " << mode << " ns\n"
              << "Standard Deviation: " << stdDev << " ns\n";

    // Return the tuple with statistics
    return std::make_tuple(mean, median, mode, stdDev);
}

// Function to calculate percent error
double QpcUtils::qpcCalculatePercentError(double expectedTime, double meanTime) const {
    if (expectedTime == 0.0) {
        std::cerr << "Error: Expected time cannot be zero.\n";
        return 0.0;
    }
    // Calculate the absolute difference between expected and actual times
    double diff = std::abs(expectedTime - meanTime);

    // Calculate and return the percent error
    double percentError = diff / expectedTime * 100.0;
    std::cout << "Percent Error: " << percentError << "%\n";
    return percentError;
}