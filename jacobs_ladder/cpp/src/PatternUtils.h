#ifndef PATTERN_UTILS_H
#define PATTERN_UTILS_H

enum PatternDirection {
    ASC,                    // Pattern is ascending toward higher pitch register
    DESC,                   // Pattern is descending toward lower pitch register
    STAT,                   // Pattern is stationary neither ascending nor descending when comparing start pitch and end pitch
    ANYDIR
};

enum SongStage {
    BEGINNING,              // Pattern is typically used in the beginning of songs
    MIDDLE,                 // Pattern is typically used in the middle of songs
    END,                    // Pattern is typically used in the end of songs
    ANYSTAGE
};

enum Mood {
    HAPPY,
    SAD,
    ANYMOOD
};

struct RhythmPatternData {
    std::string name;
    std::vector<Midi::Beats> beats;
    double bpm;
    uint32_t repeatNum;
    SongStage stage;
    std::vector<Mood> mood;
    uint32_t numberOfBeats;
    int64_t totalNumberOfMidiTicks;
    
    // TODO: Once this is stable make a copy without the numberOfBeats and totaleNumberOfMidiTicks
    RhythmPatternData(
        std::string name,
        const std::vector<Midi::Beats>& beats,
        double bpm,
        uint32_t repeatNum,
        SongStage stage,
        std::vector<Mood> mood,
        uint32_t numberOfBeats,
        int64_t totalNumberOfMidiTicks
        )
    : name(name),
      beats(beats),
      bpm(bpm),
      repeatNum(repeatNum),
      stage(stage),
      mood(mood),
      numberOfBeats(numberOfBeats),
      totalNumberOfMidiTicks(totalNumberOfMidiTicks) {}
};

struct HarmonicPatternData {
    std::string name;
    int startNote;
    int repeatStartNote;
    std::vector<int> intervals;
    std::vector<std::string> compatibleScales;
    double bpm;
    uint32_t repeatNum;
    PatternDirection direction;
    SongStage stage;
    std::vector<Mood> mood;

    HarmonicPatternData(
        std::string name,
        int startNote,
        int repeatStartNote,
        const std::vector<int> &intervals,
        const std::vector<std::string> &compatibleScales,
        double bpm,
        uint32_t repeatNum,
        PatternDirection direction,
        SongStage stage,
        std::vector<Mood> mood
        )
    : name(name),
      startNote(startNote),
      repeatStartNote(repeatStartNote),
      intervals(intervals),
      compatibleScales(compatibleScales),
      bpm(bpm),
      repeatNum(repeatNum),
      direction(direction),
      stage(stage),
      mood(mood) {}
};

#endif // PATTERN_UTILS_H 
