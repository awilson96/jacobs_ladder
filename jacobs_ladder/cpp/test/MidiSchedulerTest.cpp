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

TEST_CASE("Profile the MidiScheduler addEvent function", "[MidiScheduler][addEvent(const Midi::MidiEvent &event)]") {
    
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
    std::cout << "Or " << meanAddEventTimeWithLoopNs << "ns per event on average." << std::endl;
    REQUIRE(meanAddEventTimeWithLoopNs < 300.0); 
}

TEST_CASE("Play every note on the piano very quickly", "[MidiScheduler][addEvent(Midi::MidiEvent &event, long long offsetTicks)]") {
    MidiScheduler midiScheduler("jacob", true);
    QpcUtils timer;
    long long now = timer.qpcGetTicks();
    long long later = timer.qpcGetFutureTime(now, 2000);

    Midi::MidiEvent event;
    event.note = 108;
    event.velocity = 80;
    int count = 0;
    for (uint32_t i = 174; i > 0; i--) {
        count++;
        if (i % 2 == 0) {
            event.status = Midi::MidiMessageType::NOTE_ON;
            event.note -= 1;
            event.qpcTime = timer.qpcGetFutureTime(later, (count+1) * 5LL);
        }
        else {
            event.status = Midi::MidiMessageType::NOTE_OFF;
            event.qpcTime += 20LL;
        }
        midiScheduler.addEvent(event);
    }

    timer.qpcSleepMs(4000);
}

TEST_CASE("Test add event NoteEvent implimentation [MidiScheduler][addEvent(Midi::NoteEvent &noteEvent)]") {

    using namespace Midi;

    MidiScheduler midiScheduler("jacob", true, false);
    QpcUtils timer;
    long long now = timer.qpcGetTicks();
    long long oneSecondFromNow = timer.qpcGetFutureTime(now, 2000);

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
            Beats::WHOLE, 
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

    timer.qpcSleepMs(4000);
    
}

TEST_CASE("Four staccato chords test", "[MidiScheduler][addEvent(Midi::NoteEvent &noteEvent, Midi::Beats offsetBeats)]") {
    using namespace Midi;

    MidiScheduler midiScheduler("jacob", true, false);
    QpcUtils timer;
    long long now = timer.qpcGetTicks();

    const double tempo = 120.0;
    MidiEvent firstEvent = 
        MidiEvent(
            MidiMessageType::NOTE_ON,
            62,
            70
        );

    NoteEvent note = 
        NoteEvent(
            0.1, 
            Beats::HALF, 
            firstEvent,
            tempo,
            timer.qpcGetFutureTime(now, 500)
        );

    midiScheduler.addEvent(note, Beats::WHOLE);
    
    note.event.note = 65;
    midiScheduler.addEvent(note, Beats::WHOLE);

    note.event.note = 68;
    midiScheduler.addEvent(note, Beats::WHOLE);

    note.event.note = 72;
    midiScheduler.addEvent(note, Beats::WHOLE);

    note.scheduledTimeTicks = midiScheduler.getPreviouslyScheduledNoteQpcTimeTicks();
    note.event.note = 62;
    midiScheduler.addEvent(note, Beats::WHOLE);

    note.event.note = 65;
    midiScheduler.addEvent(note, Beats::WHOLE);

    note.event.note = 67;
    midiScheduler.addEvent(note, Beats::WHOLE);

    note.event.note = 71;
    midiScheduler.addEvent(note, Beats::WHOLE);

    note.scheduledTimeTicks = midiScheduler.getPreviouslyScheduledNoteQpcTimeTicks();
    note.event.note = 60;
    midiScheduler.addEvent(note, Beats::WHOLE);

    note.event.note = 63;
    midiScheduler.addEvent(note, Beats::WHOLE);

    note.event.note = 67;
    midiScheduler.addEvent(note, Beats::WHOLE);

    note.event.note = 70;
    midiScheduler.addEvent(note, Beats::WHOLE);

    note.scheduledTimeTicks = midiScheduler.getPreviouslyScheduledNoteQpcTimeTicks();
    note.event.note = 57;
    midiScheduler.addEvent(note, Beats::WHOLE);

    note.event.note = 60;
    midiScheduler.addEvent(note, Beats::WHOLE);

    note.event.note = 63;
    midiScheduler.addEvent(note, Beats::WHOLE);

    note.event.note = 67;
    midiScheduler.addEvent(note, Beats::WHOLE);

    timer.qpcSleepMs(8000);

}

TEST_CASE("Profile the MidiScheduler addEvents function", "[MidiScheduler][addEvents(const std::vector<Midi::MidiEvent> &events)]") {
    
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
    std::cout << "Or " << meanAddEventsTimeWithLoopNs << "ns per event on average." << std::endl;
    REQUIRE(meanAddEventsTimeWithLoopNs < 350.0);
}

TEST_CASE("Test the MidiScheduler addEvents function", "[MidiScheduler][addEvents(std::vector<Midi::MidiEvent> &events, long long offsetTicks)]") {

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

TEST_CASE("Descend C Major from fastest note division to slowest", "[MidiScheduler][addEvents(std::vector<Midi::NoteEvent> &noteEvents)]") {
    using namespace Midi;

    MidiScheduler midiScheduler("jacob", false, false);
    QpcUtils timer;
    long long now = timer.qpcGetTicks();

    const double tempo = 120.0;
    MidiEvent firstEvent = 
        MidiEvent(
            MidiMessageType::NOTE_ON,
            72,
            70
        );

    NoteEvent note = 
        NoteEvent(
            0.99, 
            Beats::TRIPLET_THIRTYSECOND, 
            firstEvent,
            tempo,
            timer.qpcGetFutureTime(now, 2000)
        );

    NoteEvent c72 = note;

    note.scheduledTimeTicks = -1;
    note.event.note = 71;
    note.duration = Beats::THIRTYSECOND;
    NoteEvent b71 = note;
    
    note.event.note = 69;
    note.duration = Beats::TRIPLET_SIXTEENTH;
    NoteEvent a69 = note;

    note.event.note = 67;
    note.duration = Beats::SIXTEENTH;
    NoteEvent g67 = note;
   
    note.event.note = 65;
    note.duration = Beats::TRIPLET_EIGHTH;
    NoteEvent f65 = note;

    note.event.note = 64;
    note.duration = Beats::DOTTED_SIXTEENTH;
    NoteEvent e64 = note;

    note.event.note = 62;
    note.duration = Beats::EIGHTH;
    NoteEvent d62 = note;

    note.event.note = 60;
    note.duration = Beats::TRIPLET_QUARTER;
    NoteEvent c60 = note;

    note.event.note = 59;
    note.duration = Beats::DOTTED_EIGHTH;
    NoteEvent b59 = note;

    note.event.note = 57;
    note.duration = Beats::QUARTER;
    NoteEvent a57 = note;

    note.event.note = 55;
    note.duration = Beats::TRIPLET_HALF;
    NoteEvent g55 = note;

    note.event.note = 53;
    note.duration = Beats::DOTTED_QUARTER;
    NoteEvent f53 = note;

    note.event.note = 52;
    note.duration = Beats::HALF;
    NoteEvent e52 = note;

    note.event.note = 50;
    note.duration = Beats::DOTTED_HALF;
    NoteEvent d50 = note;

    note.event.note = 48;
    note.duration = Beats::WHOLE;
    NoteEvent c48 = note;

    std::vector<NoteEvent> events = {c72, b71, a69, g67, f65, e64, d62, c60, b59, a57, g55, f53, e52, d50, c48};
    midiScheduler.addEvents(events);

    midiScheduler.start();

    timer.qpcSleepMs(10000);
}

TEST_CASE("Polyrhythm test", "[MidiScheduler][addEvents(std::vector<Midi::NoteEvent> &noteEvents, Midi::Beats offsetBeats)]") {
    using namespace Midi;

    MidiScheduler midiScheduler("jacob", false, false);
    QpcUtils timer;
    long long now = timer.qpcGetTicks();
    long long startTime = timer.qpcGetFutureTime(now, 2000);

    const double tempo = 120.0;
    MidiEvent firstEvent = 
        MidiEvent(
            MidiMessageType::NOTE_ON,
            63,
            70
        );

    NoteEvent note = 
        NoteEvent(
            0.2, 
            Beats::QUINTUPLET_EIGTH, 
            firstEvent,
            tempo,
            startTime
        );

    NoteEvent eb63 = note;

    for (uint32_t i = 0; i < 4; i++) {

        if (i != 0) {
            note.event.note = 63;
            eb63 = note;
        }
        
        note.scheduledTimeTicks = -1;
        note.event.note = 65;
        NoteEvent f65 = note;

        note.event.note = 67;
        NoteEvent g67 = note;

        note.event.note = 70;
        NoteEvent bb70 = note;

        note.event.note = 72;
        NoteEvent c72 = note;

        std::vector<NoteEvent> events = {eb63, f65, g67, bb70, c72};
        midiScheduler.addEvents(events, Beats::WHOLE);
    }

    note.event.note = 48;
    note.duration = Beats::QUARTER;
    note.scheduledTimeTicks = startTime;
    NoteEvent c48 = note;

    for (uint32_t i = 0; i < 2; i++) {
        if (i != 0) {
            note.event.note = 48;
            c48 = note;
        }

        note.scheduledTimeTicks = -1;
        note.event.note = 46;
        NoteEvent bb46 = note;

        note.event.note = 44;
        NoteEvent ab44 = note;

        note.event.note = 43;
        NoteEvent f43 = note;

        std::vector<NoteEvent> events = {c48, bb46, ab44, f43};
        midiScheduler.addEvents(events, Beats::WHOLE);
    }

    midiScheduler.start();

    timer.qpcSleepMs(6000);

}

TEST_CASE("Test that we can pause and restart", "[MidiScheduler][pause()]") {
    using namespace Midi;

    MidiScheduler midiScheduler("jacob", false, true);
    QpcUtils timer;
    long long now = timer.qpcGetTicks();
    long long twoSecondsFromNow = timer.qpcGetFutureTime(now, 2000);

    const double tempo = 120.0;
    MidiEvent firstEvent = 
        MidiEvent(
            MidiMessageType::NOTE_ON,
            61,
            70
        );

    NoteEvent note = 
        NoteEvent(
            0.5, 
            Beats::SIXTEENTH, 
            firstEvent,
            tempo,
            twoSecondsFromNow
        );

    midiScheduler.addEvent(note);
    long long previouslyScheduledNoteQpcTime = midiScheduler.getPreviouslyScheduledNoteQpcTimeTicks();
    note.scheduledTimeTicks = -1;
    for (uint32_t i = 1; i < 16; i++) {
        if (i % 6 == 0 && i != 0 && i >= 6)
            note.event.note = 69;
        else if (i % 3 == 0 && i != 0 && i >= 3)
            note.event.note = 68;
        else if (i % 2 == 0 && i != 0 && i >= 2)
            note.event.note = 65;
        
        note.scheduledTimeTicks = previouslyScheduledNoteQpcTime;
        midiScheduler.addEvent(note);
        previouslyScheduledNoteQpcTime = midiScheduler.getPreviouslyScheduledNoteQpcTimeTicks();
    }

    midiScheduler.start();

    timer.qpcSleepMs(2500);
    midiScheduler.pause();
    timer.qpcSleepMs(1000);
    midiScheduler.resume();
    timer.qpcSleepMs(4000);

}

TEST_CASE("Test successful beat shifting","[MidiScheduler][shiftBeats(long long offsetTicks)]") {
    using namespace Midi;

    MidiScheduler midiScheduler("jacob", false, true);
    QpcUtils timer;
    long long now = timer.qpcGetTicks();
    long long twoSecondsFromNow = timer.qpcGetFutureTime(now, 2000);

    const double tempo = 150.0;
    MidiEvent firstEvent = 
        MidiEvent(
            MidiMessageType::NOTE_ON,
            45,
            70
        );

    NoteEvent note = 
        NoteEvent(
            0.99, 
            Beats::SIXTEENTH, 
            firstEvent,
            tempo,
            twoSecondsFromNow
        );

    midiScheduler.addEvent(note);

    note.duration = Beats::QUARTER;
    note.scheduledTimeTicks = -1;
    note.event.note = 45;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 47;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 48;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 47;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 45;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 43;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 42;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 40;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 47;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 48;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 45;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 50;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 52;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 40;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.duration = Beats::SIXTEENTH;
    note.event.note = 52;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 40;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.event.note = 52;
    midiScheduler.addEvent(note);

    note.scheduledTimeTicks = -1;
    note.duration = Beats::QUARTER;
    note.event.note = 40;
    midiScheduler.addEvent(note);

    midiScheduler.start();

    std::vector<std::pair<long long, int>> oldBeats = midiScheduler.getBeatSchedule();

    midiScheduler.shiftBeats(10000);

    timer.qpcSleepMs(1000);

    std::vector<std::pair<long long, int>> newBeats = midiScheduler.getBeatSchedule();

    for (uint32_t beatIdx = 0; beatIdx < oldBeats.size(); beatIdx++) {
        REQUIRE(newBeats[beatIdx].first == oldBeats[beatIdx].first + 10000);
        REQUIRE(newBeats[beatIdx].second == oldBeats[beatIdx].second);
    }

    timer.qpcSleepMs(10000);
}

TEST_CASE("Test change tempo","[MidiScheduler][changeTempo(double tempo, long long startQpcTime)]") {

}