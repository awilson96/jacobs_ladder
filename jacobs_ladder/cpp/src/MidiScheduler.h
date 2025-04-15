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

class MidiScheduler {
public:
    MidiScheduler(const std::string& outputPortName, bool printMsgs = false);
    ~MidiScheduler();

    bool addEvent(MidiEvent event);
    bool addEvent(MidiEvent event, int offset);
    bool addEvents(std::vector<MidiEvent> events);
    bool addEvents(std::vector<MidiEvent> events, int offset);

    void player();

private:
    std::atomic<bool> mPrintMsgs {false};
    std::priority_queue<MidiEvent> mQueue;
    std::unique_ptr<QpcUtils> mTimer;
    std::unique_ptr<RtMidiOut> mMidiOut;
    long long mFrequencyHz {10000};
};


#endif // MIDI_SCHEDULER_H
