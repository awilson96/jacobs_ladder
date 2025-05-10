#ifndef MIDI_DEFINITIONS_H
#define MIDI_DEFINITIONS_H

#include <cstdint>

namespace Midi {

    // Midi status types used by the MidiScheduler
    enum class MidiMessageType : uint8_t {
        NOTE_OFF = 0x80,
        NOTE_ON  = 0x90,
        POLY_KEY_PRESSURE = 0xA0,
        CONTROL_CHANGE = 0xB0,
        PROGRAM_CHANGE = 0xC0,
        CHANNEL_PRESSURE = 0xD0,
        PITCH_BEND = 0xE0
    };

    // Note durations based on 60 BPM in ms where the quarter note is equal to the 60 BPM pulse
    enum class Beats : int32_t {
        SIXTEEN_MEASURES = 64000,
        EIGHT_MEASURES = 32000,
        FOUR_MEASURES = 16000,
        TWO_MEASURES = 8000,
        MEASURE = 4000,
        WHOLE = 4000,
        WHOLE_REST = -4000,
        DOTTED_HALF = 3000,
        DOTTED_HALF_REST = -3000,
        HALF = 2000,
        HALF_REST = -2000,
        DOTTED_QUARTER = 1500,
        DOTTED_QUARTER_REST = -1500,
        TRIPLET_HALF = 1333,
        TRIPLET_HALF_REST = -1333,
        QUARTER = 1000,
        QUARTER_REST = -1000,
        QUINTUPLET_QUARTER = 800,
        QUINTUPLET_QUARTER_REST = -800,
        DOTTED_EIGHTH = 750,
        DOTTED_EIGHTH_REST = -750,
        TRIPLET_QUARTER = 666,
        TRIPLET_QUARTER_REST = -666,
        SEPTUPLET_QUARTER = 571,
        SEPTUPLET_QUARTER_REST = -571,
        EIGHTH = 500,
        EIGHTH_REST = -500,
        QUINTUPLET_EIGTH = 400,
        QUINTUPLET_EIGTH_REST = -400,
        DOTTED_SIXTEENTH = 375,
        DOTTED_SIXTEENTH_REST = -375,
        TRIPLET_EIGHTH = 333,
        TRIPLET_EIGHTH_REST = -333,
        SIXTEENTH = 250,
        SIXTEENTH_REST = -250,
        TRIPLET_SIXTEENTH = 166,
        TRIPLET_SIXTEENTH_REST = -166,
        THIRTYSECOND = 125,
        THIRTYSECOND_REST = -125,
        TRIPLET_THIRTYSECOND = 83,
        TRIPLET_THIRTYSECOND_REST = -83,
        ZERO = 0
    };

    
    struct MidiEvent {
        MidiMessageType status;                     // The status message indicating either NOTE_ON or NOTE_OFF. Can optionally include CC (Control Change) messages, but this is uncommon.
        uint8_t note;                               // The note number represented as an integer where the piano range is from A0 -> C8 or [21-108]
        uint8_t velocity;                           // How quiet or loud the note is played, where 0 is the quietest and 127 the loudest [0-127]
        long long qpcTime;                          // A future tick time based on the Query Performance Counter which usually operates at or around 10 kHz. This can be thought of as the start time for a MidiEvent.

        MidiEvent()
        : status(MidiMessageType::NOTE_OFF), note(0), velocity(0), qpcTime(0) {}

        MidiEvent(MidiMessageType status, uint8_t note, uint8_t velocity)
        : status(status), note(note), velocity(velocity), qpcTime(0) {}

        MidiEvent(MidiMessageType status, uint8_t note, uint8_t velocity, long long qpcTime)
        : status(status), note(note), velocity(velocity), qpcTime(qpcTime) {}

        MidiEvent(const MidiEvent& other, long long durationTicks)
        : status(MidiMessageType::NOTE_OFF),
          note(other.note),
          velocity(other.velocity),
          qpcTime(other.qpcTime + durationTicks) {}
    
        bool operator<(const MidiEvent& other) const {
            return qpcTime > other.qpcTime;
        }
    };
    
    struct NoteEvent {
        double division;                            // The percentage duration length the note is held for (0-1) exclusive. The division is always shorter than duration by some threshold
        Beats duration;                             // The length the note is represented for symbolically in context to other notes. Useful for establishing the start time of the next note or rest.
        MidiEvent event;                            // A MidiEvent with valid status, note, and velocity fields. Only the qpcTime is populated using the components of the NoteEvent struct
        double tempo;                               // The current tempo for the note being held. 
        long long scheduledTimeTicks;               // The scheduled start time for the note (NOTE_ON message). If scheduledTimeTicks is less than 0, then chaining is assumed (i.e. use the previously scheduled note's end time)

        NoteEvent()
        : division(0.5),
          duration(Beats::QUARTER),
          event(),
          tempo(-1),
          scheduledTimeTicks(-1) {}

        NoteEvent(Beats duration, const MidiEvent& event, double tempo)
        : division(0.5),
          duration(duration),
          event(event),
          tempo(tempo),
          scheduledTimeTicks(-1) {}
        
        NoteEvent(double division, Beats duration, const MidiEvent& event, long long scheduledTimeTicks)
        : division(division),
          duration(duration),
          event(event),
          tempo(-1),
          scheduledTimeTicks(scheduledTimeTicks) {}

        NoteEvent(double division, Beats duration, const MidiEvent& event, double tempo, long long scheduledTimeTicks)
        : division(division),
          duration(duration),
          event(event),
          tempo(tempo),
          scheduledTimeTicks(scheduledTimeTicks) {}

        NoteEvent(const NoteEvent& other)
        : division(other.division),
          duration(other.duration),
          event(other.event),
          tempo(other.tempo),
          scheduledTimeTicks(other.scheduledTimeTicks) {}
    };

}



#endif // MIDI_DEFINITIONS_H
