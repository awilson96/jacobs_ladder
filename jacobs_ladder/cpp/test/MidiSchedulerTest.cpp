#include "MidiScheduler.h"
#include "MidiDefinitions.h"
#include "QpcUtils.h"
#include "rtmidi/RtMidi.h"

#include <cstdlib>

int main() {

    // Create a MidiScheduler instance with a specific output port name
    MidiScheduler midiScheduler("jacob");
    QpcUtils timer;
    long long now = timer.qpcGetTicks();

    MidiEvent c60 = {MidiMessageType::NOTE_ON, 60, 127, timer.qpcGetFutureTime(now, 50LL)};
    MidiEvent _c60 = {MidiMessageType::NOTE_OFF, 60, 127, timer.qpcGetFutureTime(now, 100LL)}; 
    MidiEvent c62 = {MidiMessageType::NOTE_ON, 62, 127, timer.qpcGetFutureTime(now, 100LL)}; 
    MidiEvent _c62 = {MidiMessageType::NOTE_OFF, 62, 127, timer.qpcGetFutureTime(now, 150LL)};
    MidiEvent c64 = {MidiMessageType::NOTE_ON, 64, 127, timer.qpcGetFutureTime(now, 150LL)};
    MidiEvent _c64 = {MidiMessageType::NOTE_OFF, 64, 127, timer.qpcGetFutureTime(now, 200LL)};
    MidiEvent c65 = {MidiMessageType::NOTE_ON, 65, 127, timer.qpcGetFutureTime(now, 200LL)};
    MidiEvent _c65 = {MidiMessageType::NOTE_OFF, 65, 127, timer.qpcGetFutureTime(now, 250LL)};
    MidiEvent c67 = {MidiMessageType::NOTE_ON, 67, 127, timer.qpcGetFutureTime(now, 250LL)};
    MidiEvent _c67 = {MidiMessageType::NOTE_OFF, 67, 127, timer.qpcGetFutureTime(now, 300LL)};
    MidiEvent c69 = {MidiMessageType::NOTE_ON, 69, 127, timer.qpcGetFutureTime(now, 300LL)};
    MidiEvent _c69 = {MidiMessageType::NOTE_OFF, 69, 127, timer.qpcGetFutureTime(now, 350LL)};
    MidiEvent c71 = {MidiMessageType::NOTE_ON, 71, 127, timer.qpcGetFutureTime(now, 350LL)};
    MidiEvent _c71 = {MidiMessageType::NOTE_OFF, 71, 127, timer.qpcGetFutureTime(now, 400LL)};
    MidiEvent c72 = {MidiMessageType::NOTE_ON, 72, 127, timer.qpcGetFutureTime(now, 400LL)};
    MidiEvent _c72 = {MidiMessageType::NOTE_OFF, 72, 127, timer.qpcGetFutureTime(now, 450LL)};

    std::vector<MidiEvent> events = {c60, _c60, c62, _c62, c64, _c64, c65, _c65, c67, _c67, c69, _c69, c71, _c71, c72, _c72};
    midiScheduler.addEvents(events, 500);
    midiScheduler.player();

    timer.qpcSleepMs(2000);

    return 0;
}