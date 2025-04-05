#include "MidiScheduler.h"
#include "MidiDefinitions.h"
#include "QpcUtils.h"
#include "rtmidi/RtMidi.h"

#include <cstdlib>

int main() {

    // Create a MidiScheduler instance with a specific output port name
    MidiScheduler midiScheduler("jacob");
    QpcUtils timer;

    MidiEvent c60 = {MidiMessageType::NOTE_ON, 60, 127, 500};
    MidiEvent _c60 = {MidiMessageType::NOTE_OFF, 60, 127, 501}; 
    MidiEvent c62 = {MidiMessageType::NOTE_ON, 62, 127, 502}; 
    MidiEvent _c62 = {MidiMessageType::NOTE_OFF, 62, 127, 503};
    MidiEvent c64 = {MidiMessageType::NOTE_ON, 64, 127, 504};
    MidiEvent _c64 = {MidiMessageType::NOTE_OFF, 64, 127, 505};
    MidiEvent c65 = {MidiMessageType::NOTE_ON, 65, 127, 506};
    MidiEvent _c65 = {MidiMessageType::NOTE_OFF, 65, 127, 507};
    MidiEvent c67 = {MidiMessageType::NOTE_ON, 67, 127, 508};
    MidiEvent _c67 = {MidiMessageType::NOTE_OFF, 67, 127, 509};
    MidiEvent c69 = {MidiMessageType::NOTE_ON, 69, 127, 510};
    MidiEvent _c69 = {MidiMessageType::NOTE_OFF, 69, 127, 511};
    MidiEvent c71 = {MidiMessageType::NOTE_ON, 71, 127, 512};
    MidiEvent _c71 = {MidiMessageType::NOTE_OFF, 71, 127, 513};
    MidiEvent c72 = {MidiMessageType::NOTE_ON, 72, 127, 514};
    MidiEvent _c72 = {MidiMessageType::NOTE_OFF, 72, 127, 515};

    std::vector<MidiEvent> events = {c60, _c60, c62, _c62, c64, _c64, c65, _c65, c67, _c67, c69, _c69, c71, _c71, c72, _c72};
    midiScheduler.addEvents(events, 500);
    midiScheduler.player();

    timer.qpcSleepMs(2000);

    return 0;
}