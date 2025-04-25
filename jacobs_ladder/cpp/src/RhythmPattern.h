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
    RhythmPattern(std::vector<Midi::Beats> beats, double bpm = DEFAULT_BPM);
    ~RhythmPattern();

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
    RhythmPatternData getRhythmPatternData();

    /**
     * @brief Set the Bpm for the RhythmPattern class
     * 
     * @param bpm the beats per minute
     */
    void setBpm(double bpm);

private:
    std::vector<Midi::Beats> mBeats;
    uint32_t mNumberOfBeats {0};
    int64_t mTotalNumberOfMidiTicks;
    double mBpm; 

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
