#ifndef MIDI_SCHEDULER_H
#define MIDI_SCHEDULER_H

// Project Includes
#include "Constants.h"
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
    void addEvent(Midi::NoteEvent &noteEvent);
    void addEvent(Midi::NoteEvent &noteEvent, double offsetMs);

    void addEvents(const std::vector<Midi::MidiEvent> &events);
    void addEvents(std::vector<Midi::MidiEvent> &events, long long offsetTicks);
    void addEvents(std::vector<Midi::NoteEvent> &noteEvents);
    void addEvents(std::vector<Midi::NoteEvent> &noteEvents, double offsetMs);

    long long getPreviouslyScheduledNoteQpcTime();

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
    std::mutex mPreviouslyScheduledNoteQpcTimeMutex;
    std::condition_variable mPauseCv;

    std::priority_queue<Midi::MidiEvent> mQueue;
    std::priority_queue<Midi::MidiEvent> mBuffer;

    std::unique_ptr<QpcUtils> mTimer;
    std::unique_ptr<RtMidiOut> mMidiOut;
    long long mFrequencyHz {QPC_FREQUENCY};
    const long long mBudgetTicks {TEN_MILLISECOND_BUDGET_TICKS};
    long long mPreviouslyScheduledNoteQpcTime {0}; 

    bool conditionallyPause();
    long long getNoteDurationTicks(Midi::NoteEvent &noteEvent);
    void player();
    void resetPreviouslyScheduledNoteQpcTime();
    bool scheduleEvent(Midi::MidiEvent event);
    bool scheduleEvents(std::vector<Midi::MidiEvent> events);
    void smartSleep(Midi::MidiEvent &event);

};


#endif // MIDI_SCHEDULER_H
