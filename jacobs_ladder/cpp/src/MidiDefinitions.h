#ifndef MIDI_DEFINITIONS_H
#define MIDI_DEFINITIONS_H

struct MidiEvent {
    int status;
    int note;
    int velocity;
    int time;

    bool operator<(const MidiEvent& other) const {
        return time > other.time;
    }
};

#endif // MIDI_DEFINITIONS_H