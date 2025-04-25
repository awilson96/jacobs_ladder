#include "RhythmPattern.h"

RhythmPattern::RhythmPattern(std::vector<Midi::Beats> beats, double bpm)
    : mBpm(bpm),
      mBeats(beats) {
    mNumberOfBeats = beats.size();
    mTotalNumberOfMidiTicks = totalMidiTicks();
}

RhythmPattern::~RhythmPattern() {}

uint32_t RhythmPattern::getNumberOfBeats() {
    return mNumberOfBeats;
}

RhythmPatternData RhythmPattern::getRhythmPatternData() {
    return RhythmPatternData(
        mBeats,
        mNumberOfBeats,
        mTotalNumberOfMidiTicks,
        mBpm
    );
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

