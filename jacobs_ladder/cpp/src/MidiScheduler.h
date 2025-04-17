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

    void addEvent(const Midi::MidiEvent &event);
    void addEvent(Midi::MidiEvent &event, long long offsetTicks);
    void addEvent(const Midi::NoteDuration &noteDuration);
    void addEvent(const Midi::NoteDuration &noteDuration, double offsetMs);

    void addEvents(const std::vector<Midi::MidiEvent> &events);
    void addEvents(std::vector<Midi::MidiEvent> &events, long long offsetTicks);
    void addEvents(std::vector<Midi::NoteDuration> &noteDurations);
    void addEvents(std::vector<Midi::NoteDuration> &noteDurations, double offsetMs);

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

    std::priority_queue<Midi::MidiEvent> mQueue;
    std::priority_queue<Midi::MidiEvent> mBuffer;

    std::unique_ptr<QpcUtils> mTimer;
    std::unique_ptr<RtMidiOut> mMidiOut;
    long long mFrequencyHz {10000};
    const long long mBudgetNs {50000};

    bool conditionallyPause();
    void player();
    bool scheduleEvent(Midi::MidiEvent event);
    bool scheduleEvents(std::vector<Midi::MidiEvent> events);
    void smartSleep(Midi::MidiEvent &event);

};


#endif // MIDI_SCHEDULER_H
