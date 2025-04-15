#ifndef MIDI_SCHEDULER_H
#define MIDI_SCHEDULER_H

// Project Includes
#include "MidiDefinitions.h"
#include "QpcUtils.h"
#include "rtmidi/RtMidi.h"

// System Includes
#include <queue>
#include <vector>
#include <memory>
#include <atomic>
#include <thread>
#include <mutex>
#include <condition_variable>

class MidiScheduler {
public:
    MidiScheduler(const std::string& outputPortName, bool startImmediately = true,  bool printMsgs = false);
    ~MidiScheduler();

    void addEvent(const MidiEvent &event);
    void addEvent(MidiEvent &event, long long offsetTicks);
    void addEvents(const std::vector<MidiEvent> &events);
    void addEvents(std::vector<MidiEvent> &events, long long offsetTicks);

    void pause();
    void resume();
    bool start();
    void stop();

private:
    std::atomic<bool> mRunning {false};
    std::atomic<bool> mPaused {false};
    std::atomic<bool> mPrintMsgs {false};

    std::thread mPlayerThread;
    std::mutex mPauseMutex;
    std::mutex mBufferMutex;
    std::condition_variable mPauseCv;

    std::priority_queue<MidiEvent> mQueue;
    std::priority_queue<MidiEvent> mBuffer;

    std::unique_ptr<QpcUtils> mTimer;
    std::unique_ptr<RtMidiOut> mMidiOut;
    long long mFrequencyHz {10000};
    const long long mBudgetNs {50000};

    bool conditionallyPause();
    void player();
    bool scheduleEvent(MidiEvent event);
    bool scheduleEvents(std::vector<MidiEvent> events);
    void smartSleep(MidiEvent &event);

};


#endif // MIDI_SCHEDULER_H
