#ifndef QPC_UTILS_H
#define QPC_UTILS_H

// system includes
#include <windows.h>
#include <chrono>
#include <utility>
#include <vector>
#include <cstdlib>

class QpcUtils {
public:
    QpcUtils();
    ~QpcUtils();

    long long qpcGetFutureTime(long long now, long long ms) const;
    long long qpcGetFrequency() const { return mFrequencyHz; }
    long long qpcGetTicks() const;
    void qpcCoarseSleep(long long ms);
    void qpcSleepMs(long long ms);
    void qpcSleepUs(long long us);
    void qpcSleepNs(long long ns);
    void qpcPrintTimeDiffNs(long long start, long long end) const;
    void qpcPrintTimeDiffUs(long long start, long long end) const;
    void qpcPrintTimeDiffMs(long long start, long long end) const;
    std::tuple<double, double, long long, double> qpcDisplayStatistics(const std::vector<long long>& durations) const;
    double qpcCalculatePercentError(double expectedTime, double meanTime) const;

private:
    long long mFrequencyHz;
    static constexpr long long mPrecisionNs = 16'000'000;
    LARGE_INTEGER mStartTime;
    DWORD_PTR mPreviousMask;

    void qpcSetFrequency(bool printMsgs = false);
    void qpcSleep(int option, long long dimmensionlessTime);
    void qpcPrintTimeDiff(int option, long long start, long long end) const;
};

#endif // QPC_UTILS_H
