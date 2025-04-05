#include <iostream>
#include <cstdint>
#include <vector>
#include <thread>

#include "QpcUtils.h"

int main() {
    QpcUtils timer;
    std::vector<uint64_t> durations;
    std::tuple<double, double, uint64_t, double> stats;
    double percentError;

    // Test the accuracy of sleeps when using the default sleep function (10 ms)
    for (unsigned int i = 0; i < 100; i++) {
        uint64_t start = timer.qpcGetTicks();
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        uint64_t end = timer.qpcGetTicks();
        durations.push_back(end - start);
    }
    std::cout << "Using std::this_thread_sleep_for(std::chrono::milliseconds(10))\n";
    stats = timer.qpcDisplayStatistics(durations);
    percentError = timer.qpcCalculatePercentError(10000000.0, std::get<0>(stats));
    std::cout << "\n";
    durations.clear();

    // Test the accuracy of sleeps when using the course sleep function (1 ms, this is a wrapper around std::this_sleep_for() but uses winmm function timeBeginPeriod(1) for higher accuracy, 1 ms precision)
    for (unsigned int i = 0; i < 100; i++) {
        uint64_t start = timer.qpcGetTicks();
        timer.qpcCoarseSleep(10);
        uint64_t end = timer.qpcGetTicks();
        durations.push_back(end - start);
    }
    std::cout << "Using QpcUtils::qpcCoarseSleep(10)\n";
    stats = timer.qpcDisplayStatistics(durations);
    percentError = timer.qpcCalculatePercentError(10000000.0, std::get<0>(stats));
    std::cout << "\n";
    durations.clear();

    // Test the accuracy of sleeps when sleeping for 1 ms using QpcUtils::qpcSleepMs
    for (unsigned int i = 0; i < 10000; i++) {
        uint64_t start = timer.qpcGetTicks();
        timer.qpcSleepMs(1);
        uint64_t end = timer.qpcGetTicks();
        durations.push_back(end - start);
    }
    std::cout << "Using QpcUtils::qpcSleepMs(1) i.e. 1 ms\n";
    stats = timer.qpcDisplayStatistics(durations);
    percentError = timer.qpcCalculatePercentError(1000000.0, std::get<0>(stats));
    std::cout << "\n";
    durations.clear();
    
    // Test accuracy of sleeps when sleeping for 33 ms using QpcUtils::qpcSleepNs (1 ms above the threshold for using course sleep)
    for (unsigned int i = 0; i < 1000; i++) {
        uint64_t start = timer.qpcGetTicks();
        timer.qpcSleepNs(33000000);
        uint64_t end = timer.qpcGetTicks();
        durations.push_back(end - start);
    }
    std::cout << "Using QpcUtils::qpcSleepNs(33000000) i.e. 33 ms\n";
    stats = timer.qpcDisplayStatistics(durations);
    percentError = timer.qpcCalculatePercentError(33000000.0, std::get<0>(stats));
    std::cout << "\n";
    durations.clear();

    // Test the accuracy of sleeps when sleeping for 1000 ms (1 second checking for good coarse time accuracy)
    for (unsigned int i = 0; i < 30; i++) {
        uint64_t start = timer.qpcGetTicks();
        timer.qpcSleepUs(1000000);
        uint64_t end = timer.qpcGetTicks();
        durations.push_back(end - start);
    }
    std::cout << "Using QpcUtils::qpcSleepUs(1000000) i.e. 1000 ms\n";
    stats = timer.qpcDisplayStatistics(durations);
    percentError = timer.qpcCalculatePercentError(1000000000.0, std::get<0>(stats));
    
    return 0;
}
