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

    uint64_t qpcGetFrequency() const { return mFrequencyHz; }
    uint64_t qpcGetTicks() const;
    void qpcCoarseSleep(uint64_t ms);
    void qpcSleepMs(uint64_t ms);
    void qpcSleepUs(uint64_t us);
    void qpcSleepNs(uint64_t ns);
    void qpcPrintTimeDiffNs(uint64_t start, uint64_t end) const;
    void qpcPrintTimeDiffUs(uint64_t start, uint64_t end) const;
    void qpcPrintTimeDiffMs(uint64_t start, uint64_t end) const;
    std::tuple<double, double, uint64_t, double> qpcDisplayStatistics(const std::vector<uint64_t>& durations) const;
    double qpcCalculatePercentError(double expectedTime, double meanTime) const;

private:
    uint64_t mFrequencyHz;
    static constexpr uint64_t mPrecisionNs = 16'000'000;
    LARGE_INTEGER mStartTime;
    DWORD_PTR mPreviousMask;

    void qpcSetFrequency(bool printMsgs = false);
    void qpcSleep(int option, uint64_t dimmensionlessTime);
    void qpcPrintTimeDiff(int option, uint64_t start, uint64_t end) const;
};

#endif // QPC_UTILS_H
