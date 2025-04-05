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

uint64_t QpcUtils::qpcGetTicks() const {
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

void QpcUtils::qpcCoarseSleep(uint64_t ms) {
    // Sleep for the specified number of milliseconds using coarse sleep (1 ms resolution since we used winmm function timeBeginPeriod(1))
    std::this_thread::sleep_for(std::chrono::milliseconds(ms));
}

void QpcUtils::qpcSleep(int option, uint64_t dimmensionlessTime) {
    uint64_t dimensionlessTimeInNs;
    uint64_t conversionFactor;
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
        uint64_t targetTicks = start.QuadPart + (dimmensionlessTime * mFrequencyHz) / conversionFactor;
        
        // If the requested sleep time is greater than 2 times mPrecisionNs, use coarse sleep
        uint64_t threshold = 5 * mPrecisionNs;
        if (dimensionlessTimeInNs > threshold) {
            // Coarse sleep for the requested time minus 2 times the course time resolution 
            uint64_t coarseSleepTime = static_cast<uint64_t>(dimensionlessTimeInNs - threshold);
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

void QpcUtils::qpcSleepNs(uint64_t ns) {
    qpcSleep(0, ns);
}

void QpcUtils::qpcSleepUs(uint64_t us) {
    qpcSleep(1, us);
}

void QpcUtils::qpcSleepMs(uint64_t ms) {
    qpcSleep(2, ms);
}

void QpcUtils::qpcPrintTimeDiff(int option, uint64_t start, uint64_t end) const {
    if (start < 0 || end < 0 || option < 0 || option > 2) {
        std::cerr << "Error: Invalid start or end time.\n";
        return;
    }

    uint64_t conversionFactor;
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
    uint64_t elapsedNs = (end - start) * conversionFactor / mFrequencyHz;

    // Force decimal notation with no scientific output
    std::cout << std::fixed << std::setprecision(0)
              << "Elapsed time: " << elapsedNs << " " << units << "\n";
}

void QpcUtils::qpcPrintTimeDiffNs(uint64_t start, uint64_t end) const {
    qpcPrintTimeDiff(0, start, end);
}

void QpcUtils::qpcPrintTimeDiffUs(uint64_t start, uint64_t end) const {
    qpcPrintTimeDiff(1, start, end);
}

void QpcUtils::qpcPrintTimeDiffMs(uint64_t start, uint64_t end) const {
    qpcPrintTimeDiff(2, start, end);
}

std::tuple<double, double, uint64_t, double> QpcUtils::qpcDisplayStatistics(const std::vector<uint64_t>& durations) const {
    if (durations.empty()) {
        std::cerr << "Error: Empty duration vector passed to displayStatistics.\n";
        return std::make_tuple(0.0, 0.0, 0LL, 0.0);
    }

    // Convert the raw ticks to nanoseconds
    std::vector<uint64_t> durationsInNs;
    for (uint64_t duration : durations) {
        uint64_t durationInNs = static_cast<uint64_t>((duration * 1.0 / mFrequencyHz) * 1e9);
        durationsInNs.push_back(durationInNs);
    }

    // Mean Calculation
    uint64_t sum = std::accumulate(durationsInNs.begin(), durationsInNs.end(), 0LL);
    double mean = static_cast<double>(sum) / durationsInNs.size();

    // Median Calculation
    std::vector<uint64_t> sortedDurations = durationsInNs;
    std::sort(sortedDurations.begin(), sortedDurations.end());
    double median;
    size_t n = sortedDurations.size();
    if (n % 2 == 0) {
        median = (sortedDurations[n / 2 - 1] + sortedDurations[n / 2]) / 2.0;
    } else {
        median = sortedDurations[n / 2];
    }

    // Mode Calculation
    std::map<uint64_t, int> frequencyMap;
    for (uint64_t duration : durationsInNs) {
        frequencyMap[duration]++;
    }

    uint64_t mode = durationsInNs[0];
    int maxCount = 0;
    for (const auto& entry : frequencyMap) {
        if (entry.second > maxCount) {
            mode = entry.first;
            maxCount = entry.second;
        }
    }

    // Standard Deviation Calculation
    double variance = 0.0;
    for (uint64_t duration : durationsInNs) {
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