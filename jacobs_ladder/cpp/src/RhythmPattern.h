#ifndef RHYTHM_PATTERN_H
#define RHYTHM_PATTERN_H

#include <vector>
#include <cstdint>
#include <cmath>

#include "Constants.h"
#include "MidiScheduler.h"
#include "PatternUtils.h"
#include "QpcUtils.h"

class RhythmPattern {
public:
    RhythmPattern(RhythmPatternData &rpd);
    ~RhythmPattern();

    /**
     * @brief Get the name of the RhythmPattern object
     * 
     * @return std::string the name of the RhythmPatterm object
     */
    std::string getName();

    /**
     * @brief Get the total number of beats in the RhythmPattern 
     * 
     * @return uint32_t the total number of beats in the RhythmPattern
     */
    uint32_t getNumberOfBeats();

    /**
     * @brief Get the RhythmPattern data representation of this class
     * 
     * @return RhythmPatternData a struct representing the RhythmPattern class's data
     */
    const RhythmPatternData getRhythmPatternData();

    /**
     * @brief Set the Bpm for the RhythmPattern class
     * 
     * @param bpm the beats per minute
     */
    void setBpm(double bpm);

private:
    std::vector<Midi::Beats> mBeats;                // The beats themselves which form the RhythmPattern
    uint32_t mNumberOfBeats {0};                    // The number of beats after any repitions have been applied
    int64_t mTotalNumberOfMidiTicks;                // The total amount of time in MidiTicks that this beat takes up
    double mBpm;                                    // The tempo the rhythm is to be played at
    uint32_t mRepeatNum;                            // The number of times to repeat the pattern (defaults to 0)
    SongStage mStage;                               // The stage of the song the pattern typically occurs in
    std::vector<Mood> mMood;                        // The mood(s) the pattern typically portays
    std::string mName;                              // The name of the pattern (must be unique)

    /**
     * @brief Converts a beat duration (in ms at 60 BPM) to ticks based on the current BPM
     * 
     * @param beatDurationMs The duration of the beat in ms at 60 BPM
     * @param bpm The desired bpm for the RhythmPattern 
     * @return int64_t the number of PPQN (Midi ticks) for a singular beat
     */
    int64_t convertMsToMidiTicks(int32_t beatDurationMs);

    /**
     * @brief Get the total number of PPQN (Pulses Per Quarter Note) aka Midi ticks
     * 
     * @return int64_t the total number of PPQN (Midi ticks) for the whole beat sequence
     */
    int64_t totalMidiTicks();
};

#endif // RHYTHM_PATTERN_H
