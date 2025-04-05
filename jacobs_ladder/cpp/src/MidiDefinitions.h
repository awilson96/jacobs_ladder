#ifndef MIDI_DEFINITIONS_H
#define MIDI_DEFINITIONS_H

#include <cstdint>

enum class MidiMessageType {
    NOTE_OFF = 0x80,
    NOTE_ON  = 0x90,
    POLY_KEY_PRESSURE = 0xA0,
    CONTROL_CHANGE = 0xB0,
    PROGRAM_CHANGE = 0xC0,
    CHANNEL_PRESSURE = 0xD0,
    PITCH_BEND = 0xE0
};

struct MidiEvent {
    MidiMessageType status;
    uint8_t note;
    uint8_t velocity;
    uint64_t time;

    bool operator<(const MidiEvent& other) const {
        return time > other.time;
    }
};

#endif // MIDI_DEFINITIONS_H
