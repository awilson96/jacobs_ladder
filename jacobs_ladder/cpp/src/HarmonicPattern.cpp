#include <cassert>

#include "HarmonicPattern.h"

HarmonicPattern::HarmonicPattern(HarmonicPatternData &hpd)
    : mName(hpd.name),
      mStartNote(hpd.startNote),
      mRepeatStartNote(hpd.repeatStartNote),
      mIntervals(hpd.intervals),
      mCompatibleScales(hpd.compatibleScales),
      mBpm(hpd.bpm),
      mRepeatNum(hpd.repeatNum),
      mDirection(hpd.direction),
      mStage(hpd.stage),
      mMood(hpd.mood)
{
    assert(!mName.empty());
    assert(mIntervals.size() > 0);
    if (mRepeatNum >= 1) {
        int diff = mRepeatStartNote - mStartNote;

        std::vector<int> originalIntervals = mIntervals;
        mIntervals.reserve(mIntervals.size() + mRepeatNum * mIntervals.size());
    }
}

HarmonicPattern::~HarmonicPattern() {}

const std::string HarmonicPattern::getName() { return mName; }

const HarmonicPatternData HarmonicPattern::getHarmonicPatternData() { 
    return HarmonicPatternData(
        mName,
        mStartNote,
        mRepeatStartNote,
        mIntervals,
        mCompatibleScales,
        mBpm,
        mRepeatNum,
        mDirection,
        mStage,
        mMood
    ); 
}

void HarmonicPattern::setBpm(double bpm) { mBpm = bpm; }

