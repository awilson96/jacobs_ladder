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

    Midi::MidiEvent c60 = {Midi::MidiMessageType::NOTE_ON, 60, 10, timer.qpcGetFutureTime(now, 50LL)};
    Midi::MidiEvent _c60 = {Midi::MidiMessageType::NOTE_OFF, 60, 10, timer.qpcGetFutureTime(now, 60LL)}; 
    Midi::MidiEvent c64 = {Midi::MidiMessageType::NOTE_ON, 64, 20, timer.qpcGetFutureTime(now, 100LL)};
    Midi::MidiEvent _c64 = {Midi::MidiMessageType::NOTE_OFF, 64, 20, timer.qpcGetFutureTime(now, 110LL)};
    Midi::MidiEvent c67 = {Midi::MidiMessageType::NOTE_ON, 67, 30, timer.qpcGetFutureTime(now, 150LL)};
    Midi::MidiEvent _c67 = {Midi::MidiMessageType::NOTE_OFF, 67, 30, timer.qpcGetFutureTime(now, 160LL)};
    Midi::MidiEvent c71 = {Midi::MidiMessageType::NOTE_ON, 71, 40, timer.qpcGetFutureTime(now, 200LL)};
    Midi::MidiEvent _c71 = {Midi::MidiMessageType::NOTE_OFF, 71, 40, timer.qpcGetFutureTime(now, 210LL)};
    Midi::MidiEvent c72 = {Midi::MidiMessageType::NOTE_ON, 72, 50, timer.qpcGetFutureTime(now, 250LL)};
    Midi::MidiEvent _c72 = {Midi::MidiMessageType::NOTE_OFF, 72, 50, timer.qpcGetFutureTime(now, 260LL)};
    Midi::MidiEvent c76 = {Midi::MidiMessageType::NOTE_ON, 76, 60, timer.qpcGetFutureTime(now, 300LL)};
    Midi::MidiEvent _c76 = {Midi::MidiMessageType::NOTE_OFF, 76, 60, timer.qpcGetFutureTime(now, 310LL)}; 
    Midi::MidiEvent c79 = {Midi::MidiMessageType::NOTE_ON, 79, 70, timer.qpcGetFutureTime(now, 350LL)};
    Midi::MidiEvent _c79 = {Midi::MidiMessageType::NOTE_OFF, 79, 70, timer.qpcGetFutureTime(now, 360LL)};
    Midi::MidiEvent c83 = {Midi::MidiMessageType::NOTE_ON, 83, 80, timer.qpcGetFutureTime(now, 400LL)};
    Midi::MidiEvent _c83 = {Midi::MidiMessageType::NOTE_OFF, 83, 80, timer.qpcGetFutureTime(now, 410LL)};
    Midi::MidiEvent c84 = {Midi::MidiMessageType::NOTE_ON, 84, 90, timer.qpcGetFutureTime(now, 450LL)};
    Midi::MidiEvent _c84 = {Midi::MidiMessageType::NOTE_OFF, 84, 90, timer.qpcGetFutureTime(now, 460LL)};
    

    std::vector<Midi::MidiEvent> events = {c60, _c60, c64, _c64, c67, _c67, c71, _c71, c72, _c72, c76, _c76, c79, _c79, c83, _c83, c84, _c84};
    midiScheduler.addEvents(events, 500000);

    // Sleep for 2 second to give time for the player to play all 8 notes
    timer.qpcSleepMs(1000);
}

TEST_CASE("Profile the MidiScheduler addEvent function", "[MidiScheduler][addEvent]") {
    
    MidiScheduler midiScheduler("jacob", false);
    QpcUtils timer;
    long long now = timer.qpcGetTicks();

    Midi::MidiEvent c60;
    long long startLoop = timer.qpcGetTicks();
    for (uint32_t i = 0; i < 1000000; i++) {
        if (i % 2 == 0) {
            c60 = {Midi::MidiMessageType::NOTE_ON, 60, 127, timer.qpcGetFutureTime(now, (i+1) * 50LL)};
        } 
        else {
            c60 = {Midi::MidiMessageType::NOTE_OFF, 60, 127, timer.qpcGetFutureTime(now, (i+1) * 100LL)};
        }
        midiScheduler.addEvent(c60);
    }
    long long endLoop = timer.qpcGetTicks();

    // Check that the loop time is less than 230 ns per AddEvent() call when also considering the loop time for the 1 million events
    std::cout << "\n[AddEvent] Time it takes to add 1 million MidiEvent structs to the priority queue using AddEvent()..." << std::endl;
    long long loopElapsedNs = timer.qpcPrintTimeDiffNs(startLoop, endLoop);
    double meanAddEventTimeWithLoopNs = static_cast<double>(loopElapsedNs) / 1000000.0;
    REQUIRE(meanAddEventTimeWithLoopNs < 300.0); 
}

TEST_CASE("Profile the MidiScheduler addEvents function", "[MidiScheduler][addEvents]") {
    
    MidiScheduler midiScheduler("jacob", false);
    QpcUtils timer;
    long long now = timer.qpcGetTicks();

    Midi::MidiEvent c60;
    std::vector<Midi::MidiEvent> events;
    events.reserve(1000000);
    long long startLoop = timer.qpcGetTicks();
    for (uint32_t i = 0; i < 1000000; i++) {
        if (i % 2 == 0) {
            c60 = {Midi::MidiMessageType::NOTE_ON, 60, 127, timer.qpcGetFutureTime(now, (i+1) * 50LL)};
        } 
        else {
            c60 = {Midi::MidiMessageType::NOTE_OFF, 60, 127, timer.qpcGetFutureTime(now, (i+1) * 100LL)};
        }
        events.push_back(c60);
    }
    midiScheduler.addEvents(events);
    long long endLoop = timer.qpcGetTicks();

    std::cout << "\n[AddEvents] Time it takes to add 1 million MidiEvent structs to the priority queue using AddEvents()..." << std::endl;
    long long loopElapsedNs = timer.qpcPrintTimeDiffNs(startLoop, endLoop);
    double meanAddEventsTimeWithLoopNs = static_cast<double>(loopElapsedNs) / 1000000.0;
    REQUIRE(meanAddEventsTimeWithLoopNs < 350.0);
}

TEST_CASE("Test add event NoteEvent implimentation [MidiScheduler][addEvent]") {

    using namespace Midi;

    MidiScheduler midiScheduler("jacob", true, true);
    QpcUtils timer;
    long long now = timer.qpcGetTicks();
    long long oneSecondFromNow = timer.qpcGetFutureTime(now, 1000);

    // Seed note
    const double tempo = 120.0;
    MidiEvent firstEvent = 
        MidiEvent(
            MidiMessageType::NOTE_ON,
            60,
            40
        );

    NoteEvent note = 
        NoteEvent(
            0.5, 
            NoteDuration::WHOLE, 
            firstEvent,
            tempo,
            oneSecondFromNow
        );

    midiScheduler.addEvent(note);

    note.event.note = 64;
    midiScheduler.addEvent(note);

    note.event.note = 55;
    midiScheduler.addEvent(note);
    
    note.event.note = 58;
    note.event.velocity = 10;
    midiScheduler.addEvent(note);

    timer.qpcSleepMs(5000);
    
}