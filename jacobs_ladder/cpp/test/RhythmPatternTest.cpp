/**
 * @file RhythmPatternTest.cpp
 * @brief Unit tests for the RhythmPattern class.
 * @author Alex Wilson
 * @date April 2025
 */

 #ifndef NOMINMAX
 #define NOMINMAX
 #endif
 
 #define CATCH_CONFIG_MAIN
 
 // Project Includes
 #include "RhythmPattern.h"
 #include "MidiDefinitions.h"

 // System Includes
 
 // Third Party Includes
 #include "catch_amalgamated.hpp"

 TEST_CASE("Test that repeatNum creates repeatNum number of copies of beats appended to the end of beats", "[RhythmPattern]") {
    std::vector<Midi::Beats> beats = {
        Midi::Beats::QUARTER,
        Midi::Beats::EIGHTH,
        Midi::Beats::EIGHTH,
        Midi::Beats::QUARTER,
        Midi::Beats::HALF,
        Midi::Beats::QUARTER,
        Midi::Beats::HALF
    };

    std::vector<Midi::Beats> expectedBeats = {
        Midi::Beats::QUARTER,
        Midi::Beats::EIGHTH,
        Midi::Beats::EIGHTH,
        Midi::Beats::QUARTER,
        Midi::Beats::HALF,
        Midi::Beats::QUARTER,
        Midi::Beats::HALF,
        Midi::Beats::QUARTER,
        Midi::Beats::EIGHTH,
        Midi::Beats::EIGHTH,
        Midi::Beats::QUARTER,
        Midi::Beats::HALF,
        Midi::Beats::QUARTER,
        Midi::Beats::HALF
    };

    RhythmPatternData rpd = RhythmPatternData("chicken", beats, 120.0, 1, SongStage::END, std::vector<Mood>({Mood::ANYMOOD}), 0, 0);
    RhythmPattern chicken = RhythmPattern(rpd);

    REQUIRE(chicken.getNumberOfBeats() == 14);
    
    RhythmPatternData retrievedData = chicken.getRhythmPatternData();
    REQUIRE(retrievedData.beats.size() == expectedBeats.size());
    for (uint32_t beatIdx = 0; beatIdx < retrievedData.beats.size(); beatIdx++) {
        REQUIRE(retrievedData.beats.at(beatIdx) == expectedBeats.at(beatIdx));
    }

    REQUIRE(retrievedData.numberOfBeats == 14);
    REQUIRE(retrievedData.totalNumberOfMidiTicks == 30720);

 }