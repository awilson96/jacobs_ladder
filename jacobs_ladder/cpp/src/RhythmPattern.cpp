#include <cassert>

#include "RhythmPattern.h"

RhythmPattern::RhythmPattern(RhythmPatternData &rpd)
    : mBeats(rpd.beats),
      mBpm(rpd.bpm),
      mRepeatNum(rpd.repeatNum),
      mStage(rpd.stage),
      mName(rpd.name)
{
    assert(mBeats.size() > 0);
    assert(mBpm >= 10.0);
    assert(mRepeatNum >= 1);
    if (mRepeatNum > 1) {
        std::vector<Midi::Beats> originalBeats = mBeats;
        mBeats.reserve(mBeats.size() + mRepeatNum * mBeats.size());
        
        for (uint32_t i = 1; i < mRepeatNum; i++) {
            mBeats.insert(mBeats.end(), originalBeats.begin(), originalBeats.end());
        }
    }
    mNumberOfBeats = mBeats.size();
    mTotalNumberOfMidiTicks = totalMidiTicks();
}

RhythmPattern::~RhythmPattern() {}

uint32_t RhythmPattern::getNumberOfBeats() {
    return mNumberOfBeats;
}

const RhythmPatternData RhythmPattern::getRhythmPatternData() {
    return RhythmPatternData(mName, mBeats, mBpm, mRepeatNum, mStage, mNumberOfBeats, mTotalNumberOfMidiTicks);
}

void RhythmPattern::setBpm(double bpm) {
    mBpm = bpm;
}

int64_t RhythmPattern::convertMsToMidiTicks(int32_t beatDurationMs) {
    return static_cast<int64_t>(
        std::round(std::abs(beatDurationMs) * (TICKS_PER_QUARTER_NOTE * mBpm / MS_PER_MINUTE))
    );
}

int64_t RhythmPattern::totalMidiTicks() {
    int64_t total = 0;
    for (const auto& beat : mBeats) {
        total += convertMsToMidiTicks(static_cast<int32_t>(beat));
    }
    return total;
}

