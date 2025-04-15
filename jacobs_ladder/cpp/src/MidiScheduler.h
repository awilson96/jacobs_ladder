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

    bool addEvent(MidiEvent event);
    bool addEvent(MidiEvent event, int offsetNs);
    bool addEvents(std::vector<MidiEvent> events);
    bool addEvents(std::vector<MidiEvent> events, int offsetNs);

    void pause();
    void resume();
    bool start();
    void stop();

    void player();

private:
    std::atomic<bool> mRunning {false};
    std::atomic<bool> mPaused {false};
    std::atomic<bool> mPrintMsgs {false};
    std::thread mPlayerThread;
    std::mutex mPauseMutex;
    std::condition_variable mPauseCv;
    std::priority_queue<MidiEvent> mQueue;
    std::unique_ptr<QpcUtils> mTimer;
    std::unique_ptr<RtMidiOut> mMidiOut;
    long long mFrequencyHz {10000};
};


#endif // MIDI_SCHEDULER_H
