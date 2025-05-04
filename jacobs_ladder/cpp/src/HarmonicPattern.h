#ifndef HARMONIC_PATTERN_H
#define HARMONIC_PATTERN_H

#include <vector>
#include <cstdint>
#include <cmath>

#include "Constants.h"
#include "MidiScheduler.h"
#include "PatternUtils.h"
#include "QpcUtils.h"

class HarmonicPattern {
public:
    HarmonicPattern(HarmonicPatternData &rpd);
    ~HarmonicPattern();

    /**
     * @brief Get the HarmonicPattern data representation of this class
     * 
     * @return HarmonicPatternData a struct representing the HarmonicPattern class's data
     */
    const HarmonicPatternData getHarmonicPatternData();

    /**
     * @brief Get the name of the HarmonicPattern object
     * 
     * @return std::string the name of the HarmonicPatterm object
     */
    const std::string getName();

    /**
     * @brief Set the Bpm for the HarmonicPattern class
     * 
     * @param bpm the beats per minute
     */
    void setBpm(double bpm);

private:
    double mBpm;                                    // The tempo for the harmonicPattern to be played within
    int mStartNote;                                 // The start note for the pattern used to calculate all other notes
    int mRepeatStartNote;                           // The start note of the next iteration of the pattern used for shifting behavior
    std::vector<int> mIntervals;                    // The intervalic sequence defining the pattern, each interval referenced against mStartNote
    std::vector<std::string> mCompatibleScales;     // The list of scales which are compatible with the sequence
    uint32_t mRepeatNum;                            // The number of times to repeat the sequence (defaults to 0)
    PatternDirection mDirection;                    // The harmonic direction of the pattern (ASC, DESC, STAT)
    SongStage mStage;                               // The stage of the song in why this pattern is typically deployed
    std::vector<Mood> mMood;                        // The mood that the pattern invokes
    std::string mName;                              // The name of the HarmonicPattern
};

#endif // HARMONIC_PATTERN_H
