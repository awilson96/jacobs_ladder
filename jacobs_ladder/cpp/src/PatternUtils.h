#ifndef PATTERN_UTILS_H
#define PATTERN_UTILS_H

enum PatternDirection {
    ASC,                    // Pattern is ascending toward higher pitch register
    DESC,                   // Pattern is descending toward lower pitch register
    STAT                    // Pattern is stationary neither ascending nor descending when comparing start pitch and end pitch
};

enum SongStage {
    BEGINNING,              // Pattern is typically used in the beginning of songs
    MIDDLE,                 // Pattern is typically used in the middle of songs
    END,                    // Pattern is typically used in the end of songs
};

struct RhythmPatternData {
    std::string name;
    std::vector<Midi::Beats> beats;
    double bpm;
    uint32_t repeatNum;
    SongStage stage;
    uint32_t numberOfBeats;
    int64_t totalNumberOfMidiTicks;
    
    // TODO: Once this is stable make a copy without the numberOfBeats and totaleNumberOfMidiTicks
    RhythmPatternData(
        std::string name,
        const std::vector<Midi::Beats>& beats,
        double bpm,
        uint32_t repeatNum,
        SongStage stage,
        uint32_t numberOfBeats,
        int64_t totalNumberOfMidiTicks
        )
    : name(name),
    beats(beats),
    bpm(bpm),
    repeatNum(repeatNum),
    stage(stage),
    numberOfBeats(numberOfBeats),
    totalNumberOfMidiTicks(totalNumberOfMidiTicks) {}
};

#endif // PATTERN_UTILS_H 
