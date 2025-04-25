#ifndef PATTERN_UTILS_H
#define PATTERN_UTILS_H

enum PatternDirection {
    ASC,                    // Pattern is ascending toward higher pitch register
    DESC,                   // Pattern is descending toward lower pitch register
    STAT                    // Pattern is stationary neither ascending nor descending when comparing start pitch and end pitch
};

struct RhythmPatternData {
    std::vector<Midi::Beats> beats;
    uint32_t numberOfBeats;
    int64_t totalNumberOfMidiTicks;
    double bpm;

    RhythmPatternData(const std::vector<Midi::Beats>& beats,
        uint32_t numberOfBeats,
        int64_t totalNumberOfMidiTicks,
        double bpm)
    : beats(beats),
    numberOfBeats(numberOfBeats),
    totalNumberOfMidiTicks(totalNumberOfMidiTicks),
    bpm(bpm) {}
};

#endif // PATTERN_UTILS_H 
