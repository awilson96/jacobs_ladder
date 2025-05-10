#ifndef VELOCITY_PATTERN_H
#define VELOCITY_PATTERN_H

#include <vector>
#include <cstdint>
#include <cmath>

#include "Constants.h"
#include "MidiScheduler.h"
#include "PatternUtils.h"
#include "QpcUtils.h"

class VelocityPattern {
public:
    VelocityPattern(VelocityPatternData &rpd);
    ~VelocityPattern();

    /**
     * @brief Get the name of the VelocityPattern object
     * 
     * @return std::string the name of the RhythmPatterm object
     */
    std::string getName();

    /**
     * @brief Get the total number of beats in the VelocityPattern 
     * 
     * @return uint32_t the total number of beats in the VelocityPattern
     */
    uint32_t getNumberOfBeats();

    /**
     * @brief Get the VelocityPattern data representation of this class
     * 
     * @return VelocityPatternData a struct representing the VelocityPattern class's data
     */
    const VelocityPatternData getVelocityPatternData();

private:
    std::vector<VelocityDynamics> mDynamics;        // The strength of each note in terms of VelocityDynamics 
    std::vector<int> mDynamicsInt;                  // The strength of each note in terms of velocity (0-127)
    std::vector<int> mCrop;                         // The length in terms of number of notes to crop the velocity pattern to
    uint32_t mRepeatNum;                            // The number of times to repeat the pattern (defaults to 0)
    std::string mName;                              // The name of the pattern (must be unique)
};

#endif // VELOCITY
