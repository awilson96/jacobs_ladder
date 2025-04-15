/**
 * @file MidiSchedulerTest.cpp
 * @brief Unit tests for the MidiScheduler class.
 * @author Alex Wilson
 * @date April 2025
 */

#ifndef NOMINMAX
#define NOMINMAX
#endif

#define CATCH_CONFIG_MAIN

// Project Includes
#include "MidiScheduler.h"
#include "MidiDefinitions.h"
#include "QpcUtils.h"
#include "rtmidi/RtMidi.h"

// System Includes
#include <cstdlib>

// Third Party Includes
#include "catch_amalgamated.hpp"


TEST_CASE("Test the MidiScheduler addEvents function", "[MidiScheduler][addEvents]") {

    // Create a MidiScheduler instance with a specific output port name
    MidiScheduler midiScheduler("jacob");
    QpcUtils timer;
    long long now = timer.qpcGetTicks();

    MidiEvent c60 = {MidiMessageType::NOTE_ON, 60, 127, timer.qpcGetFutureTime(now, 50LL)};
    MidiEvent _c60 = {MidiMessageType::NOTE_OFF, 60, 127, timer.qpcGetFutureTime(now, 100LL)}; 
    MidiEvent c62 = {MidiMessageType::NOTE_ON, 62, 127, timer.qpcGetFutureTime(now, 100LL)}; 
    MidiEvent _c62 = {MidiMessageType::NOTE_OFF, 62, 127, timer.qpcGetFutureTime(now, 150LL)};
    MidiEvent c64 = {MidiMessageType::NOTE_ON, 64, 127, timer.qpcGetFutureTime(now, 150LL)};
    MidiEvent _c64 = {MidiMessageType::NOTE_OFF, 64, 127, timer.qpcGetFutureTime(now, 200LL)};
    MidiEvent c65 = {MidiMessageType::NOTE_ON, 65, 127, timer.qpcGetFutureTime(now, 200LL)};
    MidiEvent _c65 = {MidiMessageType::NOTE_OFF, 65, 127, timer.qpcGetFutureTime(now, 250LL)};
    MidiEvent c67 = {MidiMessageType::NOTE_ON, 67, 127, timer.qpcGetFutureTime(now, 250LL)};
    MidiEvent _c67 = {MidiMessageType::NOTE_OFF, 67, 127, timer.qpcGetFutureTime(now, 300LL)};
    MidiEvent c69 = {MidiMessageType::NOTE_ON, 69, 127, timer.qpcGetFutureTime(now, 300LL)};
    MidiEvent _c69 = {MidiMessageType::NOTE_OFF, 69, 127, timer.qpcGetFutureTime(now, 350LL)};
    MidiEvent c71 = {MidiMessageType::NOTE_ON, 71, 127, timer.qpcGetFutureTime(now, 350LL)};
    MidiEvent _c71 = {MidiMessageType::NOTE_OFF, 71, 127, timer.qpcGetFutureTime(now, 400LL)};
    MidiEvent c72 = {MidiMessageType::NOTE_ON, 72, 127, timer.qpcGetFutureTime(now, 400LL)};
    MidiEvent _c72 = {MidiMessageType::NOTE_OFF, 72, 127, timer.qpcGetFutureTime(now, 450LL)};

    std::vector<MidiEvent> events = {c60, _c60, c62, _c62, c64, _c64, c65, _c65, c67, _c67, c69, _c69, c71, _c71, c72, _c72};
    REQUIRE(midiScheduler.addEvents(events, 500));
    midiScheduler.player();
}

TEST_CASE("Profile the MidiScheduler addEvent function", "[MidiScheduler][addEvent]") {
    
    MidiScheduler midiScheduler("jacob");
    QpcUtils timer;
    long long now = timer.qpcGetTicks();

    MidiEvent c60;
    long long startLoop = timer.qpcGetTicks();
    for (uint32_t i = 0; i < 1000000; i++) {
        if (i % 2 == 0) {
            c60 = {MidiMessageType::NOTE_ON, 60, 127, timer.qpcGetFutureTime(now, (i+1) * 50LL)};
        } 
        else {
            c60 = {MidiMessageType::NOTE_OFF, 60, 127, timer.qpcGetFutureTime(now, (i+1) * 100LL)};
        }
        midiScheduler.addEvent(c60);
    }
    long long endLoop = timer.qpcGetTicks();

    // Check that the loop time is less than 275 ns per AddEvent() call when also considering the loop time for the 1 million events
    std::cout << "\n[AddEvent] Time it takes to add 1 million MidiEvent structs to the priority queue using AddEvent()..." << std::endl;
    long long loopElapsedNs = timer.qpcPrintTimeDiffNs(startLoop, endLoop);
    double meanAddEventTimeWithLoop = static_cast<double>(loopElapsedNs) / 1000000.0;
    REQUIRE(meanAddEventTimeWithLoop < 275.0); 
}

TEST_CASE("Profile the MidiScheduler addEvents function", "[MidiScheduler][addEvents]") {
    
    MidiScheduler midiScheduler("jacob");
    QpcUtils timer;
    long long now = timer.qpcGetTicks();

    MidiEvent c60;
    std::vector<MidiEvent> events;
    events.reserve(1000000);
    long long startLoop = timer.qpcGetTicks();
    for (uint32_t i = 0; i < 1000000; i++) {
        if (i % 2 == 0) {
            c60 = {MidiMessageType::NOTE_ON, 60, 127, timer.qpcGetFutureTime(now, (i+1) * 50LL)};
        } 
        else {
            c60 = {MidiMessageType::NOTE_OFF, 60, 127, timer.qpcGetFutureTime(now, (i+1) * 100LL)};
        }
        events.push_back(c60);
    }
    midiScheduler.addEvents(events);
    long long endLoop = timer.qpcGetTicks();

    std::cout << "\n[AddEvents] Time it takes to add 1 million MidiEvent structs to the priority queue using AddEvents()..." << std::endl;
    long long loopElapsedNs = timer.qpcPrintTimeDiffNs(startLoop, endLoop);
    double meanPushBackTimeWithLoop = static_cast<double>(loopElapsedNs) / 1000000.0;
    REQUIRE(meanPushBackTimeWithLoop < 300.0);
}